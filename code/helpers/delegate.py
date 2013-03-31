import pygame
import ode
from pygame.locals import *
from colors import *
import itertools
import inspect
import os
import __main__


WIDTH=1024
HEIGHT=768
CENTER_X=400
CENTER_Y=500
fps=60
dt=1.0/fps

class System(object):
    def __init__(self,DelegateClass):
        pygame.init()
        self.world = ode.World()
        self.canvas = Canvas()
        self.delegate = DelegateClass(self.world)
        self.framecount = 0

    def step(self):
        self.delegate.prepareWorld(self.world,self.framecount)
        self.world.step(dt)
        self.delegate.draw(self.canvas)
        pygame.display.flip()
        pygame.image.save(self.canvas,"frame%04d.png" % self.framecount)
        self.framecount = self.framecount + 1
        return self.framecount

    def makeVideo(self,duration):
        frames = int(duration*fps)
        name = os.path.basename(__main__.__file__)

        def log(step):
            print "%s: Writing frame %s of %s" % (name,step,frames)

        try:
            map(lambda x: log(self.step()),range(0,frames))
        except StopIteration:
            return True

class PhysicsDelegate(object):
    def __init__(self,world):
        self.world = world
        self.initializeWorld()
          
    def initializeWorld(self):
        raise NotImplementedError("PhysicsDelegate must implement prepareWorld")

    def prepareWorld(self,world,nframe):
        raise NotImplementedError("PhysicsDelegate must implement prepareworld")

    def draw(self,canvas):
        raise NotImplementedError("DrawingDelegate must implement draw")

    def createSphericalBodyWithMass(self,x,y):
        world = self.world
        M = ode.Mass()
        M.setSphere(x,y)
        body = ode.Body(world)
        body.setMass(M)
        return body

    def createSphericalBodies(self,positions,masses=itertools.repeat((2500,0.05))):
        def create(params):
            (mass,position) = params
            body = self.createSphericalBodyWithMass(*mass)
            body.setPosition(position)
            return body
        return map(create,itertools.izip(masses,positions))
        
    def ballJoint(self,body1,body2=ode.environment,anchor=None):
        joint = ode.BallJoint(self.world)
        joint.attach(body1,body2)
        if body2 == ode.environment and not anchor:
            raise Exception("You must provide an anchor point for environment-anchored spheres.")
        return joint

    def motorJoint(self,body1,body2=ode.environment,anchor=None):
        joint = ode.LMotor(self.world)
        joint.attach(body1,body2)
        joint.setNumAxes(1)
        joint.setAxis(0,1,(0,1,0))
        if body2 == ode.environment and not anchor:
            raise Exception("You must provide an anchor point for environment-anchored spheres.")
        return joint

    def rotatorJoint(self,body1,body2):
        joint = ode.HingeJoint(self.world)
        joint.attach(body1,body2)
        return joint

    def slideJoint(self,body1,body2):
        joint = ode.PistonJoint(self.world)
        joint.attach(body1,body2)
        return joint

    def drawSphere(self,body,canvas):
        pygame.draw.circle(canvas,DarkGreen,coord(*body.getPosition()),20,0)
        pygame.draw.circle(canvas,LightGreen,coord(*body.getPosition()),17,0)
        
    def drawJoint(self,joint,canvas):
        pos1 = joint.getBody(0).getPosition() if joint.getBody(0) else joint.getAnchor()
        pos2 = joint.getBody(1).getPosition() if joint.getBody(1) else joint.getAnchor2()
        coord1 = coord(*pos1)
        coord2 = coord(*pos2)
        pygame.draw.line(canvas,DarkPink,coord1,coord2,4)

    def drawJoints(self,items,canvas):
        def draw(item):
            self.drawJoint(item,canvas)
        map(draw,items)
    
    def drawSpheres(self,items,canvas):
        def draw(item):
            self.drawSphere(item,canvas)
        map(draw,items)
    
    def relativeAngle(self,leftPair,rightPair):
        pos1 = relativePosition(leftPair[1],leftPair[0])
        pos2 = relativePosition(rightPair[0],rightPair[1])

        return angle(pos1,pos2)

import math

def relativePosition(left,right):
    positions = [x.getPosition() for x in [left,right]]
    return tuple([(x-y) for x,y in zip(*positions)])

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))) if length(v1) and length(v2) else 0

def difference(v1,v2):
    return tuple([x-y for x,y in zip(v1,v2)])

class SphereJointPhysicsDelegate(PhysicsDelegate):
    def draw(self,canvas):
        canvas.fill(LightBlue)
        self.drawJoints(self.joints,canvas)
        self.drawSpheres(self.spheres,canvas)

def Canvas():
    return pygame.display.set_mode((WIDTH,HEIGHT))

def coord(x,y,z):
    if z:
        raise Exception()
    "Convert world coordinates to pixel coordinates."
    return int(round(WIDTH/2+(WIDTH/5)*x)), int(round(3*HEIGHT/4-(WIDTH/5)*y))

