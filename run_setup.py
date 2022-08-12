# Imports:
from setup import Setup
from run_data_challenge_module import RunDataChallenge
import os

# Initial setup of source directory
Setup("inputs.yaml").setup_srcs()

# Copy submission files:
working_dir = os.getcwd()
dc_dir = RunDataChallenge("inputs.yaml").dc_dir
submit_files = os.path.join(dc_dir,"{run_parallel_sims.py,run_sims.py,submit_jobs.py}")
os.system("scp %s %s" %(submit_files, working_dir))
