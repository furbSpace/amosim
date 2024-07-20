import numpy as np
import matplotlib.pyplot as plt

def getProperties(z):
    # Function for calculating properties based on altitude
    # https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html
    temps = []
    pres = []
    dens = []
    for n in range(len(z)):
        h = z[n]
        if h < 11000: # Troposphere
            temperature = 15.04 - 0.00649*h
            pressure = 101.29*((temperature + 273.1)/288.08)**5.256
        elif h < 25000 and h > 11000: # Lower Stratosphere
            temperature = -56.46
            pressure = 22.65*np.exp(1.73 - 0.000157*h)
        else: # Upper Stratosphere
            temperature = -131.21 + 0.00299*h
            pressure = 2.488*((temperature + 273.1)/216.6)**(-11.388)

        density = pressure/(0.2869*(temperature + 273.1))
        temps.append(temperature)
        pres.append(pressure)
        dens.append(density)

    return np.array([temps,pres,dens])

def getWind(z):
    # Function for estimating wind based upon location
    # https://wind-data.ch/tools/profile.php?lng=en
    # https://www.coaps.fsu.edu/~bourassa/scat_html/forcing_tut/forcing_tutorial.php
    # https://www.researchgate.net/post/How_we_can_realistically_calculate_wind_speed_at_higher_altitudes#:~:text=Alternatively%20another%20formula%20can%20be,Z0%20is%20the%20roughness%20length.
    u=1
    v=1

    return [u,v]

resolution = 100
maxAlt = 50000
alt = np.linspace(0,maxAlt,resolution)
conditions = getProperties(alt)

# Plotting Atmospheric Conditions
fig,ax = plt.subplots(1,3,sharey=True)
fig.set_size_inches(11,7)
fig.suptitle(r"Properties of Air at Various Altitudes")
fig.supylabel(r"Altitude $(m)$")
plt.ylim(0,maxAlt)

# Temperature Subplot
ax[0].plot(conditions[0],alt,'-')
ax[0].set_xlabel(r"Temperature $(\degree C)$")
ax[0].grid()

# Pressure Subplot
ax[1].plot(conditions[1],alt,'-')
ax[1].set_xlabel(r"Pressure $(kPa)$")
ax[1].grid()

# Density Subplot
ax[2].plot(conditions[2],alt,'-')
ax[2].set_xlabel(r"Density $(kg \cdot m^{-3})$")
ax[2].grid()

plt.show() # Show figures
