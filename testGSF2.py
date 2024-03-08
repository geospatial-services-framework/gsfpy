from gsf import Server, Service, Job

server = Server('mjdeeplearning', '8282')
print(server.version)
print(server.description)
print(server.requestHandlers)


wait = True

if wait:
  jobs_running = server.getJobs(jobStatus='Started', taskName='ClassifyDataset')
  if len(jobs_running) > 0 :
    for job in jobs_running:
      server.cancelJob(job["jobId"])


services = server.services()

print(services)

service = server.service('javascript')


task = service.task('ClassifyDataset')

inputParameters = {
  "LIDARDIR": "/data/ecassini/Lidar/data/CholetCentreVille3/",
  "MODEL": "pylones_multiv210cm"
}

wait = False
job = task.submit(parameters=inputParameters)

if wait :     
  job.wait_for_done()
  results = job.results
  print(results)
else:
  server.cancelJob(job.job_id)

print(job.status)
  

jobs_succeeded = server.getJobs(jobStatus='Succeeded', taskName="createPatchesForLidarTile")
print(jobs_succeeded)

jobs_running = server.getJobs(jobStatus='Started')
print(jobs_running)