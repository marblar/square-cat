from delegate import SphereJointPhysicsDelegate
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
        self.rotator = self.rotatorJoint(*joint_pairs[1])
        self.joints = [self.ballJoint(*x) for x in joint_pairs]
        self.rotator.setParam(ode.ParamFMax,10)
        self.rotator.setParam(ode.ParamVel,1)

    def prepareWorld(self,world,nframe):
        pass
