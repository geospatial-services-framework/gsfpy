from gsf import Server, Service

server = Server('mjdeeplearning', '9191')

print(server.version)
print(server.description)
print(server.requestHandlers)

services = server.services()

print(services)

envi_service = server.service('ENVI')

python_service = server.service("python")

tasks = envi_service.tasks()

inputRasterUrl = server._url+"/data/qb_boulder_msi"
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

task = envi_service.task('ExportRasterToPNG')

j = task.submit(parameters=inputParameters)

print(j.error_message)
print(j.progress_message)

jobs = server.jobs
print(jobs)

jobs_succeeded = server.getJobs(jobStatus='Succeeded', taskName="ExportRasterToPNG")
jobs_running = server.getJobs(jobStatus='Started')


print(jobs_running)