import matplotlib.pyplot as plt
from variables import *

# Plotting Atmospheric Conditions
fig1,ax1 = plt.subplots(1,4,sharey=True)
fig1.set_size_inches(15,7)
fig1.suptitle(r"Properties of Air and Winds")
plt.ylim(0,maxAlt)

# Temperature Subplot
ax1[0].plot(properties[0],altRange,'-',color="black")
ax1[0].set_xlabel(r"Temperature $(\degree C)$")
ax1[0].set_ylabel(r"Altitude $(m)$")
ax1[0].grid()

# Pressure Subplot
ax1[1].plot(properties[1],altRange,'-',color="black")
ax1[1].set_xlabel(r"Pressure $(kPa)$")
ax1[1].grid()

# Density Subplot
ax1[2].plot(properties[2],altRange,'-',color="black")
ax1[2].set_xlabel(r"Density $(kgm^{-3})$")
ax1[2].grid()

# Winds Subplot
ax1[3].plot(winds[0],altRange,'-',label="Magnitude",color="black")
ax1[3].plot(winds[1],altRange,'-',label="X Component",color="red")
ax1[3].plot(winds[2],altRange,'-',label="Y Component",color="green")
ax1[3].set_xlabel(r"Velocity $(ms^{-1})$")
ax1[3].legend(loc="best")
ax1[3].grid()

# Plotting Simulated Fall
fig2,ax2 = plt.subplots(1,3,sharex=True)
fig2.set_size_inches(15,7)
fig2.suptitle(r"Idealized Fall of $1m^3$ Cube")
plt.xlim(0,max(fall[0]))

# X & Y Movement Subplot
ax2[0].plot(fall[0],fall[1],'-',label="X Movement",color="red")
ax2[0].plot(fall[0],fall[2],'-',label="Y Movement",color="green")
ax2[0].set_xlabel(r"Time $(s)$")
ax2[0].set_ylabel(r"Position $(m)$")
ax2[0].grid()
ax2[0].legend(loc='best')
ax2[0].set_title("Traversal")

# Z Coordinate Subplot
ax2[1].plot(fall[0],fall[3],'-',color="blue")
ax2[1].set_xlabel(r"Time $(s)$")
ax2[1].set_ylabel(r"Altitude $(m)$")
ax2[1].grid()
ax2[1].set_title("Altitude")

# Velocities Subplot
ax2[2].plot(fall[0],fall[4],'-',label="X Velocity",color="red")
ax2[2].plot(fall[0],fall[5],'-',label="Y Velocity",color="green")
ax2[2].plot(fall[0],fall[6],'-',label="Z Velocity",color="blue")
ax2[2].set_xlabel(r"Time $(s)$")
ax2[2].set_ylabel(r"Velocity $(ms^{-1})$")
ax2[2].grid()
ax2[2].legend(loc='best')
ax2[2].set_title("Velocity")

plt.show() # Show Plots
