# Imports:
import numpy as np
import pandas as pd
import os
import crab
import cenA
import vela
import cygX1

# Source energy range for data challenge 1: 100 keV - 10 MeV 
# Note: COSI range: 0.2 - 5 MeV 
# Include padding above and below to account for energy dispersion.
power_low = 2 # 100 keV
power_high = np.log10(1e4) # 10 MeV
energy_range = np.logspace(power_low,power_high,50) # keV
elow = 10**power_low
ehigh = 10**power_high

# Function to make spectrum files:
def make_spec_file(src_name, src_energy, src_flux, intg):

    '''
    Write Cosima input file.

    src_name: name of source

    src_energy: an array of the energy range over which the 
    SED is defined. Units of keV. 

    src_flux: an array of dN/dE corresponding to src_energy. 
    Units of ph/cm^2/s/keV
    
    '''
    
    # Setup directory and file:
    this_name = src_name
    this_dir = "../%s" %this_name
    this_spec = os.path.join(this_dir,this_name + "_spec.dat")
    if os.path.isdir(this_dir) == False:
        os.system("mkdir %s" %this_dir)

    # Write spectrum file:
    f = open(this_spec,"w")
    f.write("#Format: <DP> <Energy in keV> <Spectrum in ph cm^-2 s^-1 keV^-1>\n")
    f.write("#flux (%s - %s keV): %s ph/cm^2/s\n" %(str(min(src_energy)),str(max(src_energy)),str(intg)))
    f.write("\n\nIP LINLIN\n\n")
    d = {"name":["DP"]*len(src_energy),"energy[keV]":src_energy,"photons[ph/cm^2/s/keV]":src_flux}
    df = pd.DataFrame(data=d, columns=["name","energy[keV]","photons[ph/cm^2/s/keV]"])
    df.to_csv(f,index=False, float_format='%10.5e',sep="\t",header=False)

    f.close()

    return

def update_src_file(src_name, intg):

    """
    Updates flux in .source file based on integration 
    over specified energy range.
    """

    # Get src file:
    this_name = src_name
    this_dir = "../%s" %this_name
    this_file = os.path.join(this_dir,this_name + ".source")

    # Open file for reading:
    f = open(this_file, "r")
    all_lines = f.readlines()
    
    # Open new file for writting:
    g = open(this_file, "w")

    for line in all_lines:

        split = line.split()

        if len(split) == 0:
            g.write(line)

        elif "Flux" in split[0]:
            new_line = line.replace(split[1],str(intg))
            g.write(new_line)

        else:
            g.write(line)

    g.close()

    return

#######################
# Define sources below:

# Crab:
src_name, photons, intg = crab.crab_flux(energy_range, elow, ehigh)
make_spec_file(src_name, energy_range, photons, intg)
update_src_file(src_name, intg)

# CenA
src_name, photons, intg = cenA.cenA_flux(energy_range, elow, ehigh)
make_spec_file(src_name, energy_range, photons, intg)
update_src_file(src_name, intg)

# Vela:
src_name, photons, intg = vela.vela_flux(energy_range, elow, ehigh)
make_spec_file(src_name, energy_range, photons, intg)
update_src_file(src_name, intg)

# CygX1:
src_name, photons, intg = cygX1.cygX1_flux(energy_range, elow, ehigh)
make_spec_file(src_name, energy_range, photons, intg)
update_src_file(src_name, intg)
