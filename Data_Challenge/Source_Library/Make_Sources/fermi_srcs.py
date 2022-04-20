# Imports:
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.wcs import WCS
from matplotlib import rc
from matplotlib.cm import register_cmap,cmap_d
import numpy as np
from astropy.io import fits
import pandas as pd
from scipy.interpolate import interp1d
import sys
from scipy import integrate


class FermiSources:

    def __init__(self):

        # Upload catalog:
        input_file = "LAT_4FGL_DR2/gll_psc_v27.fit"
        hdu_cat = fits.open(input_file)
        cat_data = hdu_cat[1].data

        self.name = cat_data["Source_Name"]
        self.ts_band = cat_data["Sqrt_TS_Band"]
        self.source_class = cat_data["CLASS1"]
        self.spectral_type = cat_data["SpectrumType"]
        self.association = cat_data["ASSOC1"]
        self.K = cat_data["PL_Flux_Density"]
        self.alpha = cat_data["PL_Index"]
        self.E0 = cat_data["Pivot_Energy"]
        self.K_lp = cat_data["LP_Flux_Density"]
        self.alpha_lp = cat_data["LP_Index"]
        self.beta_lp = cat_data["LP_beta"]
        self.K_plec = cat_data["PLEC_Flux_Density"]
        self.GAMMA_plec = cat_data["PLEC_Index"]
        self.b = cat_data["PLEC_Exp_Index"]
        self.a = cat_data["PLEC_Expfactor"]
        self.ra = cat_data["RAJ2000"]
        self.dec = cat_data["DEJ2000"]
        self.glon = cat_data["GLON"]
        self.glat = cat_data["GLAT"]

        #define classes:
        self.blazar = ["BLL","bll","BCU","bcu","FSRQ","fsrq"]
        self.pulsar = ["PSR","psr"]

        #print
        #print("total number of sources: " + str(len(self.name)))
        #print

    # Define spectral models (returns dN/dE in ph/cm^2/s/MeV):

    def PowerLaw(self, Energy, norm, index, pivot_energy):
    
        spec = norm*(Energy/pivot_energy)**(-index)
 
        return spec

    def LogParabola(self, Energy, norm, index1, index2, pivot_energy):

        spec = norm*(Energy/pivot_energy)**(-index1-index2*np.log(Energy/pivot_energy))

        return spec
    
    def PLSuperExpCutoff(self, Energy, norm, index, pivot_energy, index_cut, exp_fact):

        spec = norm*(Energy/pivot_energy)**(-index)*np.exp(exp_fact*(pivot_energy**(index_cut)-Energy**(index_cut)))

        return spec

    def DoublePowerLaw(self, Energy,k,index):

        Energy = Energy / 1000.0 #convert to GeV
    
        d1 = 1.7
        d2 = 2.8
        Eb = 10**(9.25 - 4.11*index)  #GeV
    
        spec = k * ( (Energy/Eb)**d1 + (Energy/Eb)**d2 )**-1
    
        return spec

    def get_flux(self,src_name,src_energy):

        """ 
        Calculate flux from Fermi 4FGL DR2.

        Inputs:
        
        src_name: 4FGL name
        
        src_energy: input array in units of MeV

        Returns flux in units of MeV/cm^2/s
        """

        for i in range(0,len(self.name)):
    
            if self.name[i] == src_name:
            
                TS = self.ts_band[i][0]**2 + self.ts_band[i][1]**2 
                this_class = self.source_class[i]
                this_spectrum = self.spectral_type[i]
                this_association = self.association[i]
                this_l = self.glon[i]
                this_b = self.glat[i]
                this_ra = self.ra[i]
                this_dec = self.dec[i]
                
                if this_spectrum == "PowerLaw":

                    # Get scaling constant for dpl:
                    f50_pl = PowerLaw(50, self.K[i], self.alpha[i], self.E0[i])
                    f50_dpl = DoublePowerLaw(50,1,self.alpha[i])
                    k = f50_pl/f50_dpl
            
                    this_flux = self.DoublePowerLaw(src_energy,k,self.alpha[i])

                if this_spectrum == "LogParabola":

                    this_flux = self.LogParabola(src_energy,self.K_lp[i], self.alpha_lp[i], self.beta_lp[i], self.E0[i])

                if this_spectrum == "PLSuperExpCutoff":

                    this_flux = self.PLSuperExpCutoff(src_energy, self.K_plec[i], self.GAMMA_plec[i], self.E0[i], self.b[i], self.a[i])

        return this_flux
