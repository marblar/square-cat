# pyODE example 2: Connecting bodies with joints
import pygame
import ode
from helpers.delegate import System, SphereJointPhysicsDelegate, coord
import itertools
from helpers.colors import *

class DoublePendulumDelegate(SphereJointPhysicsDelegate):
    def initializeWorld(self):
        self.world.setGravity((0,-9.81,0))
        positions = [ (1,2,0), (2,2,0) ]
        self.body1, self.body2 = self.createSphericalBodies(positions)
        self.j1 = self.ballJoint(self.body1,anchor=(0,2,0))
        self.j2 = self.ballJoint(self.body1,self.body2)

    def prepareWorld(self,step,nframe):
        pass

    @property
    def joints(self):
        return [self.j1,self.j2]

    @property
    def spheres(self):
        return [self.body1,self.body2]

if __name__ == "__main__":
    system = System(DoublePendulumDelegate)
    system.makeVideo(1)
