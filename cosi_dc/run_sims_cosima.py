# Imports:
from cosi_dc.pipeline.run_dc import RunDataChallenge

# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

# Generate tra file for simulation challenge:

instance.define_sim()
instance.run_cosima()
instance.check_cosima_parallel() # please comment out if the simulation is performed with a single core. 

#instance.run_nuclearizer() # it will not be used in DC2.

# In DC2, the simulations below must be performed with the megalib branch dee2022.
#instance.run_revan()
#instance.check_revan_parallel()
#instance.run_mimrec(extract_root=True)
#instance.clear_unessential_data()
