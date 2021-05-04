import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import sqrt
from time import sleep
from chamber import Chamber
from laser import Laser

laser = Laser()
chamber = Chamber(laser, simultaneous=True)
chamber.create_particles()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

def animate(i):
    ax.clear()
    chamber.update_particles()
    for p in chamber.particles:
        x = p.x
        y = p.y
        z = p.z
        ax.scatter(x, y, z, c=[p.get_color()])
    
    ax.set_xlim([0, chamber.x])
    ax.set_ylim([0, chamber.y])
    ax.set_zlim([0, chamber.z])

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()