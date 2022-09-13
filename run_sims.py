# Imports:
from run_data_challenge_module import RunDataChallenge

# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

# Generate tra file for simulation challenge:
instance.define_sim()
instance.run_cosima()
instance.run_nuclearizer()
instance.run_revan()
instance.run_mimrec(extract_root=True)
instance.clear_unessential_data()
