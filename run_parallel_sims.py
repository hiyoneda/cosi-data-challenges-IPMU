# Imports
import os
import shutil
import time
import sys
from make_orientation_bins import make_bins
import yaml
from run_data_challenge_module import RunDataChallenge

# Get parameters from data challene instance:
instance = RunDataChallenge("inputs.yaml")
name = instance.name
orientation_file = instance.orientation_file
num_sims = instance.num_sims 
clear = instance.clear_sims 

# Make orientation time bins:
# Note: the function returns 0 or 1 depending if an extra file is needed (see for loop below).
extra = make_bins(num_sims,orientation_file)

# Get working directory:
home = os.getcwd()

# Make main simulation directory:
if os.path.isdir("Simulations") == False:
    os.system("mkdir Simulations")

# Submit jobs:
for i in range(0,num_sims+extra):

    this_dir = "Simulations/sim_" + str(i) 
    
    if clear == True:
    
        # Remove sim_i directory if it already exists:
        if os.path.isdir(this_dir) == True:
            shutil.rmtree(this_dir)
    
        # Make new sim_i directory:
        os.system("mkdir %s" %this_dir)
    
    os.system("scp client_code.py inputs.yaml %s" %this_dir)
    os.chdir(this_dir)
    new_dir = os.getcwd()
    
    # Copy orientation file for ith time bin:
    this_ori_path = os.path.join(home,"Orientation_Bins")
    this_ori_name = "bin_%s.ori" %str(i)
    this_ori_file = os.path.join(this_ori_path,this_ori_name)
    shutil.copy2(this_ori_file, 'GalacticScan.ori')

    # Write batch submission file:
    f = open('multiple_batch_submission.pbs','w')
    f.write("#PBS -N sim_%s\n" %str(i))
    f.write("#PBS -l select=1:ncpus=1:mem=15gb:interconnect=1g,walltime=48:00:00\n\n")
    f.write("#the MEGAlib environment first needs to be sourced:\n")
    f.write("cd /zfs/astrohe/Software\n")
    f.write("source COSIMain.sh\n\n")
    f.write("#change to working directory and run job\n")
    f.write("cd %s\n" %new_dir)
    f.write("python run_sims.py")
    f.close()
    
    # Submit job:
    os.system("qsub multiple_batch_submission.pbs")

    # Sleep a bit in order to not overwhelm batch system:
    time.sleep(3)

    # Return home:
    os.chdir(home)

# Make main output directory:
os.system("mkdir Main_Output")
os.system("mkdir Main_Output/Output")
os.system("scp client_code.py inputs.yaml submit_jobs.py Main_Output")

# Write combined tra file:
f = open("Main_Output/Output/%s.inc1.id1.tra" %name,"w")
f.write("TYPE TRA\n\n")

for i in range(0,num_sims+extra):
    
    this_name = "Simulations/sim_%s/Output/%s.inc1.id1.tra.gz" %(str(i),name)
    this_file = os.path.join(home,this_name)
    f.write("IN %s\n" %this_file)

f.write("EN")
f.close()
os.system("gzip %s" %"Main_Output/Output/%s.inc1.id1.tra" %name)
