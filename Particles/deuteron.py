from .particle import Particle
from .proton import Proton
from .neutron import Neutron
from .triton import Triton
from .helion import Helion
from scipy import constants as C

min_fusion_dist = 0.01 # TEMPORARY

# Nucleus of deuterium
class Deuteron(Particle):
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15,**other_properties):
        Particle.__init__(self, x, y, z, vx, vy, vz, temperature, **other_properties)
        self.compounds = {Proton(), Neutron()}
        self.mass_MeV = C.value("deuteron mass energy equivalent in MeV")  # [MeV/c2]
        self.mass_kg = C.value("deuteron mass")  # [kg]
        self.charge = C.value("elementary charge")  # [C]
        self.radius = C.value("deuteron rms charge radius")  # [m]
        self.magneticDipoleMoment = C.value("deuteron mag. mom.")  # [J*T**-1]
    
    def fusion_can_occur(self, particle):
        return isinstance(particle, Triton) and self.get_distance_to(particle) < min_fusion_dist

    def execute_fusion(self, triton):
        helion = Helion(self.x, self.y, self.z)
        neutron = Neutron(triton.x, triton.y, triton.z)
        return helion, neutron

    def get_color(self):
        return '#ff1a00'