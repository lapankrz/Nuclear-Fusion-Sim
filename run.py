import matplotlib.pyplot as plt
import matplotlib.animation as animation
from chamber import Chamber
from laser import Laser

laser = Laser()

print('''\nSimulation scenarios:
(1) Chamber full of particles
(2) Pair of particles moving towards each other (with collision)
(3) Pair of particles moving towards each other (without collision)
(4) Pair of particles at an angle (with collision)
(5) Pair of particles at an angle (without collision)
(6) Custom simulation
''')
scenario = int(input("Choose scenario: ") or "1")
chamber = Chamber(laser, scenario=scenario)

if scenario == 6:
    particle_pairs = int(input("\nNumber of D+T pairs [10]: ") or "10")
    wavelength = float(input("Laser wavelength [3.51e-8 m]: ") or "3.51e-8")
    intensity = float(input("Laser intensity [5e17 W/m^2]: ") or "5e17")
    activation_time = int(input("Laser activation time [1 s]: ") or "1")
    laser = Laser(wavelength, intensity, activation_time)
    chamber = Chamber(laser, scenario=scenario, particle_pairs=particle_pairs)

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
        plt.title( "Time:                             " + '{:<.3e}'.format(chamber.Time) + " [s]" + "\n"
                 + "Subtracted Energy:        " + '{:<.3e}'.format(chamber.sub_energy) + " [J] " + "\n"
                 + "Total reactions:              " + str(chamber.reaction_count) + "\n"
                 + "Total released energy:   " + '{:<.2f}'.format(chamber.total_energy_released) + " [MeV] " + "\n"
                 + "Temperature:                 " + '{:<.3e}'.format(chamber.Temperature) + " [K]" + "\n"
                 + "Pressure:                       " + '{:<.3e}'.format(chamber.Pressure) + " [Pa]", loc="left", fontsize=8)
    ax.set_xlim([0, chamber.x])
    ax.set_ylim([0, chamber.y])
    ax.set_zlim([0, chamber.z])
    ax.set_xlabel('X axis [m] ')
    ax.set_ylabel('Y axis [m] ')
    ax.set_zlabel('Z axis [m] ')


# file_name = str(input("Choose fileName: "))
# file_name = "./gifs/" + file_name + '.gif'
ani = animation.FuncAnimation(fig, animate, frames=150, interval=50)
# ani.save(file_name, writer='pillow', fps=1000, dpi=80)
plt.show()
