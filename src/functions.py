import numpy as np

# Function for calculating properties based on altitude
# https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html
def getProperties(z):
    temps = []
    pres = []
    dens = []
    for n in range(len(z)):
        if z[n] < 11000: # Troposphere
            temperature = 15.04 - 0.00649*z[n]
            pressure = 101.29*((temperature + 273.1)/288.08)**5.256
        elif z[n] < 25000 and z[n] > 11000: # Lower Stratosphere
            temperature = -56.46
            pressure = 22.65*np.exp(1.73 - 0.000157*z[n])
        else: # Upper Stratosphere
            temperature = -131.21 + 0.00299*z[n]
            pressure = 2.488*((temperature + 273.1)/216.6)**(-11.388)

        density = pressure/(0.2869*(temperature + 273.1))
        temps.append(temperature)
        pres.append(pressure)
        dens.append(density)

    return np.array([temps,pres,dens])

# Function for estimating wind based upon location
# https://wind-data.ch/tools/profile.php?lng=en
# https://www.coaps.fsu.edu/~bourassa/scat_html/forcing_tut/forcing_tutorial.php
# https://www.researchgate.net/post/How_we_can_realistically_calculate_wind_speed_at_higher_altitudes#:~:text=Alternatively%20another%20formula%20can%20be,Z0%20is%20the%20roughness%20length.
def getWinds(z,windSpeed,windDirection,windAlt,terrainRoughness):
    windDirection = np.deg2rad(windDirection)
    magnitude = []
    u = []
    v = []
    for n in range(len(z)):
        if z[n] < 5000:
            locWindSpeed = windSpeed*((np.log(z[n]/terrainRoughness))/(np.log(windAlt/terrainRoughness)))
            windX = locWindSpeed*np.cos(windDirection)
            windY = locWindSpeed*np.sin(windDirection)
        else:# IGNORE DATA PAST 5000m
            locWindSpeed = locWindSpeed
            windX = windX
            windY = windY

        magnitude.append(locWindSpeed)
        u.append(windX)
        v.append(windY)

    return [magnitude,u,v]
