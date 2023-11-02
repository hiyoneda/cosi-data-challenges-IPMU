# Imports:
from cosi_dc.pipeline.run_dc import RunDataChallenge

# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

instance.geo_file = '/lustre/work/COSI/software/cosi-data-challenges-IPMU/cosi_dc/Input_Files/Geometry_Files/massmodel-cosi-smex-v12/COSISMEX.O64.geo.setup' # do not change this. In DC2, the geometry file for the dee2022 simulation has to be this, not the same as the cosima simulation.

# Generate tra file for simulation challenge:

# In DC2, the simulations below must be performed with the main megalib branch.
#instance.define_sim()
#instance.run_cosima()
#instance.check_cosima_parallel()

#instance.run_nuclearizer() # it will not be used in DC2.

instance.run_revan()
instance.check_revan_parallel() # please comment out if the simulation is performed with a single core. 
instance.run_mimrec(extract_root=True)
instance.clear_unessential_data() # please comment out if the simulation is performed with a single core. 
