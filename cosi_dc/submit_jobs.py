# Imports:
import os, sys
import time

# Get current working directory:
this_dir = os.getcwd()

# do not change these lines.
megalib_main_path = "/lustre/work/COSI/software/megalib"
megalib_dee2022_path = "/lustre/work/COSI/software/megalib_dee2022"
python_cosi_path = "/lustre/work/COSI/software/python_cosi"

# Write submission file and submit:
f = open('batch_submission.pbs','w')

f.write("#!/bin/bash\n")
f.write("#PBS -N COSIsim_single\n")
f.write("#PBS -l select=1:ncpus=2:mem=50gb\n")
f.write("#PBS -l walltime=01:00:00\n")
f.write("#PBS -m ae\n")
f.write("#PBS -q mini\n")
f.write("\n")
f.write("# Source global definitions\n")
f.write("if [ -f /etc/bashrc ]; then\n")
f.write("	. /etc/bashrc\n")
f.write("fi\n")
f.write("\n")
f.write("#change to working directory and run job\n")
f.write("cd %s\n" %this_dir)
f.write("\n")
f.write("#conda activation\n")
f.write(f"conda activate {python_cosi_path}\n")
f.write("\n")
f.write("#the main MEGAlib environment is sourced\n")
f.write(f"source {megalib_main_path}/bin/source-megalib.sh\n")
f.write("python run_sims_cosima.py\n")
f.write("\n")
f.write("#the dee2022 MEGAlib environment is sourced\n")
f.write(f"source {megalib_dee2022_path}/bin/source-megalib.sh\n")
f.write("python run_sims_revan.py\n")
f.close()

os.system("qsub batch_submission.pbs")
time.sleep(3)
