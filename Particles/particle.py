import numpy as np
from math import sqrt
from scipy import constants as C
from vectormath import Vector3

proportion_constant = 1e30
max_speed = 0.4

class Particle:
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, temperature=298.15, **other_properties):
        self.position = Vector3(x,y,z)
        self.velocity = Vector3(vx, vy, vz) # [m/s]
        self.temperature = temperature  # [K]

        for name, value in other_properties.items():
            setattr(self, name, value)
    
    def get_speed(self):
        v = self.velocity
        return sqrt(v.x**2 + v.y**2  + v.z**2)
    
    # modify particle velocity based on influence from some particle
    # returns true if fusion occured, false otherwise
    def get_influence_from(self, particle):
        dist = self.get_distance_to(particle)
        if (dist > 0):
            force = (C.k * self.charge * particle.charge) / (dist**2)
            acc = force / (self.mass_kg)
            self.velocity += acc * -self.get_vector_to(particle) * proportion_constant
            if (self.velocity.length > max_speed):
                self.velocity = self.velocity.normalize() * max_speed
        return False #TODO add influence from particle - implement in subclasses

    def fusion_can_occur(self, particle):
        return False

    def get_distance_to(self, particle):
        # ret = sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2 + (self.z - particle.z)**2)
        return (particle.position - self.position).length
    
    # modify position by current velocity value
    def update_position(self):
        self.position += self.velocity

    # get unique color for this particle type (used for plotting)
    def get_color(self):
        return '#000000'

    # get normalized vector from self to particle
    def get_vector_to(self, particle):
        return particle.position - self.position

    def get_kinetic_energy(self):
        return self.mass_kg * self.get_speed()**2 / 2
