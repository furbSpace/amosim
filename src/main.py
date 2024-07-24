import matplotlib.pyplot as plt
from variables import *



# Plotting Atmospheric Conditions
fig1,ax1 = plt.subplots(1,4,sharey=True)
fig1.set_size_inches(15,7)
fig1.suptitle(r"Properties of Air and Winds at Various Altitudes")
fig1.supylabel(r"Altitude $(m)$")
plt.ylim(0,maxAlt)

# Temperature Subplot
ax1[0].plot(properties[0],altRange,'-')
ax1[0].set_xlabel(r"Temperature $(\degree C)$")
ax1[0].grid()

# Pressure Subplot
ax1[1].plot(properties[1],altRange,'-')
ax1[1].set_xlabel(r"Pressure $(kPa)$")
ax1[1].grid()

# Density Subplot
ax1[2].plot(properties[2],altRange,'-')
ax1[2].set_xlabel(r"Density $(kgm^{-3})$")
ax1[2].grid()

# Winds Subplot
ax1[3].plot(winds[0],altRange,'-',label="Magnitude")
ax1[3].plot(winds[1],altRange,'-',label="Longitudinal")
ax1[3].plot(winds[2],altRange,'-',label="Latitudinal")
ax1[3].set_xlabel(r"Velocity $(ms^{-1})$")
ax1[3].grid()
plt.axhline(y=5000,color='r',linestyle='--',label="Terrain Influence")
ax1[3].plot(windSpeed,windAlt,'d',label="Reference")
ax1[3].set_title("Winds")
plt.legend(loc='best')

# Plotting Simulated Fall
fig2,ax2 = plt.subplots(1,4,sharex=True)
fig2.set_size_inches(15,7)
fig2.suptitle(r"Simulated Fall")
fig2.supxlabel(r"Time $(s)$")
plt.xlim(0,max(fall[0]))

# X Coordinate Subplot
ax2[0].plot(fall[0],fall[1],'-')
ax2[0].set_ylabel(r"Position $(m)$")
ax2[0].grid()

# Y Coordinate Subplot
ax2[1].plot(fall[0],fall[2],'-')
ax2[1].set_ylabel(r"Position $(m)$")
ax2[1].grid()

# Z Coordinate Subplot
ax2[2].plot(fall[0],fall[3],'-')
ax2[2].set_ylabel(r"Position $(m)$")
ax2[2].grid()

# Velocities Subplot
ax2[3].plot(fall[0],fall[4],'-')
ax2[3].plot(fall[0],fall[5],'-')
ax2[3].plot(fall[0],fall[6],'-')
ax2[3].set_ylabel(r"Velocity $(ms^{-1})$")
ax2[3].grid()

plt.show() # Show Plots
