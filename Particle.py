from numpy import *
from scipy import constants as C
from math import *


class Particle:
    def __init__(self, name, DFBWavelength=1000 * 10 ** -9, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,
                 **other_properties):
        # type of particle
        self.name = name

        if self.name == "proton" or "p+" or "p":
            # properties of particle
            self.type = "Baryon"  # Baryon
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

        if self.name == "neutron" or "n" or "n0":
            # properties of particle
            self.type = "Baryon"  # Baryon
            self.statistics = "Fermion"
            self.compounds = {"u", "d", "d"}
            self.mass_MeV = C.value("neutron mass energy equivalent in MeV")  # [MeV/c2]
            self.mass_kg = C.value("neutron mass")  # [kg]
            self.charge = 0  # [C] (theoretical)
            self.spin = 1 / 2
            self.radius = 0.8 * 10 ** -15  # [m]
            self.meanLifetime = 879.466  # [s]
            self.magneticDipoleMoment = C.value("neutron mag. mom.")  # [J*T**-1]
            self.electricDipoleMoment = 2.9 * 10 ** -26  # [e*cm]
            self.electricPolarizability = 1.1615 * 10 ** -3  # [f*m**3]
            self.magneticPolarizability = 3.720 * 10 ** -4  # [f*m**3]

        if self.name == "electron" or "e" or "e-" or "u":
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

        if self.name == "photon" or "hv" or "ph" or "γ" or "Y":
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
            self.meanLifetime = Inf
            self.magneticDipoleMoment = 0
            self.electricDipoleMoment = 0
            self.electricPolarizability = 0
            self.magneticPolarizability = 0
        if self.name == "neutrino" or "ve" or "vu" or "vt":
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
        else:
            # properties of particle
            self.type = 0
            self.statistics = 0
            self.compounds = 0
            self.mass_eV = 0
            self.mass_kg = 0
            self.charge = 0
            self.spin = 0
            self.radius = 0
            self.meanLifetime = 0
            self.magneticDipoleMoment = 0
            self.electricDipoleMoment = 0
            self.electricPolarizability = 0
            self.magneticPolarizability = 0

        # current position in cartesian coordinate
        self.x = x
        self.y = y
        self.z = z

        # forces acting of particle / physical mathematical external properties
        self.vx = vx  # [m/s]
        self.vy = vy  # [m/s]
        self.vz = vz  # [m/s]

        self.position = array([x, y, z])
        self.velocity = array([vx, vy, vz])  # [m/s]
        self.speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2  + self.velocity[1]**2)
        # other defined properties
        self.temperature = temperature  # [K]

        # other not-defined parameters / properties
        for name, value in other_properties.items():
            setattr(self, name, value)

    def move(self):
