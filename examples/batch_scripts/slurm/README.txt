submit_slurm.sh:
This script has bees successfully used on NASA's Discover cluster. 
It uses srun to send a single job to a single cpu. 
The script parallel.py needs to be modified to only take sys.argv[1],
i.e. remove sys.argv[2].

slurm_run_script.sh:
This script has been successfully used on MOGON (JGU Mainz).
This uses the 'smp partition', which makes things simple, 
b/c it sends each array job to its own cpu.
