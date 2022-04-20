# Imports:
from run_data_challenge_module import RunDataChallenge
import time

start_time = time.time()

# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

# Run help function:
#help(instance)

# Full paths to configuration files:
revan_config = "/zfs/astrohe/Software/COSI/Nuclearizer/resource/examples/crabsanitycheck/Crab.revan.cfg"
nuc_config = "/zfs/astrohe/Software/COSI/Nuclearizer/resource/dee/ConfigurationFile_CliosFinalDEE.cfg"
mimrec_config = "/zfs/astrohe/ckarwin/My_Class_Library/COSI/Data_Challenge/Input_Files/Configuration_Files/Data_Challenges/DC1_preliminary_mimrec.cfg"

# Generate tra file for simulation challenge:
instance.define_sim()
instance.run_cosima(432020)
instance.run_nuclearizer(nuc_config)
instance.run_revan(revan_config)
#instance.run_mimrec(mimrec_config,extract_root=True)

# Save simulation time:
total_time = time.time() - start_time
f = open("run_time.txt","w")
f.write(str(total_time))
f.close()
