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
lightcurve_file = instance.lightcurve_file
lightcurve = instance.lightcurve
num_sims = instance.num_sims 
run_type = instance.run_type
clear = instance.clear_sims 
mcosima = instance.mcosima
num_cores = instance.num_cores

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
    
    os.system("scp run_sims.py inputs.yaml %s" %this_dir)
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
        f.write("#PBS -N sim_%s\n" %str(i))
        f.write("#PBS -l select=1:ncpus=1:mem=15gb:interconnect=1g,walltime=48:00:00\n\n")
        f.write("#the MEGAlib environment first needs to be sourced:\n")
        f.write("cd /zfs/astrohe/Software\n")
        f.write("source COSIMain_u2.sh\n\n")
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

def write_parallel(args):

    """
    Writes intermediate parallel submission script.
    
    args: number of passed arguements. Must be 1 or 2. 
    """

    f = open('parallel.py','w')
    f.write('# Imports:\n')
    f.write('import sys\n')
    f.write('import os\n\n')
    f.write('# Run directory:\n')
    if args not in [1,2]:
        print("ERROR: args must be 1 or 2.")
        sys.exit()
    if args == 1:
        f.write('this_run = int(sys.argv[1])\n')
    if args == 2:
        f.write('this_run = int(sys.argv[1]) + int(sys.argv[2])\n')
    f.write('this_dir = "Simulations/sim_%s" %this_run\n')
    f.write('os.system("scp run_sims.py inputs.yaml %s" %this_dir\n')
    f.write('os.chdir(this_dir)\n')
    f.write('os.system("python run_sims.py")')
    f.close()
    
    return

if run_type == "array_jobs-parallel":
    
    # Main submission script:
    f = open('array_job.sh','w')
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

    # Make parallel file:
    write_parallel(2)

if run_type == "array_jobs":
    f = open('array_job.sh','w')
    f.write('#PBS -N array\n')
    f.write('#PBS -l select=1:ncpus=1:mem=15gb:interconnect=1g,walltime=25:00:00\n')
    f.write('#PBS -J 0-%s\n\n' %str(num_sims))
    f.write('#Need to delay job start times by random number to prevent overloading system:\n')
    f.write('sleep `expr $RANDOM % 60`\n\n')
    f.write('#The MEGAlib environment first needs to be sourced:\n')
    f.write('cd $tmp/zfs/astrohe/Software\n')
    f.write('source COSIMain_u2.sh\n\n')
    f.write('#Change to home directory and run job\n')
    f.write('cd $PBS_O_WORKDIR\n')
    f.write('scp run_sims.py inputs.yaml Simulations/sim_$PBS_ARRAY_INDEX\n')
    f.write('cd Simulations/sim_$PBS_ARRAY_INDEX\n')
    f.write('python run_sims.py')
    f.close()

if run_type == "slurm":
    
    # Main submission script
    f = open('slurm_mult.sh','w')
    f.write('#!/bin/bash\n')
    f.write('#SBATCH --time=0:55:00\n')
    f.write('#SBATCH -o output.%j\n')
    f.write('#SBATCH -e error.%j\n')
    f.write('#SBATCH --qos=debug\n')
    f.write('#SBATCH --account=j1042\n')
    f.write('#SBATCH --job-name=511_thick10x\n')
    f.write('#SBATCH --ntasks=1000\n')
    f.write('#SBATCH --mem-per-cpu=3G\n\n')
    f.write('#The MEGAlib environment first needs to be sourced:\n')
    f.write('cd /discover/nobackup/ckarwin/Software\n')
    f.write('source COSI.sh\n\n')
    f.write('cd $SLURM_SUBMIT_DIR\n\n')
    f.write('for i in {0..1001}\n')
    f.write('do\n')
    f.write('   sleep 1\n')
    f.write('   srun -n1 --exclusive python parallel.py $i &\n')
    f.write('done\n')
    f.write('wait')
    f.close()

    # Make parallel file:
    write_parallel(1)

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
