#!/bin/bash
#SBATCH --time=0:55:00
#SBATCH -o output.%j
#SBATCH -e error.%j
#SBATCH --array=0-1000
#SBATCH --partition=packable
#SBATCH --account=j1042
#SBATCH --job-name=crab
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=3G

#Need to delay job start times by random number to prevent overloading system:
sleep `expr $RANDOM % 60`

#The MEGAlib environment first needs to be sourced:
cd /discover/nobackup/ckarwin/Software
source COSI_dee2022.sh

#Change to home directory and run job
cd $SLURM_SUBMIT_DIR
scp run_sims.py inputs.yaml Simulations/sim_$SLURM_ARRAY_TASK_ID
cd Simulations/sim_$SLURM_ARRAY_TASK_ID
python run_sims.py
