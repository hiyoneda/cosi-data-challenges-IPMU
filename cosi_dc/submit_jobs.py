# Imports:
import os, sys
import time

# Get current working directory:
this_dir = os.getcwd()

# Write submission file and submit:
f = open('multiple_batch_submission.pbs','w')

f.write("#PBS -N Main_Output\n")
f.write("#PBS -l select=1:ncpus=2:mem=50gb:interconnect=1g,walltime=10:00:00\n\n")
f.write("#the MEGAlib environment first needs to be sourced:\n")
f.write("cd /zfs/astrohe/Software\n")
f.write("source COSIMain_u2.sh\n\n")
f.write("#change to working directory and run job\n")
f.write("cd %s\n" %this_dir)
f.write("python run_sims.py")
f.close()

os.system("qsub multiple_batch_submission.pbs")
time.sleep(3)
