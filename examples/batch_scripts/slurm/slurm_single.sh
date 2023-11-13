#!/bin/bash
#SBATCH --time=0:55:00
#SBATCH -o output.%j
#SBATCH -e error.%j
#SBATCH --qos=debug
#SBATCH --account=j1042
#SBATCH --job-name=crab
#SBATCH --ntasks=1

#The MEGAlib environment first needs to be sourced:
cd /discover/nobackup/ckarwin/Software
source COSI_dee2022.sh

cd $SLURM_SUBMIT_DIR
python run_sims.py
