# Imports:
from run_data_challenge_module import RunDataChallenge
import time

start_time = time.time()

# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

# Run help function:
#help(instance)

# Full paths to configuration files:
revan_config = "full/path/ContinuumResponse_cori_v1v2_nuclearizer_12Det_200812_imaging_atmos_9Det_6deg_10ebins.revan.cfg"
nuc_config = "full/path/ContinuumResponse_cori_v1v2.nuclearizer.cfg"
mimrec_config = "full/path/ContinuumResponse_cori_v1v2_nuclearizer_12Det_200812_imaging_atmos_9Det_6deg_10ebins.mimrec.cfg"

# Generate tra file for simulation challenge:
instance.define_sim()
instance.run_cosima()
instance.run_nuclearizer(nuc_config)
instance.run_revan(revan_config)
instance.run_mimrec(mimrec_config,extract_root=True)

# Save simulation time:
total_time = time.time() - start_time
f = open("run_time.txt","w")
f.write(str(total_time))
f.close()
