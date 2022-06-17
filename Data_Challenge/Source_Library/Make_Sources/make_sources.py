# Imports:
import numpy as np
from SpectralModels import Band
from scipy.interpolate import interp1d
from scipy import integrate
import pandas as pd
import os
import matplotlib.pyplot as plt
from fermi_srcs import FermiSources

# Source energy range for main data challenge: 8 keV - 50 MeV.
# Source energy range for preliminary data challenge: 100 keV - 10 MeV 
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

    src_energy: an array of the energy range over which the SED is defined. Units of keV. 

    src_flux: an array of dN/dE corresponding to src_energy. Units of ph/cm^2/s/keV
    
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

# Define sources below:

# Open master source list:
f = open("../master_source_list.txt","w")
f.write("[\n")

##################
#crab:
src_name = "crab"
src_type = "ps"
gal_l = 184.56
gal_b = -5.78

#spectrum:
band = Band(amplitude=7.52e-4,E_peak=5.31,alpha=-1.99,beta=-2.32) #note: E_0 = 531 keV, which is the break energy, E_0 = E_peak/(2-alpha)
crab_energy,crab_photons = band.PhotonSpectrum(Energy=energy_range)
crab_func = interp1d(crab_energy,crab_photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#sanity checks on integrated flux:
crab_intg1 = integrate.quad(crab_func,325,480)
crab_intg2 = integrate.quad(crab_func,298.5984,515.978)
print()
print("Crab flux between 325 - 480 keV [ph/cm^2/s]: " + str(crab_intg1[0]))
print("Crab flux between 298.5984 - 515.978 keV [ph/cm^2/s]: " + str(crab_intg2[0]))
print()

#integrated flux for source file:
intg = integrate.quad(crab_func,elow,ehigh)[0]
intg = float("{:.6f}".format(intg))
print()
print("Crab flux between %s keV - %s keV [ph/cm^2/s]: " %(str(elow),str(ehigh)) + str(intg))
print()

make_spec_file(src_name, energy_range, crab_photons, intg)
f.write(str([src_name,src_type,gal_b,gal_l,intg]) + ",\n")
##################

##################
#crab2 (for testing):
src_name = "crab2"
src_type = "ps"
gal_l = 270.0
gal_b = 10.0

#spectrum:
band = Band(amplitude=7.52e-4,E_peak=5.31,alpha=-1.99,beta=-2.32) #note: E_0 = 531 keV, which is the break energy, E_0 = E_peak/(2-alpha)
crab_energy,crab_photons = band.PhotonSpectrum(Energy=energy_range)
crab_func = interp1d(crab_energy,crab_photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#integrated flux for source file:
intg = integrate.quad(crab_func,elow,ehigh)[0]
intg = float("{:.6f}".format(intg))
print()
print("Crab2 flux between %s keV - %s keV [ph/cm^2/s]: " %(str(elow),str(ehigh)) + str(intg))
print()

make_spec_file(src_name, energy_range, crab_photons, intg)
f.write(str([src_name,src_type,gal_b,gal_l,intg]) + ",\n")
##################


##################
#cen A (from HESS+LAT 2018)
src_name = "cenA"
src_type = "ps"
gal_l = 309.516
gal_b = 19.417

#spectrum:
df = pd.read_csv("cenA.txt",delim_whitespace=True)
energy = df["energy[eV]"]*(1.0/1000.0) #keV
flux = df["flux[erg/cm^2/s]"] #erg/cm^2/s
flux = flux*6.242e8 #keV/cm^2/s
func = interp1d(energy,flux,kind="linear",bounds_error=False,fill_value="extrapolate")
photons = func(energy_range)/energy_range**2 #ph/cm^2/s/keV
func2 = interp1d(energy_range,photons,kind="linear",bounds_error=False,fill_value="extrapolate")
#photons = flux/(energy**2)
#func = interp1d(energy,photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#integrated flux for source file:
intg = integrate.quad(func2,elow,ehigh)[0]
intg = float("{:.6f}".format(intg))
print()
print("cenA flux between %s keV - %s keV [ph/cm^2/s]: " %(str(elow),str(ehigh)) + str(intg))
print()

#plot for sanity check:
#plt.loglog(energy_range,energy_range**2 * photons)
#plt.show()
#plt.close()

make_spec_file(src_name, energy_range, photons, intg)
f.write(str([src_name,src_type,gal_b,gal_l,intg]) + ",\n")
##################

##################
#vela
src_name = "vela"
src_type = "ps"
gal_l = 263.552
gal_b = -2.787

#spectrum:
df = pd.read_csv("vela.txt",delim_whitespace=True)
energy = df["energy[eV]"]*(1.0/1000.0) #keV
flux = df["flux[erg/cm^2/s]"] #erg/cm^2/s
flux = flux*6.242e8 #keV/cm^2/s
photons = flux/(energy**2)
func = interp1d(energy,photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#integrated flux for source file:
##intg = integrate.quad(func,elow,ehigh)[0]
#intg = float("{:.6f}".format(intg))
#print()
#print("vela flux between %s keV - %s keV [ph/cm^2/s]: " %(str(elow),str(ehigh)) + str(intg))
#print()

#plot for sanity check:
#plt.loglog(df["energy[eV]"],df["flux[erg/cm^2/s]"])
#plt.show()

#make_spec_file(this_name, energy_range, func(energy_range), intg)

# Extrapolate from LAT 4FGL 
fermi_instance = FermiSources()
energy_range_MeV = energy_range/1.0e3
lat_flux = fermi_instance.get_flux("4FGL J0835.3-4510",energy_range_MeV) # pulsar, ph/cm^2/s/MeV
lat_flux = lat_flux / 1000.0 # ph/cm^2/s/keV

#integrated flux for source file:
func = interp1d(energy_range,lat_flux,kind="linear",bounds_error=False,fill_value="extrapolate")
intg = integrate.quad(func,elow,ehigh)[0]
intg = float("{:.6f}".format(intg))
print()
print("vela flux between %s keV - %s keV [ph/cm^2/s]: " %(str(elow),str(ehigh)) + str(intg))
print()

make_spec_file(src_name, energy_range, lat_flux, intg)
f.write(str([src_name,src_type,gal_b,gal_l,intg]) + ",\n")
##################

##################
#cyg X-1:
src_name = "cygX1"
src_type = "ps"
gal_l = 71.33496
gal_b = 3.066917

df = pd.read_csv("Cyg_X1.dat",skiprows=1,delim_whitespace=True)
energy = df["energy[eV]"]*(1.0/1000.0) #keV
flux = df["flux[erg/cm^2/s]"] #erg/cm^2/s
flux = flux*6.242e8 #keV/cm^2/s
func = interp1d(energy,flux,kind="linear",bounds_error=False,fill_value="extrapolate")
photons = func(energy_range)/(energy_range**2) #ph/cm^2/s/keV
func2 = interp1d(energy_range,photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#integrated flux for source file:
intg = integrate.quad(func2,elow,ehigh)[0]
intg = float("{:.6f}".format(intg))
print()
print("Cyg X-1 flux between %s keV - %s keV [ph/cm^2/s]: " %(str(elow),str(ehigh)) + str(intg))
print()

#plot for sanity check:
#plt.loglog(energy_range,energy_range**2 * photons)
#plt.show()
#plt.close()

make_spec_file(src_name, energy_range, photons, intg)
f.write(str([src_name,src_type,gal_b,gal_l,intg]) + ",\n")
###############

###############
# Data challenge 1:
src_name = "DataChallenge1"
src_type = "include"
src_list = ['crab', 'cenA', 'vela', 'cygX1']
f.write(str([src_name,src_type,src_list]) + ",\n")

##############
# Ling BG:
src_list = ['LingBG','LingBG']
f.write(str(src_list) + ",\n")

##############
# Al26:
src_list = ['Al26','diffuse','AllSky_Al26_NormInnerGalaxyDiehl_DIRBE240um.dat']
f.write(str(src_list) + ",\n")

##############
# Al26_10xFlux:
src_list = ['Al26_10xFlux','diffuse','scaled_10x_AllSky_Al26_NormInnerGalaxyDiehl_DIRBE240um.dat']
f.write(str(src_list) + ",\n")

##############
# GalIC:
src_list = ['GalIC','diffuse','GalacticDiffuse_IC.dat']
f.write(str(src_list) + ",\n")

##############
# GalBrem:
src_list = ['GalBrem','diffuse','GalacticDiffuse_Brem.dat']
f.write(str(src_list) + ",\n")

##############
# GC 511A
src_list = ['GC511A', 'GC511']
f.write(str(src_list) + ",\n")

##############
# GC 511A_10xFlux
src_list = ['GC511A_10xFlux', 'GC511']
f.write(str(src_list) + ",\n")

##############
# GC 511B
src_list = ['GC511B', 'GC511']
f.write(str(src_list) + "\n")

# Close master source list:
f.write("]")
f.close()

# Run setup:
home = os.getcwd()
os.chdir("../../Setup/")
os.system("python setup.py")
os.chdir(home)
