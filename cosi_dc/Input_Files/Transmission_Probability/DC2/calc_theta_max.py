# Imports
import math


"""
Calculates the zenith angle for Earch occultation,
given the altitude of the orbit. The current calculation
is only for a zenith pointing orbit. 
"""


R_earth = 6378 # km
h = 550 # km

theta_m = math.pi - math.asin(R_earth/(R_earth+h)) # radians
theta_m = theta_m * (180/math.pi) # degrees

print()
print("theta_m [deg]: " + str(theta_m))

