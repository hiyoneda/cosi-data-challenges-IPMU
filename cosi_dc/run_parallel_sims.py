# Imports
import os
import shutil
import time
import sys
from cosi_dc.pipeline.make_orientation_bins import make_bins
import yaml
from cosi_dc.pipeline.run_dc import RunDataChallenge

# Please change them if needed.
node = 1 # num. of nodes for each job request. Be careful that it is not the same as the number of total nodes in your simulation. Basically, you don't have to change this.
ncpus = 1 # num. of cps on a node
mem = 16 # size of memory on a node
mailoption = "a"
walltime = "24:00:00"
qtype = "tiny"

# Get parameters from data challene instance:
instance = RunDataChallenge("inputs.yaml")
name = instance.name
orientation_file = instance.orientation_file
lightcurve_file = instance.lightcurve_file
lightcurve = instance.lightcurve
num_sims = instance.num_sims 
run_type = instance.run_type
clear = instance.clear_sims 
mcosima = instance.mcosima
num_cores = instance.num_cores

# Parameters for array jobs parallel
num_run_in_node = 8

# Make orientation time bins:
# Note: the function returns 0 or 1 depending if an extra file is needed (see for loop below).
extra = make_bins(num_sims,orientation_file,lightcurve,lightcurve_file)

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
    
    os.system("scp run_script_single_thread.sh run_sims_cosima.py run_sims_revan.py inputs.yaml %s" %this_dir)
    os.chdir(this_dir)
    new_dir = os.getcwd()
    
    # Copy orientation file for ith time bin:
    this_ori_path = os.path.join(home,"Orientation_Bins")
    this_ori_name = "bin_%s.ori" %str(i)
    this_ori_file = os.path.join(this_ori_path,this_ori_name)
    shutil.copy2(this_ori_file, 'GalacticScan.ori')

    if lightcurve == True:
        
        # Copy lightcurve file for ith time bin:
        this_lc_name = "bin_%s.dat" %str(i)
        this_lc_file = os.path.join(this_ori_path,this_lc_name)
        shutil.copy2(this_lc_file, 'lightcurve.dat')
    
    if run_type == "mult_nodes":
    
        # Write batch submission file:
        f = open('multiple_batch_submission.pbs','w')

        f.write( "#!/bin/bash\n")
        f.write(f"#PBS -N sim_{i}\n")
        f.write(f"#PBS -l select={node}:ncpus={ncpus}:mem={mem}gb\n")
        f.write(f"#PBS -l walltime={walltime}\n")
        f.write(f"#PBS -m {mailoption}\n")
        f.write(f"#PBS -q {qtype}\n")
        f.write( "\n")
        f.write(f"cd {new_dir}\n")
        f.write(f"sh run_script_single_thread.sh `pwd`\n")
        f.close()
    
        # Submit job:
        os.system("qsub multiple_batch_submission.pbs")

        # Sleep a bit in order to not overwhelm batch system:
        time.sleep(3)

    # Return home:
    os.chdir(home)

if run_type == "array_jobs-parallel":
    num_node = (num_sims + extra) // num_run_in_node + 1

    print(f"will use {num_node} nodes")
    print(f"in each node, {num_run_in_node} simulations will be performed in parallel.")

    f = open('array_job-parallel.pbs','w')

    f.write( "#!/bin/bash\n")
    f.write( "#PBS -N array-parallel\n")
    f.write(f"#PBS -l select={node}:ncpus={ncpus}:mem={mem}gb\n")
    f.write(f"#PBS -l walltime={walltime}\n")
    f.write(f"#PBS -m {mailoption}\n")
    f.write(f"#PBS -q {qtype}\n")
    f.write(f'#PBS -J 0-{num_node-1}\n')
    f.write( "\n")
    f.write( '# Need to delay job start times by random number to prevent overloading system:\n')
    f.write( 'sleep `expr $RANDOM % 60`\n')
    f.write( "\n")
    f.write( 'cd $PBS_O_WORKDIR\n')
    f.write( "for i in {0..%d}\n" % (num_run_in_node-1))
    f.write( "do\n")
    f.write(f'echo "sleep $i;sh run_script_single_thread.sh $PBS_O_WORKDIR/Simulations/sim_`expr $PBS_ARRAY_INDEX \* {num_run_in_node} + $i`"\n')
    f.write(f'done | xargs -P{num_run_in_node} -I@ sh -c "@"\n')

    f.close()

'''
    f.write('#PBS -N array\n')
    f.write('#PBS -l select=1:ncpus=1:mem=15gb:interconnect=1g,walltime=25:00:00\n')
    f.write('#PBS -J 0-%s:7\n\n' %str(num_sims))
    f.write('#Need to delay job start times by random number to prevent overloading system:\n')
    f.write('sleep `expr $RANDOM % 60`\n\n')
    f.write('#The MEGAlib environment first needs to be sourced:\n')
    f.write('cd $tmp/zfs/astrohe/Software\n')
    f.write('source COSIMain_u2.sh\n\n')
    f.write('#Change to home directory and run job\n')
    f.write('cd $PBS_O_WORKDIR\n')
    f.write("module add gnu-parallel\n")
    f.write("parallel --delay=3 -j7 python parallel.py $PBS_ARRAY_INDEX ::: {0..6}")
    f.close()
'''

if run_type == "array_jobs":

    f = open('array_job.pbs','w')

    f.write("#!/bin/bash\n")
    f.write("#PBS -N array\n")
    f.write(f"#PBS -l select={node}:ncpus={ncpus}:mem={mem}gb\n")
    f.write(f"#PBS -l walltime={walltime}\n")
    f.write(f"#PBS -m {mailoption}\n")
    f.write(f"#PBS -q {qtype}\n")
    f.write('#PBS -J 0-%s\n' %str(num_sims+extra-1))
    f.write("\n")
    f.write('# Need to delay job start times by random number to prevent overloading system:\n')
    f.write('sleep `expr $RANDOM % 60`\n')
    f.write("\n")
    f.write('cd $PBS_O_WORKDIR\n')
    f.write("\n")
    f.write(f"sh run_script_single_thread.sh $PBS_O_WORKDIR/Simulations/sim_$PBS_ARRAY_INDEX\n")

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
