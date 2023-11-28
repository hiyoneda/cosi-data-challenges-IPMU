DC2 activation sims:

More details regarding the DC2 background sims are available in the cosi-data-challenge-2 github repository. Here we give a brief summary. 

For DC2 we simulated 3 months of backgrounds. This includes a time dependence of the particle flux due to the changing geomagnetic cutoff with the instrument's position in the orbit. To accomplish the time dependence the simulations use both an orientation file and a light curve file.  

All source files for DC are available in the DC2 source library:
https://github.com/cositools/cosi-data-challenges/tree/main/cosi_dc/Source_Library/DC2/backgrounds
They are generated using the cosi-background class. 

The simulations are very computionally intensive. To run them we split the total time into smaller time bins, and calculate all of the time bins in parallel. The most time consuming simulations were the primary protons. Specifically, step 1 of the activation sims takes the longest. We ended up using 6045 parallel CPUs. This corresponds to a time bin size of 1320 seconds (22 minutes). The average compute time for each CPU was ~5000 minutes (3.5 days). This gives a total CPU time of ~57.5 years!

Some detailed notes for running the sims:

Use parallel CPUs for step 1. 

Step 1 will generate an isotope file, to be used for the activation sims (i.e. the delayed component). It will also generate a standard sim file, which is for the prompt component. For the prompt component, you can run revan and mimrec in the normal way. For the activation component, you need to run steps 2 and 3 of the simulations first, and then revan and mimrec. 

For the step 2 source file, combine the isotope files from all parallel runs.
It's easiest to use one of the sim directories for this (e.g. sim_0).
It looks something like this:
A.IsotopeProductionFile   PrimaryProtonsIsotopes.inc1.dat
A.IsotopeProductionFile  ../../sim_1/Output/PrimaryProtonsIsotopes.inc1.dat
A.IsotopeProductionFile  ../../sim_2/Output/PrimaryProtonsIsotopes.inc1.dat
.
.
.

You can then run step 2 in the same sim_0 directory. It's best to run this from the command line. It shouldn't take very long -- less than an hour. If it's running for a very long time, there might be a problem. We found that there are some bugs in geant4 (v10.3), where certain isotopes will get stuck, and the calculation will never finish. This happened for the isotope Re162 in the alpha sims. Such isotopes can be skipped by adding them to the geant4 black list.

For step 2, set the irradiation time in the source file to your preference. We use 1 yr for DC2. This means that our background estimates are for an irradiation time of 1 year, based on the isotopes that were created after an exposure time of 3 months.  

Step 2 will generate the activation file. This can then be used as the source file for all parallel runs. The 'TT' keyword in the activation file does not need to be modified.  

Step 3 can be ran in parallel. 
