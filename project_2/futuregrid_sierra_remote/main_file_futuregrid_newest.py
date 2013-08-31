import os,sys,time,random
import saga
import traceback
from pilot import PilotComputeService, ComputeDataService, State

#REDIS_PWD = os.environ.get('XSEDE_TUTORIAL_REDIS_PASSWORD')
#USER_NAME = os.environ.get('XSEDE_TUTORIAL_USER_NAME')

COORD = "redis://ILikeBigJob_wITH-REdIS@gw68.quarry.iu.teragrid.org:6379"
#COORD = "redis://localhost:6379"

HOSTNAME = "vivek91@sierra.futuregrid.org"

QUEUE = "batch"

WORKDIR = "/N/u/vivek91/"

NUMBER_JOBS = 128     #should be power of two.. 2^N

DATA_SIZE = 1048576    #keep it to power of two .. 2^N

DATA_RANGE = 1024


def merge(left,right):
    result = []
    i,j = 0,0
    while ((i<len(left)) and (j<len(right))):
        if(left[i] <= right[j]):
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    result += left[i:]
    result += right[j:]
    return result

if __name__ == "__main__":
    #Data generation
    data = []
    i=0
    while(i<DATA_SIZE):
        data.append(random.randint(0,DATA_RANGE))
        i+=1
    workdir = saga.filesystem.Directory("sftp://%s/%s" %(HOSTNAME,WORKDIR),saga.filesystem.CREATE_PARENTS)
    mbpy = saga.filesystem.File("file://localhost/%s/sorter.py"%os.getcwd())
    mbpy.copy(workdir.get_url())
    #mbpy = saga.filesystem.File("file://localhost/%s/main_file_futuregrid_newest_localhost.py"%os.getcwd())
    #mbpy.copy(workdir.get_url())
    pilot_tic = time.time()
    pilot_compute_service = PilotComputeService(COORD)
    #describe pilot
    pilot_compute_description = {
                            "service_url" :"pbs+ssh://%s" %HOSTNAME,
                            "number_of_processes" : 8, 
                            "working_directory" : WORKDIR,
                            "walltime": 10
    }
    #create pilot
    pilotjob = pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    pilot_toc = time.time()
    compute_data_service=ComputeDataService()
    compute_data_service.add_pilot_compute_service(pilot_compute_service)
    print 'Finished pilot job creation'
    print 'Start CU submission'
    
    #submit jobs
 #   tasks = list()
    i=0
    job_tic = time.time()
    while(i<NUMBER_JOBS):
	print 'Submitting job',(i+1)
        outputfile = 'file_%s.txt'%(i)
        #job description
        #task_description = pilot.ComputeUnitDescription()
        compute_unit_description= {"executable" : "python","arguments" : [WORKDIR+'/sorter.py',outputfile,str(data[i*(DATA_SIZE/NUMBER_JOBS):(i+1)*(DATA_SIZE/NUMBER_JOBS)])], "number_of_processes" : 1, "output":"stdout.txt","error":"stderror.txt"}
        compute_unit =compute_data_service.submit_compute_unit(compute_unit_description)
#        tasks.append(task)
        i+=1
    wait_tic = time.time()
    compute_data_service.wait()
    wait_toc = time.time()
    job_toc = time.time()
    #sftp back to localhost
    merge_tic = time.time()
    print 'All files generated. Copying back to localhost'
    for txt in workdir.list('file_*.txt'):
    	workdir.copy(txt,'sftp://localhost/%s/'%os.getcwd())
    #Final merger
    print 'Copying finished. Final merger'
    final_data = []
    for x in range(0,NUMBER_JOBS):
        f1 = open('file_%s.txt'%x,'r')
        k = f1.readline().split(',')
        left = final_data
        right = map(int,k)
        final_data = merge(left,right)
        f1.close()
    merge_toc = time.time()
    print 'Terminating pilot jobs'
    compute_data_service.cancel()
    pilot_compute_service.cancel()
    print DATA_SIZE,NUMBER_JOBS,'Total time : ',((pilot_toc-pilot_tic)+(job_toc-job_tic)+(merge_toc-merge_tic)) 
    print 'Pilot setup time : ',(pilot_toc - pilot_tic)
    print 'Subjobs setup time : ',(job_toc - job_tic)
    print 'Subjob wait time : ',(wait_toc - wait_tic)
    print 'Merge time : ',(merge_toc - merge_tic)
