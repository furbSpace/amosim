import pygame

# Draw Object
def drawObject(objProjection,window,pointColor,lineColor):
    # Edges
    for i in range(4):
        pygame.draw.line(window,lineColor,objProjection[i],objProjection[(i+1)%4])
        pygame.draw.line(window,lineColor,objProjection[i+4],objProjection[((i+1)%4) + 4])
        pygame.draw.line(window,lineColor,objProjection[i],objProjection[i+4])

    # Points
    for n in range(len(objProjection)):
        pygame.draw.circle(window,pointColor,objProjection[n],5)

    return

# Draw Text
def drawText(text,font,window,color,pos):
    txt = font.render(text,True,color)
    window.blit(txt,pos)

    return