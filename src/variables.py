import numpy as np
from functions import *

# Parameters
windSpeed = 7.77
windDirection = 220
windAlt = 100
terrainRoughness = 0.1

# Object Info (mass (kg), initial alt (m), initial v-speed (m/s))
obj = [100, 5000, 5]

# Plotting Utilities
resolution = 1000
maxAlt = 50000
altRange = np.linspace(0,maxAlt,resolution)
properties = getProperties(altRange)
winds = getWinds(altRange,windSpeed,windDirection,windAlt,terrainRoughness)
fall = simFall(properties,winds,obj,1)
