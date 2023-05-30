from gsf import Server, Service

server = Server('mjdeeplearning', '8282')

print(server.version)
print(server.description)
print(server.requestHandlers)

services = server.services

print(services)

envi_service = server.service('ENVI')

#python_service = server.service("python")

#tasks = envi_service.tasks()

# task = envi_service.task('inventory')

# j = task.submit()

# print(j.error_message)
# print(j.progress_message)

jobs = server.jobs
print(jobs)

jobs_succeeded = server.getJobs(jobStatus='Succeeded')
jobs_running = server.getJobs(jobStatus='Started')


print(jobs_running)