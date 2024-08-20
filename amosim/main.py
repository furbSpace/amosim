import os
import json
import pygame
import numpy as np
import scipy as sp
from equations import *
from utilities import *

# Clearing Console
if os.name == 'nt':
    os.system('cls')
elif os.name == 'posix':
    os.system('clear')

# Retriving Desired Object
with open(os.path.join(os.path.dirname(__file__), 'data/objects.json'),'r') as f:
    objects = json.load(f)
    objectTypes = objects.keys()

    # Objects Selection
    print("Objects Loaded:")
    objectCounter = 0
    for obj in objectTypes:
        print(f"{objectCounter+1}. {obj}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    objSelection = input("Please type the name of object you would like to observe: ").lower()

    # Input Validation
    while any(objSelection in objectTypes for i in objectTypes) == False: 
        print("Error, please try again!\n")
        objSelection = input("Please type the name of object you would like to observe: ").lower()
    obj = np.matrix(objects[objSelection])

    f.close()

# Retrieving Initial Parameters
with open(os.path.join(os.path.dirname(__file__), 'data/initial.json'), 'r') as f:
    parameters = json.load(f)
    height = parameters['launchHeight']
    bodyAngle = parameters['launchAngle']
    bodyVelocity = parameters['launchVelocity']

    f.close()

# Retriving View Settings
with open(os.path.join(os.path.dirname(__file__), 'settings/view.json'),'r') as f:
    settings = json.load(f)
    resolution = settings['resolution']
    orbitSpeed = settings['orbitSensitivity']
    scale = settings['defaultScale']
    theta = settings['defaultTheta']
    phi = settings['defaultPhi']
    origin = np.divide(resolution,2)

    f.close()

# Retriving Colors
with open(os.path.join(os.path.dirname(__file__), 'settings/colors.json'),'r') as f:
    colors = json.load(f)

    f.close()

pygame.init()

# Pygame Configuration
pygame.display.set_caption("Amosim")
window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
cursor = pygame.SYSTEM_CURSOR_ARROW
fontHead = pygame.font.SysFont('Arial', 24)
fontNorm = pygame.font.SysFont('Arial', 18)
fps = 100
orbiting = False
panning = False

# Main Loop
while True:
    clock.tick(fps)

    #
    # Events
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Orbit & Pan Camera
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cursorX, cursorY = event.pos
            if event.button == 1:
                cursor = pygame.SYSTEM_CURSOR_CROSSHAIR
                orbiting = True

            elif event.button == 2:
                cursor = pygame.SYSTEM_CURSOR_SIZEALL
                panning = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                cursor = pygame.SYSTEM_CURSOR_ARROW
                orbiting = False
            
            elif event.button == 2:
                cursor = pygame.SYSTEM_CURSOR_ARROW
                panning = False

        elif event.type == pygame.MOUSEMOTION:
            if orbiting:
                phi = phi + ((event.pos)[0]-cursorX) * orbitSpeed
                theta = theta + ((event.pos)[1]-cursorY) * orbitSpeed

                if abs(phi) >= 2*np.pi:
                    phi = 2*np.pi - abs(phi)
                
                if abs(theta) >= 2*np.pi:
                    theta = 2*np.pi - abs(theta)

            elif panning:
                origin[0] = origin[0] + ((event.pos)[0]-cursorX)
                origin[1] = origin[1] + ((event.pos)[1]-cursorY)

            cursorX, cursorY = event.pos

        # Zoom
        if event.type == pygame.MOUSEWHEEL:
            scale = scale + event.y

    #
    # Updates
    #
    objProjection = []
    for point in obj:
        # Apply Body Rotations
        pos = np.dot(rotateX(bodyAngle[0]),np.transpose(point))
        pos = np.dot(rotateY(bodyAngle[1]),pos)
        pos = np.dot(rotateZ(bodyAngle[2]),pos)

        # Apply Inertial Rotations (Orbiting Camera)
        pos = np.dot(rotateX(theta),pos)
        pos = np.dot(rotateY(phi),pos)

        # Record Projection
        projection = pointProjection(pos)
        x = scale*projection[0,0] + origin[0]
        y = scale*projection[1,0] + origin[1]
        objProjection.append([x,y])

    if height > 0:
        height = height + dx(bodyVelocity[2],-sp.constants.g,1/fps)
        bodyVelocity[2] = v(bodyVelocity[2],-sp.constants.g,1/fps)

    air = airProperties(height)

    # Object Data
    textHeight = f"Height: {height:.2f}m"
    textVelocityX = f"X Velocity: {bodyVelocity[0]:.2f}m/s"
    textVelocityY = f"Y Velocity: {bodyVelocity[1]:.2f}m/s"
    textVelocityZ = f"Z Velocity: {bodyVelocity[2]:.2f}m/s"
    textAngleX = f"X Rotation: {bodyAngle[0]:.2f}rad"
    textAngleY = f"Y Rotation: {bodyAngle[1]:.2f}rad"
    textAngleZ = f"Z Rotation: {bodyAngle[2]:.2f}rad"

    # Air Properties
    textTemperature = f"Temperature: {air[0]:.2f}C"
    textPressure = f"Pressure: {air[1]:.2f}kPa"
    textDensity = f"Density: {air[2]:.2f}kg/m3"

    #
    # Drawing
    #
    window.fill(colors['white']) # clear screen
    pygame.draw.circle(window,colors['black'],origin,3) # draw origin
    drawObject(objProjection,window,colors['red'],colors['black']) # draw object

    # Object Data
    drawText("Object Info:",fontHead,window,colors['black'],[0,0])
    drawText(textHeight,fontNorm,window,colors['black'],[0,24])
    drawText(textAngleX,fontNorm,window,colors['black'],[0,42])
    drawText(textAngleY,fontNorm,window,colors['black'],[0,60])
    drawText(textAngleZ,fontNorm,window,colors['black'],[0,78])
    drawText(textVelocityX,fontNorm,window,colors['black'],[0,96])
    drawText(textVelocityY,fontNorm,window,colors['black'],[0,114])
    drawText(textVelocityZ,fontNorm,window,colors['black'],[0,132])

    # Air Properties
    drawText("Air Info:",fontHead,window,colors['black'],[0,resolution[1]/2])
    drawText(textTemperature,fontNorm,window,colors['black'],[0,resolution[1]/2 + 24])
    drawText(textPressure,fontNorm,window,colors['black'],[0,resolution[1]/2 + 42])
    drawText(textDensity,fontNorm,window,colors['black'],[0,resolution[1]/2 + 60])

    pygame.mouse.set_cursor(cursor)
    pygame.display.update()
