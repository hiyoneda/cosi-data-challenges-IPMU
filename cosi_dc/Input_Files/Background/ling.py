#!/usr/bin/env python2
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapz,cumtrapz
from scipy.optimize import brenth

ling_energies = np.array([300.,500.,800.,1000.,2000.,4000.,5000.,6000.,8000.,10000.])
calc_energies = np.array([100.,300.,500.,800.,1000.,2000.,4000.,5000.,6000.,8000.,10000.])
R_earth = 6371.0088 #km, avg
fdensity = None
fdepth = None
fmu = None
fS0 = None
fb = None
fc = None
fp = None
H = None
fcosmicflux = None

def ling_continuum(altitude, theta, energies=calc_energies, dr = 0.1, atten_num=512): #theta is in radians, #dr is in km, energy in keV
    global fdensity,fdepth,fmu,fS0,fb,fc,fp,H
    r = np.array([0.,0.,R_earth + altitude]) #cosi position wrt earth center
    n = np.array([0.,np.sin(theta),np.cos(theta)]) #direction vector to integrate along
    nmag = 0.0

    integrand = []
    integrand_r = []

    while 1:
        mags = np.linspace(0.0,nmag,num=atten_num) #magnitudes of direction vector used to perform attenuation integral
        locs = r + np.outer(mags,n) #positions along which to perform attenuation integral
        rlocs = np.sqrt(np.sum(locs*locs,axis=1)) #radii of positions along which to perform attenuation integral
        pos = locs[-1] #position of current parcel of air
        rpos = rlocs[-1]#get radius of the position of the current air parcel
        if (rpos > H) or (rpos < R_earth): #check if we should stop
            break
        densities = fdensity(rlocs) #get densities along line for attenuation integral
        atten_integral = trapz(np.outer(fmu(energies),densities),mags*1E5,axis=1) #multiply densities by mu (mass absorption coeff) and integrate along line
        x = fdepth(rpos) #convert air parcel radius to depth x
        S = fS0(energies)*(1. + fb(energies)*x + fc(energies)*(x*x))*np.exp(-x/fp(energies)) #compute source function strength using air parcel depth
        rho = fdensity(rpos) #determine the density of the air parcel
        integrand.append(S*rho*np.exp(-atten_integral))
        integrand_r.append(nmag)
        nmag += dr

    
    return trapz(np.array(integrand),np.array(integrand_r)*1E5,axis=0)/(4.*np.pi)


def ling_cosmic(altitude, theta, energies=calc_energies, atten_num=512):
    global fdensity,fdepth,fmu,fS0,fb,fc,fp,H
    r = np.array([0.,0.,R_earth + altitude]) #cosi position wrt earth center
    n = np.array([0.,np.sin(theta),np.cos(theta)]) #direction vector to integrate along
    fdist = lambda q:np.sqrt(np.sum(np.power(r + (q*n),2.))) - H
    distance_to_top = brenth(fdist,0,2*H)
    mags = np.linspace(0.0,distance_to_top,num=atten_num)
    locs = r + np.outer(mags,n)
    rlocs = np.sqrt(np.sum(locs*locs,axis=1)) #radii of positions along which to perform attenuation integral
    atten_integral = trapz(np.outer(fmu(energies),fdensity(rlocs)),mags*1E5,axis=1)
    return fcosmicflux(energies)*np.exp(-atten_integral)

def ling_511(altitude, theta, dr = 0.1, atten_num=512): #theta is in radians, #dr is in km, energy in keV

    #the flux returned by this function is in units of photons/cm2/s/sr.  I checked the output from the code against the values in table 2 of Ling 1975,
    # and the fluxes are very close especially at the lower depth of 3.5 g/cm2.  The fluxes are close, but not as close, at 70 g/cm2.  

    global fdensity,fdepth,fmu,H
    #from ling 1977
    S0 = 2.1955E-3
    b = 0.91669
    c = 2.4522E-3
    p = 92.1
    """
    #from ling 1975
    S0 = 1.816E-2
    b = 1.26E-1
    c = 1.332E-5
    p = 103.1
    """
    energy = 511.
    mu = fmu(energy)
    r = np.array([0.,0.,R_earth + altitude]) #cosi position wrt earth center
    n = np.array([0.,np.sin(theta),np.cos(theta)]) #direction vector to integrate along
    nmag = 0.0

    integrand = []
    integrand_r = []

    while 1:
        mags = np.linspace(0.0,nmag,num=atten_num) #magnitudes of direction vector used to perform attenuation integral
        locs = r + np.outer(mags,n) #positions along which to perform attenuation integral
        rlocs = np.sqrt(np.sum(locs*locs,axis=1)) #radii of positions along which to perform attenuation integral
        pos = locs[-1] #position of current parcel of air
        rpos = rlocs[-1]#get radius of the position of the current air parcel
        if (rpos > H) or (rpos < R_earth): #check if we should stop
            break
        densities = fdensity(rlocs) #get densities along line for attenuation integral
        atten_integral = trapz(mu*densities,mags*1E5) #multiply densities by mu (mass absorption coeff) and integrate along line
        x = fdepth(rpos) #convert air parcel radius to depth x
        S = S0*(1. + b*x + c*(x*x))*np.exp(-x/p) #compute source function strength using air parcel depth
        rho = fdensity(rpos) #determine the density of the air parcel
        integrand.append(S*rho*np.exp(-atten_integral))
        integrand_r.append(nmag)
        nmag += dr

    
    return trapz(integrand,np.array(integrand_r)*1E5)/(4.*np.pi)



def load_data(nrlfile,altitudecolumn=0,densitycolumn=4):
    global fdensity,fdepth,fmu,ling_energies,fS0,fb,fc,fp,H,fcosmicflux
    nrl = np.genfromtxt(nrlfile) #first column is height in km, fifth column is mass density in g/cm3
    rnrl = nrl[:,altitudecolumn] + R_earth
    H = R_earth + nrl[-1,altitudecolumn] #top of atmos radius wrt earth center
    fdensity = interp1d(rnrl,nrl[:,densitycolumn],bounds_error=False, fill_value='extrapolate') 
    fdepth = interp1d(rnrl,cumtrapz(nrl[::-1,densitycolumn],rnrl*1E5,initial=0.0)[::-1],bounds_error=False,fill_value='extrapolate') #returns depth in g/cm2
    fS0 = interp1d(ling_energies,[6.15E-1,2.186E-1,9.3E-2,6.093E-2,1.5E-2,2.6E-3,1.415E-3,6.62E-4,2.03E-4,9.045E-5],bounds_error=False,fill_value='extrapolate')
    fb = interp1d(ling_energies,[3.347E-2,4.768E-2,4.8E-2,5.4E-2,8.0E-2,1.5E-1,1.882E-1,2.928E-1,6.519E-1,9.77E-1],bounds_error=False,fill_value='extrapolate')
    fc = interp1d(ling_energies,[-5.548E-5,-8.387E-6,-4.0E-6,-4.8E-6,-7.0E-6,-2.5E-5,-2.93E-5,-4.797E-5,-1.217E-4,-1.479E-3],bounds_error=False,fill_value='extrapolate')
    fp = interp1d(ling_energies,[174.1,121.8,113.0,110.,110.,107.0,112.,114.,108.5,134.9],bounds_error=False,fill_value='extrapolate')
    fcosmicflux = interp1d(ling_energies,[0.2,0.066,0.034,0.025,8.5E-3,2.0E-3,1.3E-3,1.0E-3,6.5E-4,4.3E-4],bounds_error=False,fill_value='extrapolate')
    #using the ling mass absorption coeffs, using other coefficients is not advised because the Ling results rely on the cross sections that they used for their data!
    #the mass abs coeff that ling uses for 511 keV is the same as 500 keV -> 12.5 g/cm2
    fmu = interp1d([300.,500.,511.,800.,1000.,2000.,4000.,5000.,6000.,8000.,10000.],1./np.array([9.5,12.5,12.5,16.0,17.5,22.8,32.6,36.9,40.1,45.6,49.9]),bounds_error=False,fill_value='extrapolate') 

if __name__ == '__main__':
    from argparse import ArgumentParser
    from multiprocessing import Pool
    p = ArgumentParser(description='Program for calculating photon backgrounds (continuum,cosmic,511) in the atmosphere using Lings 1975 semiempirical model.  This code can also be imported as a module')
    p.add_argument('altitude',type=float,help='altitude in km')
    p.add_argument('ntheta',type=int,help='number of theta (zenith angle) points to compute the model over')
    p.add_argument('nrlfile',help='nrlmsise file containing the air density vs. altitude')
    p.add_argument('--altitudecolumn',default=0,help='column of nrlmsise file corresponding to the altitude (should start from ground level ~ 0 km).  Default is 0 (first column)')
    p.add_argument('--densitycolumn',default=4,help='column of nrlmsise file corresponding to the total mass density in g/cm3.  Default is 4')
    p.add_argument('--plot',action='store_true',help='show a plot of the angular dependence of the flux at the Ling energies')
    p.add_argument('--continuum_scale',type=float,help='scale factor to scale the continuum model flux',default=1.0)
    p.add_argument('--cosmic_scale',type=float,help='scale factor to scale the cosmic model flux',default=1.0)
    p.add_argument('--five11_scale',type=float,help='scale factor to scale the 511 component',default=1.0)
    p.add_argument('--all_scale',type=float,help='scale factor to scale all components',default=1.0)
    p.add_argument('--file_name_tag',type=str,help='tag for naming the output files',default='00')
    a = p.parse_args()

    load_data(a.nrlfile,altitudecolumn=a.altitudecolumn,densitycolumn=a.densitycolumn)
    angles = np.linspace(0.,np.pi,num=a.ntheta)
    to_deg = 180./np.pi

    continuum = []
    cosmic = []
    five11 = []

    for t in angles:
        x = ling_continuum(a.altitude,t) 
        continuum.append(x)
        y = ling_cosmic(a.altitude,t)
        cosmic.append(y)
        z = ling_511(a.altitude,t)
        five11.append(z)

    continuum = np.array(continuum) * a.all_scale * a.continuum_scale
    cosmic = np.array(cosmic) * a.all_scale * a.cosmic_scale
    five11 = np.array(five11) * a.all_scale * a.five11_scale

    if a.plot:
        import matplotlib.pyplot as py
        n = 0
        py.figure(figsize=(5,9))
        for e in calc_energies:
            c = py.cm.viridis(float(n)/len(calc_energies))
            py.plot(angles*to_deg,continuum[:,n],'--',color=c)
            py.plot(angles*to_deg,cosmic[:,n] + continuum[:,n],color=c,label='%.1f keV'%(e))
            n += 1
        py.plot(angles*to_deg,five11,'k',label='511 keV')
        py.yscale('log')
        py.legend(loc='lower right',fontsize=8)
        py.xlabel('Zenith angle (degrees)')
        py.ylabel('Flux (photons/cm2/s/MeV/str)')
        py.savefig('ling_flux_vs_zenith_%.2f_km.eps' % (a.altitude))
        py.show()

    #########################continuum + cosmic###############################

    phipoints = np.array([0.0,180.0,360.])
    thetapoints = angles*to_deg
    fcont = open('ling_continuum_%.3f_km_%s.cosimadat' % (a.altitude,a.file_name_tag),'w')
    fcosm = open('ling_cosmic_%.3f_km_%s.cosimadat' % (a.altitude,a.file_name_tag),'w')
    fcont.write('IP LIN\n')
    fcosm.write('IP LIN\n')

    #write phi points
    fcont.write('PA ')
    fcosm.write('PA ')
    for phi in phipoints:
        fcont.write('%.6f ' % (phi))
        fcosm.write('%.6f ' % (phi))
    #write theta points
    fcont.write('\nTA ')
    fcosm.write('\nTA ')
    for th in thetapoints:
        fcont.write('%.6f ' % (th))
        fcosm.write('%.6f ' % (th))
    #write energy points
    fcont.write('\nEA ') 
    fcosm.write('\nEA ') 
    for en in calc_energies:
        fcont.write('%.6f ' % (en))
        fcosm.write('%.6f ' % (en))

    fcont.write('\n\n')
    fcosm.write('\n\n')

    for i in range(len(phipoints)):
        for j in range(len(thetapoints)):
            for k in range(len(calc_energies)):
                fcont.write('AP %d %d %d %.6e\n' % (i,j,k,continuum[j,k]/1000.0)) #factor of a thousand converts flux from per MeV to per keV
                fcosm.write('AP %d %d %d %.6e\n' % (i,j,k,cosmic[j,k]/1000.0)) #factor of a thousand converts flux from per MeV to per keV
    
    fcont.write('EN')
    fcosm.write('EN')
    fcont.close()
    fcosm.close()

    ########################511 line###################################

    f511 = open('ling_511_%.3f_km_%s.cosimadat' % (a.altitude,a.file_name_tag),'w')
    dE = 0.001 #tiny sliver of energy used to widen the delta function peak... this way cosima will calculate the flux integral for us :)
    five11_energies = np.array([511.0,511.0 + dE])
    f511.write('IP LIN\n')

    #write phi points
    f511.write('PA ')
    for phi in phipoints:
        f511.write('%.6f ' % (phi))
    #write theta points
    f511.write('\nTA ')
    for th in thetapoints:
        f511.write('%.6f ' % (th))
    #write energy points
    f511.write('\nEA ') 
    for en in five11_energies:
        f511.write('%.6f ' % (en))

    f511.write('\n\n')

    for i in range(len(phipoints)):
        for j in range(len(thetapoints)):
            for k in range(len(five11_energies)):
                f511.write('AP %d %d %d %.6e\n' % (i,j,k,five11[j]/(dE))) #1000 is for MeV->keV, dE is the artificially widened peak width.
    
    f511.write('EN')
    f511.close()










