import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sqrt
from time import sleep
from chamber import Chamber
from laser import Laser


print('''\nSimulation scenarios:
(1) Chamber full of particles
(2) Pair of particles colliding head on
(3) Pair of particles colliding at an angle''')
scenario = int(input("Choose scenario: "))

if (scenario > 1):
    speed_percent = float(input('''\nChoose fraction of minimal particle speed for reaction to appear: '''))
else:
    speed_percent = 1.0

laser = Laser()
chamber = Chamber(laser, scenario=scenario, speed_percent=speed_percent)
chamber.create_particles()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

def animate(i):
    ax.clear()
    chamber.update_particles()
    for p in chamber.particles:
        x = p.position.x
        y = p.position.y
        z = p.position.z
        ax.scatter(x, y, z, c=[p.get_color()])
    
    ax.set_xlim([0, chamber.x])
    ax.set_ylim([0, chamber.y])
    ax.set_zlim([0, chamber.z])

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()


