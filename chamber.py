import numpy as np
from math import sqrt
from random import Random
from Particles.particle import Particle

max_v = 0.1

class Chamber:
    def __init__(self, x=1, y=1, z=1, particle_number=20):
        # chamber dimensions
        self.x = x
        self.y = y
        self.z = z

        self.particle_number = particle_number
        self.particles = np.empty(particle_number, Particle)
    
    # create particles with random positions and velocities
    def create_particles(self):
        for i in range(0, self.particle_number):
            random = Random()
            x = random.uniform(0, self.x)
            y = random.uniform(0, self.y)
            z = random.uniform(0, self.z)
            vx = random.uniform(0, max_v)
            vy = random.uniform(0, max_v)
            vz = random.uniform(0, max_v)
            particle = Particle(x, y, z, vx, vy, vz)
            self.particles[i] = particle

    # update particle parameters
    def update_particles(self):
        new_particles = np.empty(self.particle_number, Particle)
        for i in range(0, self.particle_number):
            p1 = self.particles[i]
            new_particle = Particle(p1.x, p1.y, p1.z, p1.vx, p1.vy, p1.vz)
            for j in range(0, self.particle_number):
                if (i == j):
                    continue
                p2 = self.particles[j]
                new_particle.get_influence_from(p2)
            new_particle.update_position()
            new_particles[i] = new_particle
        self.particles = new_particles
        self.clip_to_bounds()

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
