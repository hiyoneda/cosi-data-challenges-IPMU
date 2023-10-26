import time
import os,sys
import numpy as np

run_list = np.arange(1664,6058,101)

for i in run_list:

    low = i
    high = i + 100
    print()
    print("low: " + str(low))
    print("high: " + str(high))
    print()

    f = open("seq.sh","w")
    f.write("#PBS -N high_%s\n" %str(high))
    f.write("#PBS -l select=13:ncpus=8:mem=31gb:interconnect=1g,walltime=200:00:00\n\n")


    f.write("#The MEGAlib environment first needs to be sourced:\n")
    f.write("cd $tmp/zfs/astrohe/Software\n")
    f.write("source COSIMain_u2.sh\n\n")

    f.write("#Change to home directory and run job\n")
    f.write("module add gnu-parallel\n")
    f.write("module load anaconda3/2022.05-gcc/9.5.0\n")
    f.write("cd $PBS_O_WORKDIR\n")
    f.write("cat $PBS_NODEFILE > nodes.txt\n")
    f.write("seq %s %s | parallel --delay=3 --sshloginfile nodes.txt -j8 'source $tmp/zfs/astrohe/Software/COSIMain_u2.sh; cd /scratch1/ckarwin/DC2/Background/Run_6;  python parallel.py {}'\n" %(str(low),str(high)))
    f.write("rm nodes.txt")
    f.close()

    os.system("qsub seq.sh")
    
    # Sleep for amount of time taken for all CPUs to start:
    time.sleep(350)
    
    # Test the all CPUs are running:
    print("Testing that all CPUs are running...")
    count = 0
    for j in range(low,high):
        this_file = "Simulations/sim_%s/Output/PrimaryProtons.inc1.id1.sim.gz" %str(j)
        test = os.path.isfile(this_file)
        if test == False:
            count += 1
            print(j)
    if count == 0:
        print("all CPUs running!")

