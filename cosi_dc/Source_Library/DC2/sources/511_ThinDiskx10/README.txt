May 17th, 2023 - Carolyn Kierans

This is the description of the source model for the 511 keV positron annihilation emission in the Galaxy for DC2

Spatial: Simple Gaussian spatial models with a thin or thick disk. The bulge is based off of the model in Skinner et al. 2014 (and used in Siegert et al. 2016) and includes a narrow and broad buldge, and a central point source. The disk descriptions follow Skinner for the thin disk (3 deg scale height) and Siegert for the thick disk (10.5 deg scale height)

Spectral: Each spatial component has two spectral components. 

1) A line at 511 keV. This has a 2 keV FWHM width for the bulge components, and 3 keV FWHM for the disk emission.

2) the orthopositrium (OPs) continuum emission (as described by Ore 1949). The spectral shape of the OPs continuum is included in the OPsSpectrum.dat file and shown in ops_spectrum.pdf.

The relative fluxes of the OPs and 511 are scale such that the positronium fraction for the disk is 85% and the fraction for the bulge is 95%

Both models are included at 1x and 10x nominal flux 

Goals: 
1) Make full sky image of 511 keV (image deconvolution)
2) Determine scale height of disk emission (model fitting)
3) Extract the spectra of the bulge emission

