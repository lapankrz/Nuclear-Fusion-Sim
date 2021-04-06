import numpy as np
from math import sqrt

class Particle:
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15, **other_properties):
        # current position in cartesian coordinate
        self.x = x
        self.y = y
        self.z = z

        # forces acting of particle / physical mathematical external properties
        self.vx = vx  # [m/s]
        self.vy = vy  # [m/s]
        self.vz = vz  # [m/s]

        # other defined properties
        self.temperature = temperature  # [K]

        # other not-defined parameters / properties
        for name, value in other_properties.items():
            setattr(self, name, value)
    
    def get_speed(self):
        return sqrt(self.vx**2 + self.vy**2  + self.vz**2)

    def get_position(self):
        return np.array([self.x, self.y, self.z])

    def get_velocity(self):
        return np.array([self.vx, self.vy, self.vz])
    
    # modify particle parameters based on influence from some particle
    def get_influence_from(self, particle):
        pass #TODO add influence from particle

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
