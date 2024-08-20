import numpy as np

# Equations of Motion
def v(v0,a,dt):
    return v0 + a*dt

def dx(v0,a,dt):
    return v0*dt + 0.5*a*(dt**2)

def drag(rho,A,cD,v):
    return (0.5*rho*A*cD*(v**2))

# Properties of Air
def airProperties(z):
    if z < 11000: # Troposphere
        temperature = 15.04 - 0.00649*z
        pressure = 101.29*((temperature + 273.1)/288.08)**5.256

    elif z < 25000 and z > 11000: # Lower Stratosphere
        temperature = -56.46
        pressure = 22.65*np.exp(1.73 - 0.000157*z)

    else: # Upper Stratosphere
        pressure = 2.488*((temperature + 273.1)/216.6)**(-11.388)
    
    density = pressure/(0.2869*(temperature + 273.1))
    
    return [temperature,pressure,density]

# Rotation Functions (RADIANS not DEGREES)
def rotateX(theta):
    Rx = np.matrix([
        [1,0,0],
        [0,np.cos(theta),-np.sin(theta)],
        [0,np.sin(theta),np.cos(theta)]
    ])

    return Rx

def rotateY(phi):
    Ry = np.matrix([
        [np.cos(phi),0,np.sin(phi)],
        [0,1,0],
        [-np.sin(phi),0,np.cos(phi)]
    ])

    return Ry

def rotateZ(psi):
    Rz = np.matrix([
        [np.cos(psi),-np.sin(psi),0],
        [np.sin(psi),np.cos(psi),0],
        [0,0,1]
    ])
    
    return Rz

# Projection
def pointProjection(pos):
    P = np.matrix([
        [1,0,0],
        [0,1,0],
        [0,0,0]
    ])

    return np.dot(P,pos)