# Imports:
from cosi_dc.pipeline.run_dc import RunDataChallenge

# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

# Generate tra file for simulation challenge:
instance.define_sim()
instance.run_cosima()
instance.check_cosima_parallel()
instance.run_nuclearizer()
instance.run_revan()
instance.check_revan_parallel()
instance.run_mimrec(extract_root=True)
instance.plot_spectrum()
instance.plot_lc()
instance.plot_image()
instance.clear_unessential_data()
