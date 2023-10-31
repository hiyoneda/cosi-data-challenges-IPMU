#PBS -N array
#PBS -l select=1:ncpus=1:mem=15gb:interconnect=1g,walltime=25:00:00
#PBS -J 0-100

#Need to delay job start times by random number to prevent overloading system:
sleep `expr $RANDOM % 60`

#The MEGAlib environment first needs to be sourced:
cd $tmp/zfs/astrohe/Software
source COSIMain_u2.sh

#Change to home directory and run job
cd $PBS_O_WORKDIR
scp run_sims.py inputs.yaml Simulations/sim_$PBS_ARRAY_INDEX
cd Simulations/sim_$PBS_ARRAY_INDEX
python run_sims.py
