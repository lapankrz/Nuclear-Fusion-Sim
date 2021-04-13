from .particle import Particle
from scipy import constants as C
from math import sqrt

class Neutrino(Particle):
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,**other_properties):
        Particle.__init__(self, x, y, z, vx, vy, vz, temperature, **other_properties)
        self.type = "Elementary particle"
        self.statistics = "Fermion"  # Elementary particle
        self.compounds = {"elementary"}
        self.mass_MeV = 0.120 * 10 ** -6  # [MeV]
        self.mass_kg = 2.14 * 10 ** -37  # [kg]
        self.charge = 0  # [C]
        self.spin = 1 / 2
        self.radius = sqrt((3.32 / 2) * 10 ** -32) * 100  # [m]
        self.meanLifetime = 2 * 10 ** 8 * 3.154e+7
        self.magneticDipoleMoment = 0
        self.electricDipoleMoment = 0
        self.electricPolarizability = 0
        self.magneticPolarizability = 0