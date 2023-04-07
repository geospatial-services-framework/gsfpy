# Change Log
All notable changes to this project will be documented in this file.

# 2.0.0 / 2023-04-07
- The main reason for this breaking change is the switch from the ese request handler to the gsf request handler. The ese request handler is no longer supported by default in gsf 2.x.  Though this python interface to gsf has not changed much gsfpy 2.0 will no longer support gsf 1.x by default.
- This package no longer supports Python 2.
- The service.tasks method now returns a list of the full task definitions. 
- Switched the job_id from an int to a str.

