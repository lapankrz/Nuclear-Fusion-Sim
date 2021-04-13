import numpy as np
from math import sqrt
from random import Random
from Particles.particle import Particle
from scipy import constants as C

class Laser:
    def __init__(self, wavelength=3.51e-7, intensity=5e19): # default values from NIF inertial confinement fusion laser
        self.wavelength = wavelength # in meters
        self.intensity = intensity # in W/m^2
        self.frequency = C.speed_of_light / wavelength # in Hz
