from Particles.helion import Helion
from Particles.triton import Triton
from Particles.neutron import Neutron
from Particles.deuteron import Deuteron
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from chamber import Chamber
from laser import Laser
from matplotlib.widgets import Slider

laser = Laser()
matplotlib.use('Qt5Agg')

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
frame_number = int(input("Number of frames to generate [100]: ") or "100")

if scenario == 6:
    particle_pairs = int(input("\nNumber of D+T pairs [10]: ") or "10")
    wavelength = float(input("Laser wavelength [3.51e-8 m]: ") or "3.51e-8")
    intensity = float(input("Laser intensity [5e17 W/m^2]: ") or "5e17")
    activation_time = int(input("Laser activation time [1 s]: ") or "1")
    laser = Laser(wavelength, intensity, activation_time)
    chamber = Chamber(laser, scenario=scenario, particle_pairs=particle_pairs)

chamber.create_particles()

file_name = "scenario" + str(scenario)
file_name = "./" + file_name + '.gif'

fig = plt.figure()

grid = plt.GridSpec(3, 4, wspace=6, hspace=0.6)
ax = fig.add_subplot(grid[:, :2], projection='3d')
aa = fig.add_subplot(grid[0, 2:])
ay = fig.add_subplot(grid[1, 2:])
az = fig.add_subplot(grid[2, 2:])

ax.set_xlim([0, chamber.x])
ax.set_ylim([0, chamber.y])
ax.set_zlim([0, chamber.z])
ax.set_xlabel('X axis [m] ')
ax.set_ylabel('Y axis [m] ')
ax.set_zlabel('Z axis [m] ')

ay.set_ylabel('Temperature [ K ] ')
ay.grid(True)

az.set_xlabel('Time [ s ]')
az.set_ylabel('Pressure [ Pa ] ')
az.grid(True)

aa.set_ylabel('Sub Energy [ J ] ')
aa.grid(True)

lines, x, y, z, helionx, heliony, helionz, deuteronx, deuterony, deuteronz, tritonx, tritony, tritonz, \
neutronx, neutrony, neutronz, Time, Temperature, SubEnergy, ReactionCount, TotalEnergy, Pressure, title = ([] for i in
                                                                                                           range(23))
helion_color = Helion().get_color()
neutron_color = Neutron().get_color()
triton_color = Triton().get_color()
deuteron_color = Deuteron().get_color()

for i in range(0, frame_number):
    chamber.update_particles()
    for p in chamber.particles:
        if isinstance(p, Helion):
            helionx.append(p.position.x)
            heliony.append(p.position.y)
            helionz.append(p.position.z)
        elif isinstance(p, Deuteron):
            deuteronx.append(p.position.x)
            deuterony.append(p.position.y)
            deuteronz.append(p.position.z)
        elif isinstance(p, Triton):
            tritonx.append(p.position.x)
            tritony.append(p.position.y)
            tritonz.append(p.position.z)
        else:
            neutronx.append(p.position.x)
            neutrony.append(p.position.y)
            neutronz.append(p.position.z)
            
    Time.append(chamber.Time)
    SubEnergy.append(chamber.sub_energy)
    ReactionCount.append(chamber.reaction_count)
    TotalEnergy.append(chamber.total_energy_released)
    Temperature.append(chamber.Temperature)
    Pressure.append(chamber.Pressure)

    lineh, = ax.plot(helionx, heliony, helionz, color='None', marker='.', markeredgecolor=helion_color, markerfacecolor=helion_color)
    lined, = ax.plot(deuteronx, deuterony, deuteronz, color='None', marker='.', markeredgecolor=deuteron_color, markerfacecolor=deuteron_color)
    linet, = ax.plot(tritonx, tritony, tritonz, color='None', marker='.', markeredgecolor=triton_color, markerfacecolor=triton_color)
    linen, = ax.plot(neutronx, neutrony, neutronz, color='None', marker='.', markeredgecolor=neutron_color, markerfacecolor=neutron_color)
    line2, = ay.semilogy(Time, Temperature, color='red', marker=',')
    line3, = az.semilogy(Time, Pressure, color='green', marker=',')
    line4, = aa.semilogy(Time, SubEnergy, color='blue', marker=',')

    title = ax.text2D(0.25, 1, "Time:                             " + '{:<.3e}'.format(chamber.Time) + " [s]" + "\n"
                + "Subtracted Energy:        " + '{:<.3e}'.format(chamber.sub_energy) + " [J] " + "\n"
                + "Total reactions:              " + str(chamber.reaction_count) + "\n"
                + "Total released energy:   " + '{:<.2f}'.format(chamber.total_energy_released) + " [MeV] " + "\n"
                + "Temperature:                 " + '{:<.3e}'.format(chamber.Temperature) + " [K]" + "\n"
                + "Pressure:                       " + '{:<.3e}'.format(chamber.Pressure) + " [Pa]",
                transform=ax.transAxes)
    lines.append([lineh, lined, linet, linen, title, line2, line3, line4])
    x.clear(), y.clear(), z.clear(), helionx.clear(), heliony.clear(), helionz.clear(), deuteronx.clear(), deuterony.clear(), deuteronz.clear()
    tritonx.clear(), tritony.clear(), tritonz.clear(), neutronx.clear(), neutrony.clear(), neutronz.clear()

ani = animation.ArtistAnimation(fig, lines, interval=20, blit=False)
ani.save(file_name, writer='pillow', fps=30)
figManager = plt.get_current_fig_manager()
figManager.window.resize(1500, 700)
plt.show()
