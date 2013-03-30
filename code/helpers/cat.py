from delegate import SphereJointPhysicsDelegate
import itertools
import collections

def shift(x,n=1):
    dq = collections.deque(x)
    dq.rotate(n)
    return list(dq)

class SquareCatPhysicsDelegate(SphereJointPhysicsDelegate):
    def initializeWorld(self):
        self.world.setGravity((0,0,0))
        mass = itertools.repeat((2500,0.05))
        positions = [ (0,0,0), (1,0,0), (1,1,0),(0,1,0) ]
        self.spheres = self.createSphericalBodies(positions)
        joint_pairs = zip(self.spheres,shift(self.spheres))
        self.rotator = self.motorJoint(*joint_pairs[0])
        self.joints = [self.rotator]
        self.joints = self.joints + [self.ballJoint(*x) for x in joint_pairs[1:]]
        self.rotator = self.joints[0];
        self.rotator.setNumAxes(3);
        self.rotator.setAxis(0,0,(100,100,0))
    
    def prepareWorld(self,world,nframe):
        self.rotator.setAxis(0,0,(100,100,0))
