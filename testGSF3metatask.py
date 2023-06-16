from gsf import Server, Service, Job

server = Server(taskUrl='http://mjdeeplearning:9191/Services/javascript/tasks/ComputeAllSpectralIndices')

print(server.version)
print(server.description)
print(server.requestHandlers)

services = server.services()

print(services)

service = server.service('javascript')

print(service.name)
print(service.description)


tasks = service.tasks()

inputRasterUrl = server._url+"/data/qb_boulder_msi"
inputParameters = {
      "SOME_INPUT_RASTER" : {
            "URL": inputRasterUrl,
            "FACTORY": 'URLRaster'
      }
}

task = service.task('ComputeAllSpectralIndices')

wait = True
job = task.submit(parameters=inputParameters)

if wait :     
  job.wait_for_done()
  results = job.results
  print(results)
else:
  server.cancelJob(job.job_id)
  

jobs = server.jobs


jobs_succeeded = server.getJobs(jobStatus='Succeeded', taskName="ComputeAllSpectralIndices")
print(jobs_succeeded)

