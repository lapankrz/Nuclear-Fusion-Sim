import numpy as np
from math import sqrt
from random import Random
from Particles.particle import Particle
from scipy import constants as C


class Laser:
    def __init__(self, wavelength=3.51e-7, intensity=1e19):  # default values from NIF inertial confinement fusion laser
        self.wavelength = wavelength  # in meters
        self.intensity = intensity  # in W/m^2
        self.frequency = C.speed_of_light / wavelength  # in Hz

    def LightToEnergy(self, input_area, dt, flag):
        if flag == 1:
            Ephoton = C.h * self.frequency  # eV # wavelength in [ um ]
            nPhotons = Ephoton * self.intensity / input_area * dt
            Ethermal = C.eV * Ephoton * nPhotons * 7.242971666667e+22  # [ K]
        else:
            Ethermal = 0
        return Ethermal
