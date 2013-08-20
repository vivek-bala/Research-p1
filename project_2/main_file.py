import os,sys,time,random
import bliss.saga as saga
import traceback
import pilot

REDIS_PWD = os.environ.get('XSEDE_TUTORIAL_REDIS_PASSWORD')
USER_NAME = os.environ.get('XSEDE_TUTORIAL_USER_NAME')

COORD = "redis://%s@gw68.quarry.iu.teragrid.org:6379" % REDIS_PWD

HOSTNAME = "fork://localhost"

QUEUE = "normal"

WORKDIR = os.getenv("HOME")+"/project_2"

NUMBER_JOBS = 8     #should be power of two.. 2^N

DATA_SIZE = 1024     #keep it to power of two .. 2^N

DATA_RANGE = 1024
        
if __name__ == "__main__":
    #Data generation
    data = []
    i=0
    while(i<DATA_SIZE):
        data.append(random.randint(0,DATA_RANGE))
        i+=1

    pilot_compute_service = pilot.PilotComputeService(COORD)
    #describe pilot
    pilot_description = pilot.PilotComputeDescription()
    pilot_description.service_url = "%s" %HOSTNAME
    pilot_description.queue = QUEUE
    pilot_description.number_of_processes = NUMBER_JOBS
    #pilot_description.working_directory = workdir.get_url().path
    pilot_description.walltime = 10
    #create pilot
    pilotjob = pilot_compute_service.create_pilot(pilot_description)

    print 'Finished pilot job creation'
    print 'Start CU submission'
    
    #submit jobs
    tasks = list()
    i=0
    while(i<NUMBER_JOBS):
        outputfile = 'file_%s.txt'%(i)
        #job description
        task_description = pilot.ComputeUnitDescription()
        task_description.executable = "python"
        task_description.arguments = [WORKDIR+'/sorter.py',outputfile,str(data[i*(DATA_SIZE/NUMBER_JOBS):(i+1)*(DATA_SIZE/NUMBER_JOBS)])]
        task_description.walltime = 10
        task_description.number_of_processes = 1
        task = pilotjob.submit_compute_unit(task_description)
        tasks.append(task)
        i+=1
    pilotjob.wait()

    #Final merger
    final_data = []
    for x in range(0,NUMBER_JOBS):
        f1 = open('file_%s.txt'%x,'r')
        k = f1.readline().split(',')
        final_data = final_data + map(int,k)
        f1.close()
    i=0
    while(i<len(final_data)):
        j=i
        while((j>0)and(final_data[j]<final_data[j-1])):
            temp=final_data[j]
            final_data[j]=final_data[j-1]
            final_data[j-1]=temp
            j=j-1
        i+=1
    print final_data
    #End

    
