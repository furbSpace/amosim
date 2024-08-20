import numpy as np

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