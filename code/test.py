# pyODE example 2: Connecting bodies with joints

import pygame
from pygame.locals import *
import ode

pygame.init()

WIDTH=1024
HEIGHT=768
CENTER_X=400
CENTER_Y=500
srf = pygame.display.set_mode((WIDTH,HEIGHT))

def coord(x,y):
    "Convert world coordinates to pixel coordinates."
    return int(round(WIDTH/2+(WIDTH/5)*x)), int(round(3*HEIGHT/4-(WIDTH/5)*y))

# Create a world object
world = ode.World()
world.setGravity((0,-9.81,0))

# Create two bodies
body1 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body1.setMass(M)
body1.setPosition((1,2,0))

body2 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body2.setMass(M)
body2.setPosition((2,2,0))

# Connect body1 with the static environment
j1 = ode.BallJoint(world)
j1.attach(body1, ode.environment)
j1.setAnchor( (0,2,0) )

# Connect body2 with body1
j2 = ode.BallJoint(world)
j2.attach(body1, body2)
j2.setAnchor( (1,2,0) )

# Simulation loop...
fps = 60
dt = 1.0/fps
loopFlag = True

framecount = 0
while loopFlag and framecount*dt < 10:
    events = pygame.event.get()
    for e in events:
        if e.type==QUIT:
            loopFlag=False
        if e.type==KEYDOWN:
            loopFlag=False

    # Clear the screen
    srf.fill((146,179,87))

    # Draw the two bodies
    x1,y1,z1 = body1.getPosition()
    x2,y2,z2 = body2.getPosition()
    pygame.draw.circle(srf, (148,61,90), coord(x1,y1), 20, 0)
    pygame.draw.circle(srf, (232,97,135), coord(x1,y1), 17, 0)
    pygame.draw.line(srf, (62,100,120), coord(0,2), coord(x1,y1), 4)
    pygame.draw.circle(srf, (148,61,90), coord(x2,y2), 20, 0)
    pygame.draw.circle(srf, (232,97,135), coord(x2,y2), 17, 0)
    pygame.draw.line(srf, (62,100,120), coord(x1,y1), coord(x2,y2), 4)

    pygame.display.flip()

    pygame.image.save(srf,"frame%04d.png" % framecount)
    framecount = framecount + 1
    # Next simulation step
    world.step(dt)

    # Try to keep the specified framerate    
#    clk.tick(fps)
