import matplotlib.pyplot as plt
from variables import *

# Plotting Atmospheric Condifrom functions import *tions
fig,ax = plt.subplots(1,4,sharey=True)
fig.set_size_inches(15,7)
fig.suptitle(r"Properties of Air and Winds at Various Altitudes")
fig.supylabel(r"Altitude $(m)$")
plt.ylim(0,maxAlt)

# Temperature Subplot
ax[0].plot(properties[0],altRange,'-')
ax[0].set_xlabel(r"Temperature $(\degree C)$")
ax[0].grid()

# Pressure Subplot
ax[1].plot(properties[1],altRange,'-')
ax[1].set_xlabel(r"Pressure $(kPa)$")
ax[1].grid()

# Density Subplot
ax[2].plot(properties[2],altRange,'-')
ax[2].set_xlabel(r"Density $(kgm^{-3})$")
ax[2].grid()

# Winds Subplot
ax[3].plot(winds[0],altRange,'-',label="Magnitude")
ax[3].plot(winds[1],altRange,'-',label="Longitudinal")
ax[3].plot(winds[2],altRange,'-',label="Latitudinal")
ax[3].set_xlabel(r"Velocity/Speed $(ms^{-1})$")
ax[3].grid()
plt.axhline(y=5000,color='r',linestyle='--',label="Terrain Influence")
ax[3].plot(windSpeed,windAlt,'d',label="Reference")
ax[3].set_title("Winds")
plt.legend(loc='best')

plt.show() # Show Plots
