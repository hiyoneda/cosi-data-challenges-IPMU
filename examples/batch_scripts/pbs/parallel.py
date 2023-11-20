# Imports:
import sys
import os

# Run directory:

this_run = int(sys.argv[1]) + int(sys.argv[2])
this_dir = "Simulations/sim_%s" %this_run
os.system("scp run_sims.py inputs.yaml %s" %this_dir)
os.chdir(this_dir)
os.system("python run_sims.py")
