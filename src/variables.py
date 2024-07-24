import numpy as np
from functions import *

# Parameters
windInfo = [7.77,40,100,0.1]

# Object Info (mass (kg), initial alt (m), initial z-axis speed (m/s), area of sides, cD)
objCube = [100,25000,-5,1,1.28]

# Plotting Utilities
dt = 1 # seconds
resolution = 1000
maxAlt = 50000

altRange = np.linspace(0,maxAlt,resolution)
properties = getProperties(altRange)
winds = getWinds(altRange,windInfo)
fall = simFall(objCube,windInfo,dt)
