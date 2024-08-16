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
    objSelection = input("Please type the name of object you would like to observe: ")

    # Input Validation
    while any(objSelection in objectTypes for i in objectTypes) == False: 
        print("Error, please try again!\n")
        objSelection = input("Please type the name of object you would like to observe: ")
    obj = np.matrix(objects[objSelection])

    f.close()

# Retriving View Settings
with open(os.path.join(os.path.dirname(__file__), 'settings/view.json'),'r') as f:
    settings = json.load(f)
    resolution = settings['resolution']
    scale = settings['defaultScale']
    theta = settings['defaultTheta']
    phi = settings['defaultPhi']
    psi = settings['defaultPsi']
    origin = np.divide(resolution,2)

    f.close()

# Retriving Colors
with open(os.path.join(os.path.dirname(__file__), 'settings/colors.json'),'r') as f:
    colors = json.load(f)

    f.close()

# Pygame Configuration
pygame.display.set_caption("Amosim")
window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
cursor = pygame.SYSTEM_CURSOR_ARROW
orbiting = False
panning = False

# Main Loop
while True:
    clock.tick(100)

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
                phi = phi + 0.1*((event.pos)[0]-cursorX)
                psi = psi + 0.1*((event.pos)[1]-cursorY)
                
            elif panning:
                origin[0] = origin[0] + ((event.pos)[0]-cursorX)
                origin[1] = origin[1] + ((event.pos)[1]-cursorY)

            cursorX, cursorY = event.pos

        # Zoom
        if event.type == pygame.MOUSEWHEEL:
            scale = scale + event.y

    # Updates
    objProjection = []
    theta += 0.01
    phi += 0.01
    psi += 0.01

    # Drawing
    window.fill(colors['white']) # clear screen
    pygame.draw.circle(window,colors['black'],origin,3) # draw origin

    for vertex in obj:
        # Apply Rotations
        pos = np.dot(rotateX(theta),np.transpose(vertex))
        pos = np.dot(rotateY(phi),pos)
        pos = np.dot(rotateZ(psi),pos)

        # Record Projection
        projection = vertexProjection(pos)
        x = scale*projection[0,0] + origin[0]
        y = scale*projection[1,0] + origin[1]
        objProjection.append([x,y])

        # Draw Vertex
        pygame.draw.circle(window,colors['red'],objProjection[-1],5)

    # Draw Object Borders
    drawEdges(objProjection,window,colors['black'])

    # Constants
    pygame.mouse.set_cursor(cursor)
    pygame.display.update()
