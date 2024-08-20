import os
import json
import pygame
import numpy as np
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

# Retriving View Settings
with open(os.path.join(os.path.dirname(__file__), 'settings/view.json'),'r') as f:
    settings = json.load(f)
    resolution = settings['resolution']
    orbitSpeed = settings['orbitSensitivity']
    scale = settings['defaultScale']
    theta = settings['defaultTheta']
    phi = settings['defaultPhi']
    bodyAngle = settings['launchAngle']
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
orbiting = False
panning = False

# Main Loop
while True:
    clock.tick(100)
    textTheta = f"X Rotation: {theta:.2f} rad"
    textPhi = f"Y Rotation: {phi:.2f} rad"

    # Events
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

    # Updates
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

    # Drawing
    window.fill(colors['white']) # clear screen
    pygame.draw.circle(window,colors['black'],origin,3) # draw origin
    drawObject(objProjection,window,colors['red'],colors['black']) # draw object

    drawText("Inertial Frame:",fontHead,window,colors['black'],[0,0])
    drawText(textTheta,fontNorm,window,colors['black'],[0,24])
    drawText(textPhi,fontNorm,window,colors['black'],[0,42])

    # Constants
    pygame.mouse.set_cursor(cursor)
    pygame.display.update()
