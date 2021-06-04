import numpy as np
from math import *
from random import Random

from Particles import particle
from Particles.particle import Particle
from Particles.triton import Triton
from Particles.deuteron import Deuteron
from Particles.helion import Helion
from Particles.neutron import Neutron
from scipy import constants as C
from scipy.stats import norm
import random

energy_released_in_MeV = 17.59
neutron_energy_ratio = 0.7987
MeV_in_Joules = 1.6021773E-13
start_speeds = [1e6, 1e5, 1]
wallCoeff = 0.2  # percent of grabbed energy
chamber_size = 1e-2


class Chamber:
    def __init__(self, laser, x=chamber_size, y=chamber_size, z=chamber_size, particle_pairs=10, scenario=1):
        # chamber dimensions
        self.laser = laser
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.particle_pairs = particle_pairs
        self.scenario = scenario
        self.particles = list()
        self.total_energy_released = 0
        self.reaction_count = 0
        self.sub_energy = 0
        self.Temperature = 298.15  # [ K ]
        self.Pressure = 0  # [ Pa ]
        self.KEavg = 0
        self.Time = 0
        self.iterator = 1
        self.current_max_v = 0
        self.dt = 1e-9  # [ s ]

    # create particles with random positions and velocities
    def create_particles(self):
        start_speed = start_speeds[self.scenario - 1]
        if self.scenario == 1:
            for _ in range(0, self.particle_pairs):
                x, y, z = self.get_random_position()
                vx, vy, vz = self.get_random_velocity(1)
                deuteron = Deuteron(x, y, z, vx, vy, vz)
                deuteron.velocity = deuteron.velocity.normalize() * start_speed
                self.particles.append(deuteron)
                x, y, z = self.get_random_position()
                vx, vy, vz = self.get_random_velocity(0)
                triton = Triton(x, y, z, vx, vy, vz)
                triton.velocity = triton.velocity.normalize() * start_speed
                self.particles.append(triton)
        elif self.scenario == 2:
            deuteron = Deuteron(0, self.y / 2, self.z / 2, start_speed)
            triton = Triton(self.x, self.y / 2, self.z / 2, -start_speed)
            self.particles.append(deuteron)
            self.particles.append(triton)
        elif self.scenario == 3:
            deuteron = Deuteron(0, 0, self.z / 2, start_speed, start_speed)
            triton = Triton(self.x, 0, self.z / 2, -start_speed, start_speed)
            self.particles.append(deuteron)
            self.particles.append(triton)

    # update particle parameters
    def update_particles(self):
        if self.scenario > 1 and self.current_max_v != 0:
            self.dt = 1e-3 / self.current_max_v
        self.current_max_v = 0
        for i in range(0, len(self.particles)):
            p1 = self.particles[i]
            for j in range(0, len(self.particles)):
                if i != j:
                    p2 = self.particles[j]
                    if p1.fusion_can_occur(p2):
                        helion, neutron = self.execute_fusion(p1, p2)
                        self.particles[i] = helion
                        self.particles[j] = neutron
                    p1.get_influence_from(p2)
        for p in self.particles:
            p.update_position(self.dt)
            p.gravity_influence(self.dt)
            laser_state = 1
            self.Temperature += self.LaserExcitation(1, laser_state)
            vsqr = sqrt((3 * C.k * self.Temperature) / p.mass_kg)
            p.velocity +=vsqr
            speed = p.get_speed()
            if speed > self.current_max_v:
                self.current_max_v = speed
        self.clip_to_bounds()
        self.Time += self.dt

    # carry out nuclear fusion
    def execute_fusion(self, deuteron, triton):
        self.reaction_count += 1
        self.total_energy_released += energy_released_in_MeV
        print('Total reactions: ' + str(self.reaction_count) + ", total energy: " + str(
            self.total_energy_released) + " MeV")

        helion = Helion(triton.position.x, triton.position.y, triton.position.z)
        neutron = Neutron(deuteron.position.x, deuteron.position.y, deuteron.position.z)

        input_energy = triton.get_kinetic_energy() + deuteron.get_kinetic_energy()
        output_energy = input_energy + energy_released_in_MeV * MeV_in_Joules
        neutron_energy = neutron_energy_ratio * output_energy  # in Joules
        helion_energy = output_energy - neutron_energy  # in Joules

        helion_speed = sqrt(2 * helion_energy / helion.mass_kg)
        helion.velocity = triton.velocity.normalize() * helion_speed

        neutron_speed = sqrt(2 * neutron_energy / neutron.mass_kg)
        neutron.velocity = deuteron.velocity.normalize() * neutron_speed

        return helion, neutron

    # clip particles inside the chamber
    def clip_to_bounds(self):
        i = 0
        self.KEavg = 0
        for particle in self.particles:
            m = particle.mass_kg
            p = particle.position
            v = particle.velocity
            if p.x < 0:
                v.x = self.set_bound_damping(v.x, m)
                v.x = -v.x
                p.x = 0
            elif p.x > self.x:
                v.x = self.set_bound_damping(v.x, m)
                v.x = -v.x
                p.x = self.x
            if p.y < 0:
                v.y = self.set_bound_damping(v.y, m)
                v.y = -v.y
                p.y = 0
            elif p.y > self.y:
                v.y = self.set_bound_damping(v.y, m)
                v.y = -v.y
                p.y = self.y
            if p.z < 0:
                v.z = self.set_bound_damping(v.z, m)
                v.z = -v.z
                p.z = 0
            elif p.z > self.z:
                v.z = self.set_bound_damping(v.z, m)
                v.z = -v.z
                p.z = self.z
            i += 1
            resultant_velocity = sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)
            self.KEavg += ((m * (resultant_velocity ** 2)) / 2)
            self.iterator += 1
        self.Pressure = (len(self.particles) * self.KEavg / (self.x * self.y * self.z))
        self.Temperature = ((self.KEavg / len(self.particles)) / (3 * C.k))

    def get_random_position(self):
        random = Random()
        x = random.uniform(0, self.x)
        y = random.uniform(0, self.y)
        z = random.uniform(0, self.z)
        return x, y, z

    def gas_velocity(self, flag):
        laser_state = 1
        vsqr = 0
        if flag == 1:
            m = C.value("deuteron mass")
        if flag == 0:
            m = C.value("triton mass")
        T = self.Temperature
        T += self.LaserExcitation(1, laser_state)
        vsqr += (3 * C.k * T) / m
        return sqrt(vsqr)

    def get_random_velocity(self, flag):
        random = Random()
        v = self.gas_velocity(flag)
        vx = random.uniform(-v, v)
        vy = random.uniform(-v, v)
        vz = random.uniform(-v, v)
        return vx, vy, vz

    def set_bound_damping(self, v, m):
        KELost = (m * v ** 2 / 2) * wallCoeff
        self.sub_energy += KELost
        particle_count = len(self.particles)
        energy_per_particle = KELost / particle_count
        for i in range(0, particle_count):
            p = self.particles[i]
            vel = sqrt(2 * energy_per_particle / p.mass_kg)
            p.velocity += vel ** (1 / 3)
        return v * (1 - wallCoeff)

    def LaserExcitation(self, dt, laser_state):
        return self.laser.LightToEnergy(self.x * self.y * self.z, dt, laser_state)
