2023/May/16 Thomas Siegert
This is the description of the source model for diffuse 26Al line emission in the Galaxy at 1808.63 keV

There are two realisations from the same doubly exponential disk model.

The three-dimensional model is

rho(R,z,phi) = L / (4 * pi * Re^2 * ze) * exp(-R/Re) * exp(-|z|/ze),

where L is the total luminosity of 26Al in the Galaxy, i.e. L = M/m * p/tau with

m = 26 u as the atomic mass of 26Al nuclei, p = 0.9976 is the branching ratio to emit a photon, and
tau = 1.05 Myr is the lifetime of 26Al. This gives a quasi-persistent luminosity for a "living"
26Al mass M.

Re and ze are the scale radius and scale height, respectively.

R is the radial coordinate, i.e. R = sqrt((x-x0)^2 + (y-y0)^2), and z is the vertical coordinate, z = z' - z0.
x0 = 8.178, y0 = 0, and z0 = -0.019 are the coordinates of the Galactic centre seen from Earth.

All distance / size units are in kpc.

The line of sight integration is performed so that the flux per pixel (here: cartesian pixel grid with 3 deg
resolution) is in units of ph / cm2 / s / sr.


The two models are
Model 1:
M = 3 Msol -> L = 4.162e42 ph/s -> F = 1.278e-3 ph / cm2 / s
Re = 5.0
ze = 0.2
filenames: COSI_DC2_26Al_R5000_z0200_M30_3deg

Model 2:
M = 6 Msol -> L = 8.324e42 ph/s -> F = 1.800e-3 ph / cm2 / s
Re = 5.0
ze = 1.0
filenames: COSI_DC2_26Al_R5000_z1000_M60_3deg


The two model with 10 times the ejecta mass, which will result in 10 times the flux:
Model 1x10:
M = 30 Msol -> L = 4.162e43 ph/s -> F = 1.278e-2 ph / cm2 / s
Re = 5.0
ze = 0.2
filenames: COSI_DC2_26Al_R5000_z0200_M30_3deg_10xflux

Model 2x10:
M = 60 Msol -> L = 8.324e43 ph/s -> F = 1.800e-2 ph / cm2 / s
Re = 5.0
ze = 1.0
filenames: COSI_DC2_26Al_R5000_z1000_M60_3deg_10xflux



Goals: Distinction between the two models of roughly equal flux.
Can we measure the scale heigt and radius in projected (Galactic) coordinates,
and can we do a profile likelihood with different 3D models to recover the input scale dimensions?
What does the reconstructed image look like, and can we determine the scale dimensions from a fit to the reconstructed image?


Files:
The .dat files for the input with cosima are created from the corresponding fits files, which also include information about
the images in the fits header.
PDF files are also created to check what the actual image should look like.
