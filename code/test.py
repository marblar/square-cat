# pyODE example 2: Connecting bodies with joints
import pygame
import ode
from helpers.canvas import System, PhysicsDelegate, coord
import itertools
from helpers.colors import *

class DoublePendulumDelegate(PhysicsDelegate):
    def initializeWorld(self):
        self.world.setGravity((0,-9.81,0))
        mass = itertools.repeat((2500,0.05))
        positions = [ (1,2,0), (2,2,0) ]
        self.body1, self.body2 = self.createSphericalBodiesWithMassesAtPositions(mass,positions)
        self.j1 = self.ballJointOnBodyWithAnchor(self.body1,(0,2,0))
        self.j2 = self.ballJointOnBodies(self.body1,self.body2)

    def prepareWorld(self,step,nframe):
        pass

    @property
    def joints(self):
        return [self.j1,self.j2]

    @property
    def spheres(self):
        return [self.body1,self.body2]

    def draw(self,canvas):
        canvas.fill(LightBlue)
        self.drawJoints(self.joints,canvas)
        self.drawSpheres(self.spheres,canvas)

if __name__ == "__main__":
    system = System(DoublePendulumDelegate)
    system.makeVideo(10)
