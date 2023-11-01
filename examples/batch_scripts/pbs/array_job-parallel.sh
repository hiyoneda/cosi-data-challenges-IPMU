#PBS -N array
#PBS -l select=1:ncpus=24:mem=46gb:interconnect=1g,walltime=200:00:00
#PBS -J 0-3404:23

#Need to delay job start times by random number to prevent overloading system:
sleep `expr $RANDOM % 120`

#The MEGAlib environment first needs to be sourced:
cd $tmp/zfs/astrohe/Software
source COSIMain_u2.sh

#Change to home directory and run job
cd $PBS_O_WORKDIR
module add gnu-parallel
parallel --delay=5 -j23 python parallel.py $PBS_ARRAY_INDEX ::: {0..22}
