from gsf import Server, Service, Job
import requests

session = requests.Session()
session.auth = ('admin','password')

server = Server('mjdeeplearning', '9191',session=session)

print(server.version)
print(server.description)
print(server.requestHandlers)

services = server.services()

print(services)

service = server.service('ENVI')

print(service.name)
print(service.description)

tasks = service.tasks()

inputRasterUrl = server.url+"/data/qb_boulder_msi"
inputParameters = {
      "INPUT_RASTER" : {
        "FACTORY": 'OptimizedLinearStretchRaster',
        "INPUT_RASTER": {
          "FACTORY": 'SubsetRaster',
          "BANDS": [2, 1, 0],
          "INPUT_RASTER" : {
            "URL": inputRasterUrl,
            "FACTORY": 'URLRaster'
          }
        }
      }
}

task = service.task('ExportRasterToPNG')


wait = True
job = task.submit(parameters=inputParameters)

if wait :     
  job.wait_for_done()
  results = job.results
  print(results)
else:
  server.cancelJob(job.job_id)
  

jobs = server.jobs
print(jobs)

jobs_succeeded = server.getJobs(jobStatus='Succeeded', taskName="ExportRasterToPNG")
jobs_running = server.getJobs(jobStatus='Started')



print(jobs_running)