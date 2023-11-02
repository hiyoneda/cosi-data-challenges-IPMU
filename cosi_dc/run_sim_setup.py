# Imports:
from cosi_dc.pipeline.sim_setup import Setup
import cosi_dc
import os

# Initial setup of source directory
Setup("inputs.yaml").setup_srcs()

run_type = Setup("inputs.yaml").run_type
if run_type == "slurm":
    submit_script = "slurm_single.sh"
else: submit_script = "submit_jobs.py"

# Copy submission files:
working_dir = os.getcwd()
dc_dir = os.path.split(cosi_dc.__file__)[0]
submit_files = os.path.join(dc_dir,"{run_parallel_sims.py,run_sims.py,%s}" %submit_script)
os.system("scp %s %s" %(submit_files, working_dir))
