# Imports
import os
import shutil
import time
import sys
from cosi_dc.pipeline.make_orientation_bins import make_bins
import yaml
from cosi_dc.pipeline.run_dc import RunDataChallenge

# Get parameters from data challene instance:
instance = RunDataChallenge("inputs.yaml")
name = instance.name
orientation_file = instance.orientation_file
num_sims = instance.num_sims 
run_type = instance.run_type
clear = instance.clear_sims 
mcosima = instance.mcosima
num_cores = instance.num_cores

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
    
    os.system("scp run_sims.py inputs.yaml %s" %this_dir)
    os.chdir(this_dir)
    new_dir = os.getcwd()
    
    # Copy orientation file for ith time bin:
    this_ori_path = os.path.join(home,"Orientation_Bins")
    this_ori_name = "bin_%s.ori" %str(i)
    this_ori_file = os.path.join(this_ori_path,this_ori_name)
    shutil.copy2(this_ori_file, 'GalacticScan.ori')

    # Return home:
    os.chdir(home)

if run_type == "gnu_parallel":

    f = open('gnu_parallel.sh','w')
    f.write('#PBS -N parallel\n')
    f.write('#PBS -l select=50:ncpus=10:mem=50gb:interconnect=1g,walltime=48:00:00\n\n')
    f.write('#the MEGAlib environment first needs to be sourced:\n')
    f.write('cd /zfs/astrohe/Software\n')
    f.write('source COSIMain_u2.sh\n')
    f.write('module add gnu-parallel\n\n')
    f.write('#change to home directory and run job\n')
    f.write('cd %s\n' %home)
    f.write('parallel --delay=5 -j%s python gnu_parallel.py ::: {0..%s}' %(str(num_sims+extra),str(num_sims+extra-1)))
    f.close()

# Make main output directory:
os.system("mkdir Output")

if mcosima == False:

    # Write combined tra file:
    f = open("Output/%s.inc1.id1.tra" %name,"w")
    f.write("TYPE TRA\n\n")

    for i in range(0,num_sims+extra):
    
        this_name = "Simulations/sim_%s/Output/%s.inc1.id1.tra.gz" %(str(i),name)
        this_file = os.path.join(home,this_name)
        f.write("IN %s\n" %this_file)

    f.write("EN")
    f.close()
    os.system("gzip %s" %"Output/%s.inc1.id1.tra" %name)

if mcosima == True:
   
    # Write total combined tra file for each cosima instance:
    g = open("Output/%s.inc1.id1.tra" %(name),"w")
    g.write("TYPE TRA\n\n")
    
    # Iterate through each cosima instance:
    for s in range(1,num_cores+1):

        # Write combined tra file for given cosima instance:
        this_dir = "Output/core_" + str(s)
        os.system("mkdir %s" %this_dir)
        os.system("mkdir %s/Output" %this_dir)
        f = open("%s/Output/%s.inc1.id1.tra" %(this_dir,name),"w")
        f.write("TYPE TRA\n\n")

        for i in range(0,num_sims+extra):

            this_name = "Simulations/sim_%s/Output/%s.p1.inc%s.id1.tra.gz" %(str(i),name,str(s))
            this_file = os.path.join(home,this_name)
            f.write("IN %s\n" %this_file)
            g.write("IN %s\n" %this_file)

        f.write("EN")
        f.close()
        os.system("gzip %s" %"%s/Output/%s.inc1.id1.tra" %(this_dir,name))

    g.write("EN")
    g.close()
    os.system("gzip %s" %"Output/%s.inc1.id1.tra" %(name))
