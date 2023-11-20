These scripts have been used on Clemson's palmetto cluster, which uses PBS. 
The recommended scripts to use are array_job.sh and array_job-parallel.sh. 

array_job.sh:
Basic script for submitting array jobs, 
without manually specifying multiple CPUs
per node. In this case, a single job will run
on a single node, using only 1 cpu. Generally,
this is a waste of CPUs. However, many clusters
have special paritions that will automatically send 
jobs of an array to individual CPUs by default, which
makes things very convenient. See the slurm directory 
for some specific examples. This script can also be 
used for such a partition, if available.    

array_job-parallel.sh: 
Basic script for submitting array jobs, 
utilizing multiple CPUs per node with gnu_parallel.
Use this for single chunks, i.e. when each 
job in the array is perfomed on a single node.

array_job_sequence.sh:
Use this when running an array job over multiple nodes. 
The script parallel.py needs to be modified to only take sys.argv[1],
i.e. remove sys.argv[2].

array_job_sequence_simple.sh:
Same as above, but does not use a job array.
Instead, submit each job one at a time. 
The submission is automated with submit_sequence_simple.py. 
The script parallel.py needs to be modified to only take sys.argv[1],
i.e. remove sys.argv[2].
