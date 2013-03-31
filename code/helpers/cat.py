from delegate import SphereJointPhysicsDelegate,angle,difference
import itertools
import collections
import ode

def shift(x,n=1):
    dq = collections.deque(x)
    dq.rotate(n)
    return list(dq)

class SquareCatPhysicsDelegate(SphereJointPhysicsDelegate):
    def initializeWorld(self):
        self.world.setGravity((0,0,0))
        mass = itertools.repeat((2500,0.05))
        positions = [ (0,0,0), (1,0,0) , (1,1,0), (0,1,0)]
        self.spheres = self.createSphericalBodies(positions)
        joint_pairs = zip(self.spheres,shift(self.spheres))
        self.joint_pairs = joint_pairs
        self.joints = [self.prJoint(*x) for x in joint_pairs] 
        self.motors = self.joints[::2]
        for joint in self.joints:
            joint.setParam(ode.ParamFMax,1)
            joint.setParam(ode.ParamFMax2,1)
            joint.setParam(ode.ParamHiStop2,3.14/2-.1)
            joint.setParam(ode.ParamHiStop,2)
            joint.setParam(ode.ParamLoStop,0)

        self.startUnwind()

    def reset(self):
        for joint in self.joints:
            joint.setParam(ode.ParamVel,0)
            joint.setParam(ode.ParamVel2,0)
            joint.setParam(ode.ParamFMax2,1)
            joint.setParam(ode.ParamFMax,3)

    def startWind(self):
        self.reset()
        for rotator in self.joints:
            if rotator in self.motors:
                rotator.setParam(ode.ParamFMax2,0)
            else:
                rotator.setParam(ode.ParamVel2,3)

    def startUnwind(self):
        self.reset()
        for rotator in self.joints:
            if rotator in self.motors:
                rotator.setParam(ode.ParamFMax2,0)
            else:
                rotator.setParam(ode.ParamVel2,-3)

    def startPush(self):
        self.reset()
        for rotator in self.motors:
            rotator.setParam(ode.ParamVel,-3)

    def startPull(self):
        self.reset()
        for rotator in self.motors:
            rotator.setParam(ode.ParamVel,3)

    def prepareWorld(self,world,nframes):
        pass


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
            switch = {
                0 : lambda: self.startPush(),
                1 : lambda: self.startWind(),
                2 : lambda: self.startPull(),
                3 : lambda: self.startUnwind(),
                4 : lambda: endCat()
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

push = 0
wind = 1
pull = 2
unwind = 3
stop = 4

def makeCycles(phaseLength=40,count=1):
    cycles = []
    time = 0
    for k in range(count):
        cycles = cycles + [
            (phaseLength,push),
            (phaseLength,wind),
            (phaseLength,pull),
            (phaseLength,unwind)
        ]
        time = time + phaseLength*5
    cycles = cycles + [(phaseLength,stop)]
    print cycles
    return cycles
