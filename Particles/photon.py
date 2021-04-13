from .particle import Particle
from scipy import constants as C
from math import sqrt, pi, inf

class Photon(Particle):
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,
                DFBWavelength=1000 * 10 ** -9, **other_properties):
        Particle.__init__(self, x, y, z, vx, vy, vz, temperature, **other_properties)
        self.type = "Elementary particle"
        self.statistics = "Boson"  # Elementary particle
        self.compounds = {"elementary"}
        self.mass_MeV = (C.value("Planck constant") * (
                C.value("speed of light in vacuum") / DFBWavelength)) * 10 ** -6  # [MeV]
        self.mass_kg = (self.mass_MeV * 1.7827E-36) * 10 ** 6
        self.charge = 1 * 10 ** -35 * C.value("elementary charge")  # [C]
        self.spin = 1
        self.radius = (2 * sqrt(2 * C.value("classical electron radius") * DFBWavelength)) / (
                (sqrt(2) - 1) * pi)  # [m]
        self.meanLifetime = inf
        self.magneticDipoleMoment = 0
        self.electricDipoleMoment = 0
        self.electricPolarizability = 0
        self.magneticPolarizability = 0