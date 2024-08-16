import pygame

# Draw Edges
def drawEdges(objProjection,window,color):
    for i in range(4):
        pygame.draw.line(window,color,objProjection[i],objProjection[(i+1)%4])
        pygame.draw.line(window,color,objProjection[i+4],objProjection[((i+1)%4) + 4])
        pygame.draw.line(window,color,objProjection[i],objProjection[i+4])

    return