These scripts have been used on Clemson's palmetto cluster, which uses PBS. 

array_job.sh: 
Basic script for submitting array jobs. 
Use this for single chunks, i.e. when each 
job in the array is perfomed on a single node.

array_job_sequence.sh:
Use this when running an array job over multiple nodes. 

array_job_sequence_simple.sh:
Same as above, but does not use a job array.
Instead, submit each job one at a time. 
The submission is automated with submit_sequence_simple.py. 

