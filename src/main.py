import numpy as np
import matplotlib.pyplot as plt

N = 10000
maxAlt = 10000

z,dz = np.linspace(0,maxAlt,N,retstep=True)

print(z[4])
print(dz)
