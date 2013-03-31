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
        self.rotator = self.rotatorJoint(*joint_pairs[0])
        self.joints = [self.ballJoint(*x) for x in joint_pairs] 

        self.motors = [self.motorJoint(*joint_pairs[0])]
    
        self.rotator.setAxis((0,0,1))
        self.rotator.setParam(ode.ParamFMax,100)
        self.rotator.setParam(ode.ParamVel,-3)
        self.rotator.setParam(ode.ParamHiStop,3.14/2-.1)
        self.rotator.setParam(ode.paramLoStop,-3.14/2-.1)

    def enableMotors(self):
        for motor in self.motors:
            print motor
            motor.setParam(ode.ParamFMax,100)
            motor.setParam(ode.ParamVel,-1)

    def disableMotors(self):
        for motor in self.motors:
            motor.setParam(ode.ParamFMax,0)

    def prepareWorld(self,world,nframe):
        pass
