import numpy as np
from math import sqrt
from random import Random
from Particles.particle import Particle
from Particles.triton import Triton
from Particles.deuteron import Deuteron

max_v = 0.1

class Chamber:
    def __init__(self, laser, x=1, y=1, z=1, particle_number=2):
        # chamber dimensions
        self.laser = laser
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.particle_number = particle_number
        self.particles = list() #np.empty(particle_number, Particle)
    
    # create particles with random positions and velocities
    def create_particles(self):

        deuteron = Deuteron(0, self.y / 2, self.z / 2, 0.02)
        triton = Triton(self.x, self.y / 2, self.z / 2, -0.02)
        self.particles.append(deuteron)
        self.particles.append(triton)

        # for _ in range(0, self.particle_number):
        #     random = Random()
        #     x = random.uniform(0, self.x)
        #     y = random.uniform(0, self.y)
        #     z = random.uniform(0, self.z)
        #     vx = random.uniform(0, max_v)
        #     vy = random.uniform(0, max_v)
        #     vz = random.uniform(0, max_v)
        #     particle = Particle(x, y, z, vx, vy, vz)
        #     self.particles.append(particle)

    # update particle parameters
    def update_particles(self):
        for i in range(0, self.particle_number):
            p1 = self.particles[i]
            for j in range(0, self.particle_number):
                if (i != j):
                    p2 = self.particles[j]
                    if (p1.fusion_can_occur(p2)):
                        helion, neutron = p1.execute_fusion(p2)
                        self.particles[i] = helion
                        self.particles[j] = neutron
                    p1.get_influence_from(p2)
        for p in self.particles:
            p.update_position()
        self.clip_to_bounds()
    
    def on_fusion_occurred(self, helion, neutron):
        pass

    # clip particles inside the chamber
    def clip_to_bounds(self):
        for p in self.particles:
            if (p.x < 0):
                p.vx = -p.vx
                p.x = 0
            elif (p.x > self.x):
                p.vx = -p.vx
                p.x = self.x
                
            if (p.y < 0):
                p.vy = -p.vy
                p.y = 0
            elif (p.y > self.y):
                p.vy = -p.vy
                p.y = self.y

            if (p.z < 0):
                p.vz = -p.vz
                p.z = 0
            elif (p.z > self.z):
                p.vz = -p.vz
                p.z = self.z
