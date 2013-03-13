# pyODE example 2: Connecting bodies with joints

import ode
import pysvg
import collections

def coord(x, y):
    "Convert world coordinates to pixel coordinates."
    return 320 + 170 * x, 400 - 170 * y

# Create a world object
world = ode.World()
world.setGravity((0, -9.81, 0))

bodies = [ode.Body(world)] * 4

for (index, body) in enumerate(bodies):
    x = index % 2
    y = index / 2
    body.setPosition((x, y, 0))
    M = ode.Mass()
    M.setSphere(1.0, 5)
    body.setMass(M)


def rotate(l, n):
    return l[-n:] + l[:-n]


for (body1,body2) in zip(bodies,rotate(bodies,1)):
    j2 = ode.BallJoint(world)
    j2.attach(body1,body2)

# Simulation loop...

fps = 60
dt = 1.0 / fps

while loopFlag:
    # Clear the screen
    srf.fill((255, 255, 255))

    # Draw the two bodies
    x1, y1, z1 = body1.getPosition()
    x2, y2, z2 = body2.getPosition()
    pygame.draw.circle(srf, (55, 0, 200), coord(x1, y1), 20, 0)
    pygame.draw.line(srf, (55, 0, 200), coord(0, 2), coord(x1, y1), 2)
    pygame.draw.circle(srf, (55, 0, 200), coord(x2, y2), 20, 0)
    pygame.draw.line(srf, (55, 0, 200), coord(x1, y1), coord(x2, y2), 2)

    pygame.display.flip()

    # Next simulation step
    world.step(dt)

    # Try to keep the specified framerate
    clk.tick(fps)
