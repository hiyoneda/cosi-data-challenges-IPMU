#!/bin/bash
#SBATCH --time=0:55:00
#SBATCH -o output.%j
#SBATCH -e error.%j
#SBATCH --qos=debug
#SBATCH --account=j1042
#SBATCH --job-name=511_thick10x
#SBATCH --ntasks=1000
#SBATCH --mem-per-cpu=3G

#The MEGAlib environment first needs to be sourced:
cd /discover/nobackup/ckarwin/Software
source COSI_dee2022.sh

cd $SLURM_SUBMIT_DIR

for i in {0..1001}
do
   sleep 1
   srun -n1 --exclusive python parallel.py $i &
done
wait
