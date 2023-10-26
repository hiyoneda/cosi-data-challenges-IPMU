#!/bin/bash
#SBATCH --time=5:00:00
#SBATCH -o output.%j
#SBATCH -e error.%j
#SBATCH --qos=allnccs
#SBATCH --account=j1042
#SBATCH --job-name=CosmicPhotons
#SBATCH --ntasks=3022
#SBATCH --mem-per-cpu=2G

#The MEGAlib environment first needs to be sourced:
cd /discover/nobackup/ckarwin/Software
source COSI.sh

cd $SLURM_SUBMIT_DIR

for i in {0..3023}
do
	sleep 1
	srun -n1 --exclusive python parallel.py $i &
done
wait
