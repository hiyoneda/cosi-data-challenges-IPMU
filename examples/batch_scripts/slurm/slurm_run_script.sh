#!/bin/bash

#SBATCH --job-name=AlbedoPhoton
#SBATCH --output=/lustre/project/nhr-cosi/MC/DC2/OUTPUT/AlbedoPhoton/Simulations/sim_%a/TestMogon_%A_%a.out # redirecting stdout
#SBATCH --error=/lustre/project/nhr-cosi/MC/DC2/OUTPUT/AlbedoPhoton/Simulations/sim_%a/TestMogon_%A_%a.err  # redirecting stderr
#SBATCH --array=0-31
#SBATCH --time=05:30:00
#SBATCH --partition=smp        
#SBATCH --ntasks=1                  # number of tasks per array job
#SBATCH --mem-per-cpu=3000M
#SBATCh --hint=nomultithread

######################
# Begin work section #
######################

#source MEGAlib main branch
source /lustre/project/nhr-cosi/software/MEGAlib/new-source-megalib.sh


#copy source files in the run directory
cp /lustre/project/nhr-cosi/MC/DC2/INPUT/source/AlbedoPhotonsTuerlerMizunoAbdo.beam.dat /lustre/project/nhr-cosi/MC/DC2/OUTPUT/AlbedoPhoton/Simulations/sim_$SLURM_ARRAY_TASK_ID
cp /lustre/project/nhr-cosi/MC/DC2/INPUT/source/AlbedoPhotons_Spec_550.0km_0.0deg_10.000cutoff_650.0solarmod.dat /lustre/project/nhr-cosi/MC/DC2/OUTPUT/AlbedoPhoton/Simulations/sim_$SLURM_ARRAY_TASK_ID
cp /lustre/project/nhr-cosi/MC/DC2/INPUT/source/AlbedoPhotons.source /lustre/project/nhr-cosi/MC/DC2/OUTPUT/AlbedoPhoton/Simulations/sim_$SLURM_ARRAY_TASK_ID

#go to the run directory 
cd /lustre/project/nhr-cosi/MC/DC2/OUTPUT/AlbedoPhoton/Simulations/sim_$SLURM_ARRAY_TASK_ID

#run cosima
cosima -z -v 0  AlbedoPhotons.source

# source MEGAlib dee2022
source /lustre/project/nhr-cosi/software/MEGAlib_de2022/bin/source-megalib.sh

#run revan
revan -g /lustre/project/nhr-cosi/MC/DC2/INPUT/massmodel-cosi-smex-v12/COSISMEX.O64.geo.setup -c /lustre/project/nhr-cosi/MC/DC2/INPUT/configuration/SMEXv12.Continuum.HEALPixO3.binnedimaging.revan.cfg -f AlbedoPhotons.inc1.id1.sim.gz -n -a

#run mimrec
mimrec -g /lustre/project/nhr-cosi/MC/DC2/INPUT/massmodel-cosi-smex-v12/COSISMEX.O64.geo.setup -c /lustre/project/nhr-cosi/MC/DC2/INPUT/configuration/SMEXv12.Continuum.HEALPixO3.binnedimaging.mimrec.cfg -x -f AlbedoPhotons.inc1.id1.tra.gz -o AlbedoPhotons.inc1.id1.extracted.tra.gz -n
