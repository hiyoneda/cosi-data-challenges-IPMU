# Imports:
from cosi_dc.pipeline.run_dc import RunDataChallenge

# Define instance with input parameter card:
instance = RunDataChallenge("inputs.yaml")

instance.check_cosima_parallel()
instance.check_revan_parallel()
instance.clear_unessential_data()
