from .particle import Particle
from scipy import constants as C

class Proton(Particle):
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,**other_properties):
        Particle.__init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,**other_properties)
        self.type = "Baryon"
        self.statistics = "Fermion"
        self.compounds = {"u", "u", "d"}
        self.mass_MeV = C.value("proton mass energy equivalent in MeV")  # [MeV/c2]
        self.mass_kg = C.value("proton mass")  # [kg]
        self.charge = C.value("elementary charge")  # [C]
        self.spin = 1 / 2
        self.radius = C.value("proton rms charge radius")  # [m]
        self.meanLifetime = (1 * 10 ** 34) * 3.154e+7  # [s]
        self.magneticDipoleMoment = C.value("proton mag. mom.")  # [J*T**-1]
        self.electricDipoleMoment = 5.4 * 10 ** -24  # [e*cm]
        self.electricPolarizability = 1.2066 * 10 ** -3  # [f*m**3]
        self.magneticPolarizability = 1.9555 * 10 ** -4  # [f*m**3]