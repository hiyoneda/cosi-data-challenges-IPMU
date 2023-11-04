# Imports:
import os, sys
import time

# Please change them if needed.
node = 1 # num. of nodes for each job request. Be careful that it is not the same as the number of total nodes in your simulation. Basically, you don't have to change this.
ncpus = 2 # num. of cps on a node
mem = 50 # size of memory on a node
mailoption = "a"
walltime = "01:00:00"
qtype = "mini"

# Get current working directory:
this_dir = os.getcwd()

# Write submission file and submit:

with open('batch_submission.pbs','w') as f:
    f.write( "#!/bin/bash\n")
    f.write( "#PBS -N COSIsim_single\n")
    f.write(f"#PBS -l select={node}:ncpus={ncpus}:mem={mem}gb\n")
    f.write(f"#PBS -l walltime={walltime}\n")
    f.write(f"#PBS -m {mailoption}\n")
    f.write(f"#PBS -q {qtype}\n")
    f.write( "\n")
    f.write( "cd $PBS_O_WORKDIR\n")
    f.write( "sh run_script_single_thread.sh `pwd`\n")

os.system("qsub batch_submission.pbs")
time.sleep(3)
