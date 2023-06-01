# Imports:
from cosi_dc.pipeline.calc_aeff import CalcAeff
import sys,os

def main(cmd_line):
    
    # Energy is passed from command line:
    energy = cmd_line[1]

    # Define instance with input parameter card:
    instance = CalcAeff("inputs.yaml")

    # Generate tra file and calculate Aeff from mono-energetic sims:
    instance.define_aeff_sim(energy)
    instance.run_cosima()
    instance.run_nuclearizer()
    instance.run_revan()
    instance.run_mimrec(extract_root=True,energy=float(energy))
    instance.aeff_from_mono_sims("Output/extracted_spectrum.dat",float(energy))

########################
if __name__=="__main__":
        main(sys.argv)
