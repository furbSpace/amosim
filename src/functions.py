import numpy as np
import scipy as sp

# PHYSICS EQUATIONS
def v(v0,a,dt):
    return v0 + a*dt

def dx(v0,a,dt):
    return v0*dt + 0.5*a*(dt**2)

def drag(rho,A,cD,v):
    if v > 0:
        return (0.5*rho*A*cD*(v**2))
    else:
        return -(0.5*rho*A*cD*(v**2))

# Function for calculating properties based on altitude
# https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html
def getProperties(z,runType=0):
    if runType == 0: # Range Calculation
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
    elif runType == 1: # Specific Altitude
        if z < 11000: # Troposphere
            temperature = 15.04 - 0.00649*z
            pressure = 101.29*((temperature + 273.1)/288.08)**5.256
        elif z < 25000 and z > 11000: # Lower Stratosphere
            temperature = -56.46
            pressure = 22.65*np.exp(1.73 - 0.000157*z)
        else: # Upper Stratosphere
            temperature = -131.21 + 0.00299*z
            pressure = 2.488*((temperature + 273.1)/216.6)**(-11.388)

        density = pressure/(0.2869*(temperature + 273.1))
        return [temperature,pressure,density]

# Function for estimating wind based upon location
# https://wind-data.ch/tools/profile.php?lng=en
# https://www.coaps.fsu.edu/~bourassa/scat_html/forcing_tut/forcing_tutorial.php
# https://www.researchgate.net/post/How_we_can_realistically_calculate_wind_speed_at_higher_altitudes#:~:text=Alternatively%20another%20formula%20can%20be,Z0%20is%20the%20roughness%20length.
def getWinds(z,windInfo,runType=0):
    windSpeed = windInfo[0]
    windDirection = np.deg2rad(windInfo[1]+180) # Convert Compass Degrees
    windAlt = windInfo[2]
    terrainRoughness = windInfo[3]

    if runType == 0:
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
                windX = locWindSpeed*np.sin(windDirection)
                windY = locWindSpeed*np.cos(windDirection)
            else:# IGNORE DATA PAST 5000m
                print('Above 5000m!')
                locWindSpeed = 0
                windX = 0
                windY = 0

            magnitude.append(locWindSpeed)
            u.append(windX)
            v.append(windY)

        return [magnitude,u,v]
    elif runType == 1:
        if z <= 0:
            print('Below sea level!')
            locWindSpeed = 0
            windX = 0
            windY = 0
        elif z <= 5000:
            locWindSpeed = windSpeed*((np.log(z/terrainRoughness))/(np.log(windAlt/terrainRoughness)))
            windX = locWindSpeed*np.sin(windDirection)
            windY = locWindSpeed*np.cos(windDirection)
        else:# IGNORE DATA PAST 5000m
            print('Above 5000m!')
            locWindSpeed = 0
            windX = 0
            windY = 0

        return [locWindSpeed,windX,windY]

# Simple Falling Simulation
def simFall(obj,windInfo,dt):
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
        altProperties = getProperties(zLoc[-1],1)
        altWinds = getWinds(zLoc[-1],windInfo,1)

        t.append(t[-1] + dt)
        print(f"\n{t[-1]:.2f}s")

        xAcl.append((drag(altProperties[2],obj[3],obj[4],altWinds[1]))/obj[0])
        yAcl.append((drag(altProperties[2],obj[3],obj[4],altWinds[2]))/obj[0])
        zAcl.append(zAcl[0] - (drag(altProperties[2],obj[3],obj[4],zVel[-1]))/obj[0])

        xLoc.append(xLoc[-1] + dx(xVel[-1],xAcl[-1],dt))
        yLoc.append(yLoc[-1] + dx(yVel[-1],yAcl[-1],dt))
        zLoc.append(zLoc[-1] + dx(zVel[-1],zAcl[-1],dt)) # Dropping too fast, not possible
        print(f"{xLoc[-1]:.2f}m, {yLoc[-1]:.2f}m, {zLoc[-1]:.2f}m")

        xVel.append(v(xVel[-1],xAcl[-1],dt))
        yVel.append(v(yVel[-1],yAcl[-1],dt))
        zVel.append(v(zVel[-1],zAcl[-1],dt))
        print(f"{xVel[-1]:.2f}m/s, {yVel[-1]:.2f}m/s, {zVel[-1]:.2f}m/s")


    return [t,xLoc,yLoc,zLoc,xVel,yVel,zVel]
