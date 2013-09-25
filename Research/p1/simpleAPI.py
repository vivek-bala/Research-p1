import sys
import os
import saga
from pilot import PilotComputeService, ComputeDataService, State
class simple:
	def __init__(self,no_jobs,pilot,COORD_url=None):
		self.no_jobs = no_jobs
		self.pilot = pilot
		if(COORD_url == None):
			self.COORD = "redis://ILikeBigJob_wITH-REdIS@gw68.quarry.iu.teragrid.org:6379"
		else:
			self.COORD = COORD_url
		
	def check(self):
		print 'Checkup time'
		print self.COORD
		
	def startpilot(self):
		print 'Start pilot service'
		self.pilot_compute_service = PilotComputeService(self.COORD)
		self.pilot_compute_description = { 
						"service_url" : self.pilot["service_url"]
						}
		if self.pilot.has_key("number_of_processes"):
			self.pilot_compute_description["number_of_processes"] = self.pilot["number_of_processes"] 
		if self.pilot.has_key("working_directory"):
			self.pilot_compute_description["working_directory"] = self.pilot["working_directory"]
		if self.pilot.has_key("queue"):
			self.pilot_compute_description["queue"] = self.pilot["queue"]
		if self.pilot.has_key("walltime"):
			self.pilot_compute_description["walltime"] = self.pilot["walltime"]
		self.pilotjob = self.pilot_compute_service.create_pilot(pilot_compute_description=self.pilot_compute_description)
		print 'Pilot successfully started'
	
	def startCU(self):
		print 'Starting Compute Unit submissions'
		self.compute_data_service = ComputeDataService()
		self.compute_data_service.add_pilot_compute_service(self.pilot_compute_service)
		for i in range(self.no_jobs):
			print 'Submitting job %s on %s'%(i+1,self.pilot["service_url"])
			self.compute_unit_description = {
							"executable":"/bin/echo",
							"arguments" : ["$MYOUTPUT"],
							"environment" : {'MYOUTPUT':'"Hello from Simple API"'},
							"number_of_processes" : 1,
							"output" : "stdout.txt",
							"error" : "stderr.txt"
							}
			self.compute_unit = self.compute_data_service.submit_compute_unit(self.compute_unit_description)
		print 'All Compute Units Submitted. Waiting for completion'
		self.compute_data_service.wait()
		print 'All CU executions completed'
		
	def terminate(self):
		print 'Terminating pilot'
		self.compute_data_service.cancel()
		self.pilot_compute_service.cancel()
							

