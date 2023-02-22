# Imports:
import os, sys
import time
from calc_aeff import CalcAeff
import numpy as np

# Get grid:
grid_list = CalcAeff("inputs.yaml").get_grid(100,5000,10,remove=False)

# Get current working directory:
home_dir = os.getcwd()

for each in grid_list:

    os.chdir(each)
    this_dir = os.path.join(home_dir,each)    
    
    # Write submission file and submit:
    f = open('multiple_batch_submission.pbs','w')

    f.write("#PBS -N %s\n" %each)
    f.write("#PBS -l select=1:ncpus=2:mem=50gb:interconnect=1g,walltime=10:00:00\n\n")
    f.write("#the MEGAlib environment first needs to be sourced:\n")
    f.write("cd /zfs/astrohe/Software\n")
    f.write("source COSIMain_u2.sh\n\n")
    f.write("#change to working directory and run job\n")
    f.write("cd %s\n" %this_dir)
    f.write("python run_sims.py %s" %each)
    f.close()

    os.system("qsub multiple_batch_submission.pbs")
    time.sleep(3)

    os.chdir(home_dir)
