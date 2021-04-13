from .particle import Particle
from scipy import constants as C

class Electron(Particle):
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,**other_properties):
        Particle.__init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,**other_properties)
        self.type = "Elementary particle"
        self.statistics = "Fermion"  # Elementary particle
        self.compounds = {"elementary"}
        self.mass_MeV = C.value("electron mass energy equivalent in MeV")  # [MeV/c2]
        self.mass_kg = C.value("electron mass")  # [kg]
        self.charge = -C.value("elementary charge")  # [C]
        self.spin = 1 / 2
        self.radius = C.value("classical electron radius")
        self.meanLifetime = (1 * 10 ** 29) * 3.154e+7  # [s]
        self.magneticDipoleMoment = C.value("electron mag. mom.")  # [J*T**-1]
        self.electricDipoleMoment = 5.4 * 10 ** -24  # [e*cm]
        self.electricPolarizability = 1.20666 * 10 ** -3  # [f*m**3]
        self.magneticPolarizability = 1.9555 * 10 ** -4  # [f*m**3]