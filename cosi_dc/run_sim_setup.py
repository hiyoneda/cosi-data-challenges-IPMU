# Imports:
from cosi_dc.pipeline.sim_setup import Setup
import cosi_dc
import os

# Initial setup of source directory
Setup("inputs.yaml").setup_srcs()

# Copy submission files:
working_dir = os.getcwd()
dc_dir = os.path.split(cosi_dc.__file__)[0]
submit_files = os.path.join(dc_dir,"{run_parallel_sims.py,parallel.py,run_sims_cosima.py,run_sims_revan.py,submit_jobs.py}")
os.system("scp %s %s" %(submit_files, working_dir))
