# Imports:
from SpectralModels import Band
from scipy.interpolate import interp1d
from scipy import integrate

def crab_flux(energy_range, elow, ehigh):

    """crab flux"""

    src_name = "crab"
    src_type = "ps"
    gal_l = 184.56
    gal_b = -5.78

    # Spectrum:
    band = Band(amplitude=7.52e-4,E_peak=5.31,alpha=-1.99,beta=-2.32) #note: E_0 = 531 keV, which is the break energy, E_0 = E_peak/(2-alpha)
    crab_energy,crab_photons = band.PhotonSpectrum(Energy=energy_range)
    crab_func = interp1d(crab_energy,crab_photons,kind="linear",bounds_error=False,fill_value="extrapolate")

    # Sanity checks on integrated flux:
    crab_intg1 = integrate.quad(crab_func,325,480)
    crab_intg2 = integrate.quad(crab_func,298.5984,515.978)
    print()
    print("Crab flux between 325 - 480 keV [ph/cm^2/s]: " + str(crab_intg1[0]))
    print("Crab flux between 298.5984 - 515.978 keV [ph/cm^2/s]: " + str(crab_intg2[0]))
    print()

    # Integrated flux for source file:
    intg = integrate.quad(crab_func,elow,ehigh)[0]
    intg = float("{:.6f}".format(intg))
    print()
    print("Crab flux between %s keV - %s keV [ph/cm^2/s]: " %(str(elow),str(ehigh)) + str(intg))
    print()

    return src_name, crab_photons, intg

