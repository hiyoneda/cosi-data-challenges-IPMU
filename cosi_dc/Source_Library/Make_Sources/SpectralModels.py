"""
A collection of spectral models

"""
import numpy
import math
import code
import scipy.integrate

class Band(object):
	"""
	The Band model (Band et al. 1993)
	
	Usage:
	aBand = SpectralModels.Band(amplitude=1, E_peak=150, alpha=-1, beta=-2.2)

	Available Methods:
		PhotonSpectrum(Energy)				:		Return the photon spectrum in units of photons cm^-2 s^-1 keV^-1
		PhotonFlux(lower=50, upper=300)		:		Return the integrated photon flux from the lower to upper energy range in units of photons cm^-2 s^-1
		kCorrection(z,lower=50, upper=300)	:		Return the k-correction for the Flux in observed energy range translated into the source frame
	"""
	
	# Define default spectral properties
#	amplitude = 1
#	E_peak=150
#	alpha=-1
#	beta=-2.2
#	Energy = numpy.arange(1000000)/10.0
	
	def __init__(self, amplitude=1, E_peak=150, alpha=-1, beta=-2.2):
	
		self.amplitude = amplitude		# photon/cm^2/s/keV
		self.E_peak = E_peak			# keV
		self.alpha = alpha
		self.beta = beta
		
	def PhotonSpectrum(self, Energy=numpy.arange(10000)):
		                   
		print('Resulting spectrum as units of photons cm^-2 s^-1 keV^-1')
		# Produce a photon spectrum in photons cm^-2 s^-1 keV^-1

		E0 = self.E_peak / (2.0 + self.alpha)
        
		# Energy should be in keV

		Photons = numpy.arange(len(Energy))/1.0
		dpde    = numpy.arange(len(Energy))/1.0
	
		i = numpy.where(Energy < (self.alpha-self.beta) * E0)
		j = numpy.where(Energy >= (self.alpha-self.beta) * E0)

		if (numpy.sum(i) > 0):
		    Photons[i] = self.amplitude * (Energy[i]/100.)**self.alpha * numpy.exp(-1*Energy[i] / E0)
		    dpde[i] = Photons[i] * (self.alpha/Energy[i] - 1/E0)

		if (numpy.sum(j) > 0):
		    Photons[j] = self.amplitude * ( (self.alpha-self.beta) *  E0 / 100.)**(self.alpha-self.beta) * numpy.exp(self.beta-self.alpha) * (Energy[j]/100.)**self.beta
		    dpde[j] = Photons[j] * (self.beta/Energy[j])

		    slope = dpde * Energy / Photons

		return Energy, Photons
		
