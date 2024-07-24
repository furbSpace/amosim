import numpy as np
import scipy as sp

# EQUATIONS OF MOTION
def dv(a,dt):
    return a*dt

def ds(u,a,dt):
    return u + a*dt

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
        if z[n] == 0:
            print('Avoiding divide by zero error...\n - Increase resolution if wind at ground is critical!')
            locWindSpeed = 0
            windX = 0
            windY = 0
        elif z[n] < 5000:
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

def simFall(properties,winds,obj,dt):
    t = [0]

    xLoc = [0]
    yLoc = [0]
    zLoc = [obj[1]]

    xVel = [0]
    yVel = [0]
    zVel = [obj[2]]

    xAcl = [0]
    yAcl = [0]
    zAcl = [-sp.constants.g]
    while zLoc[-1] > 0:
        t.append(t[-1] + dt)
        print(f"\n{t[-1]}s")

        xLoc.append(xLoc[-1] + ds(xVel[-1],xAcl[-1],dt))
        yLoc.append(yLoc[-1] + ds(yVel[-1],yAcl[-1],dt))
        zLoc.append(zLoc[-1] + ds(zVel[-1],zAcl[-1],dt))
        print(f"{xLoc[-1]:.2f}m, {yLoc[-1]:.2f}m, {zLoc[-1]:.2f}m")

        xVel.append(xVel[-1] + dv(xAcl[-1],dt))
        yVel.append(yVel[-1] + dv(yAcl[-1],dt))
        zVel.append(zVel[-1] + dv(zAcl[-1],dt))
        print(f"{xVel[-1]:.2f}m/s, {yVel[-1]:.2f}m/s, {zVel[-1]:.2f}m/s")


    return [t,xLoc,yLoc,zLoc,xVel,yVel,zVel]
