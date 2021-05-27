import numpy as np
from math import sqrt
from random import Random
from Particles.particle import Particle
from Particles.triton import Triton
from Particles.deuteron import Deuteron
from Particles.helion import Helion
from Particles.neutron import Neutron
from scipy import constants as C

max_v = 0.1
energy_released_in_MeV = 17.59
neutron_energy_ratio = 0.7987
MeV_in_Joules = 1.6021773E-13

class Chamber:
    def __init__(self, laser, x=1, y=1, z=1, particle_pairs=8, simultaneous = False):
        # chamber dimensions
        self.laser = laser
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.particle_pairs = particle_pairs
        self.simultaneous = simultaneous # if true - all particles created at once, otherwise one pair at a time
        self.particles = list()
        self.total_energy_released = 0
        self.reaction_count = 0
    
    # create particles with random positions and velocities
    def create_particles(self):
        if (self.simultaneous):
            for _ in range(0, self.particle_pairs):
                x, y, z = self.get_random_position()
                vx, vy, vz = self.get_random_velocity()
                deuteron = Deuteron(x, y, z, vx, vy, vz)
                self.particles.append(deuteron)

                x, y, z = self.get_random_position()
                vx, vy, vz = self.get_random_velocity()
                triton = Triton(x, y, z, vx, vy, vz)
                self.particles.append(triton)
        else:
            deuteron = Deuteron(0, self.y / 2, self.z / 2, 0.05)
            triton = Triton(self.x, self.y / 2, self.z / 2, -0.05)
            self.particles.append(deuteron)
            self.particles.append(triton)

    # update particle parameters
    def update_particles(self):
        for i in range(0, len(self.particles)):
            p1 = self.particles[i]
            for j in range(0, len(self.particles)):
                if (i != j):
                    p2 = self.particles[j]
                    if (p1.fusion_can_occur(p2)):
                        helion, neutron = self.execute_fusion(p1, p2)
                        self.particles[i] = helion
                        self.particles[j] = neutron
                    p1.get_influence_from(p2)
        for p in self.particles:
            p.update_position()
        self.clip_to_bounds()

    # carry out nuclear fusion
    def execute_fusion(self, deuteron, triton):
        self.reaction_count += 1
        self.total_energy_released += energy_released_in_MeV
        print('Total reactions: ' + str(self.reaction_count) + ", total energy: " + str(self.total_energy_released) + " MeV")

        helion = Helion(triton.position.x, triton.position.y, triton.position.z)
        neutron = Neutron(deuteron.position.x, deuteron.position.y, deuteron.position.z)

        input_energy = triton.get_kinetic_energy() + deuteron.get_kinetic_energy()
        output_energy = input_energy + energy_released_in_MeV * MeV_in_Joules
        neutron_energy = neutron_energy_ratio *  output_energy # in Joules
        helion_energy = output_energy - neutron_energy # in Joules

        helion_speed = sqrt(2 * helion_energy / helion.mass_kg)
        helion.velocity = deuteron.velocity.normalize() * helion_speed

        neutron_speed = sqrt(2 * neutron_energy / neutron.mass_kg)
        neutron.velocity = deuteron.velocity.normalize() * neutron_speed

        return helion, neutron

    # clip particles inside the chamber
    def clip_to_bounds(self):
        for particle in self.particles:
            p = particle.position
            v = particle.velocity
            if (p.x < 0):
                v.x = -v.x
                p.x = 0
            elif (p.x > self.x):
                v.x = -v.x
                p.x = self.x
                
            if (p.y < 0):
                v.y = -v.y
                p.y = 0
            elif (p.y > self.y):
                v.y = -v.y
                p.y = self.y

            if (p.z < 0):
                v.z = -v.z
                p.z = 0
            elif (p.z > self.z):
                v.z = -v.z
                p.z = self.z

    def get_random_position(self):
        random = Random()
        x = random.uniform(0, self.x)
        y = random.uniform(0, self.y)
        z = random.uniform(0, self.z)
        return x, y, z

    def get_random_velocity(self):
        random = Random()
        vx = random.uniform(-max_v, max_v)
        vy = random.uniform(-max_v, max_v)
        vz = random.uniform(-max_v, max_v)
        return vx, vy, vz