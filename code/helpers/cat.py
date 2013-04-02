
from delegate import SphereJointPhysicsDelegate,angle,difference,length,border,fill,defaultColor,jointDistance,jointAngle,jointVectors,angle3
from itertools import chain, repeat
import collections
import ode
from cat_actions import *
from colors import *

def shift(x,n=1):
    dq = collections.deque(x)
    dq.rotate(n)
    return list(dq)

class SquareCatPhysicsDelegate(SphereJointPhysicsDelegate):
    def initializeWorld(self):
        headColor = {border:DarkBlue,fill:LightGreen}
        self.colors = list(chain(repeat(defaultColor,2),
                            repeat(headColor,1),
                            repeat(defaultColor,1)
                            ))
        self.servoMode = False
        self.world.setGravity((0,0,0))
        mass = repeat((2500,0.05))
        positions = [ (0,0,0), (1,0,0) , (1,1,0), (0,1,0)]
        self.spheres = self.createSphericalBodies(positions)
        joint_pairs = zip(self.spheres,shift(self.spheres))
        self.joint_pairs = joint_pairs
        self.joints = [self.prJoint(*x) for x in joint_pairs] 
        self.motors = self.joints[1::2]
        for joint in self.joints:
            joint.setParam(ode.ParamFMax,9)
            joint.setParam(ode.ParamFMax2,9)
            joint.setParam(ode.ParamHiStop2,3.14/2-.1)
            joint.setParam(ode.ParamLoStop2,-3.14/2+.1)
            joint.setParam(ode.ParamHiStop,1)
            joint.setParam(ode.ParamLoStop,-.5)

        distances = [jointDistance(x) for x in self.joints]
        angles = self.getAngles()
        self.startingPosition = zip(distances,angles)

    def getAngles(self):
        triplets = zip(shift(self.spheres,-1),self.spheres,shift(self.spheres,1))
        vTriplets = [map(lambda sphere: sphere.getPosition(),spheres) for spheres in triplets]
        angles = [angle3(x,y,z) for x,y,z in vTriplets]
        print angles
        return angles

    @property
    def windVelocity(self):
        return 3

    @property
    def pushVelocity(self):
        return 3

    @property
    def maxForce(self):
        return 9

    def reset(self):
        self.servoMode = False
        for joint in self.joints:
            joint.setParam(ode.ParamVel,0)
            joint.setParam(ode.ParamVel2,0)
            joint.setParam(ode.ParamFMax2,self.maxForce)
            joint.setParam(ode.ParamFMax,self.maxForce)

    def startWind(self):
        self.reset()
        for rotator in self.joints:
            if rotator in self.motors:
                rotator.setParam(ode.ParamFMax2,0)
            else:
                rotator.setParam(ode.ParamVel2,self.windVelocity)

    def startUnwind(self):
        self.reset()
        for rotator in self.joints:
            if rotator in self.motors:
                rotator.setParam(ode.ParamFMax2,0)
            else:
                rotator.setParam(ode.ParamVel2,-self.windVelocity)

    def startPush(self):
        self.reset()
        for rotator in self.motors:
            rotator.setParam(ode.ParamVel,-self.pushVelocity)

    def startPull(self):
        self.reset()
        for rotator in self.motors:
            rotator.setParam(ode.ParamVel,self.pushVelocity)
    
    def startSquare(self):
        self.reset()
        self.servoMode = True

    def prepareWorld(self,world,nframes):
        if self.servoMode:
            Gain = 5;
            for motor,startingParams,actualAngle in zip(self.joints,self.startingPosition,self.getAngles()):
                targetDistance,targetAngle = startingParams
                actualDistance = jointDistance(motor)
                distanceError = actualDistance - targetDistance
                angleError = actualAngle - targetAngle
                
                newVelocity = -distanceError * Gain
                newAngularVelocity = - angleError * Gain

                motor.setParam(ode.ParamVel, newVelocity)
                motor.setParam(ode.ParamVel2, newAngularVelocity)

def endCat():
    raise StopIteration()

class ProgrammableCat(SquareCatPhysicsDelegate):
        def initializeWorld(self):
            SquareCatPhysicsDelegate.initializeWorld(self)
            self.instructions = self.getInstructions()
            self.last_transition = 0

        @property
        def current_instruction(self):
            return self.instructions[0]

        def popInstruction(self):
            self.instructions.pop(0)

        def prepareWorld(self,world,nframes):
            super(ProgrammableCat,self).prepareWorld(world,nframes)
            switch = {
                0 : lambda: self.startPush(),
                1 : lambda: self.startWind(),
                2 : lambda: self.startPull(),
                3 : lambda: self.startUnwind(),
                4 : lambda: endCat(),
                5 : lambda: self.startSquare()
            }
            (duration,action) = self.current_instruction
            
            if nframes == 1:
                switch[action]()
                self.popInstruction()
                return 

            if nframes - self.last_transition >= duration:
                switch[action]()
                self.popInstruction()
                self.last_transition = nframes
                print action, "#################################"

        def getInstructions(self):
            raise Exception()

def makeCycles(phaseLength=40,count=1):
    cycles = []
    time = 0
    for k in range(count):
        cycles = cycles + [
            (phaseLength,push),
            (phaseLength,wind),
            (phaseLength,pull),
            (phaseLength,unwind),
            (phaseLength,square)
        ]
        time = time + phaseLength*5
    cycles = cycles + [(phaseLength,stop)]
    print cycles
    return cycles
