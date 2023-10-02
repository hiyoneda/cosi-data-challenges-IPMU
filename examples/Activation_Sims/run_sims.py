# Imports:
from cosi_dc.pipeline.run_dc import RunDataChallenge

### INTRO ###
# Run activation sims using run_type = array_jobs-parallel.
# This allowed us to simulate 6 months of activation for DC2!

### SIMULATION SETUP ###
# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

# Generate source file:
# Here we will specify that we are using an external source.
# The source files need to be generated using the cosi-background class,
# and copied to the Source directory (in the run directory). 
# For steps 1 and 3, set the exposure time to the max time in the ori/LC files. 
# For step 2, set the irradiation time to your preference (we use 1 yr for DC2).
# The genaric name for the LC is lightcurve.dat,
# and the genaric name for the ori file is GalacticScan.ori. 
#instance.define_sim(external_src=True)

### COSIMA ###
# run cosima, steps 1-3:
# You must run each step one at a time. 
# This will be managed using array_jobs.sh, 
# which utilizes a combination of job arrays (i.e. MPI) and gnu_parallel.
# Run as many jobs in parallel as possible, based on the available resources, 
# but do not give multiple MEGAlib commands within a single run, 
# otherwise the system will be overloaded and jobs won't finish properly.
# Make sure to check the output at each stage after all jobs finish, 
# to verify that everying is running ok. 
# The parameter get_cpu in check cosima_parallel must be set to False for step 2. 
# Make sure to mofify the isotope sim time after step 1 if using an ori file!
instance.name = "PrimaryProtons" # Name of component
instance.run_cosima(output_name="cosima_step1")
instance.check_cosima_parallel(input_file="cosima_step1_terminal_output.txt", get_cpu=True, show_plot=False)
instance.modify_isotope_sim_time("PrimaryProtonsIsotopes.inc1.dat",45.0)

# If you need to modify times in the sim file in order to match the decay component with the orientation times:
# This is only needed for step 3. 
constant = instance.get_time_constant("GalacticScan.ori")
instance.modify_sim_times("PrimaryProtons_Decay.inc1.id1.sim.gz",constant)

### REVAN ###
# run revan for both prompt and activation components:

# Need to specify different geo file for revan (for DC2):
revan_geo = "/zfs/astrohe/ckarwin/My_Class_Library/COSI/Data_Challenge/Input_Files/Geometry_Files/DC2/massmodel-cosi-smex-v12/COSISMEX.O64.geo.setup"

# For prompt:
instance.name = "PrimaryProtons"
instance.run_revan(geo_file=revan_geo, output_name="revan_prompt_terminal_output")
instance.check_revan_parallel(input_file="revan_prompt_terminal_output.txt",savefile="revan_prompt_events")

# For activation:
instance.name = "PrimaryProtons_Decay"
instance.run_revan(geo_file=revan_geo, output_name="revan_decay_terminal_output")
instance.check_revan_parallel(input_file="revan_decay_terminal_output.txt",savefile="revan_decay_events")

### MIMREC ###
# Run mimrec:
instance.run_mimrec(extract_root=True)
instance.clear_unessent:ial_data()
