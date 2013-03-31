from helpers.cat import SquareCatPhysicsDelegate
from helpers.delegate import System

class TestCatDelegate(SquareCatPhysicsDelegate):
    pass

if __name__=='__main__':
    system = System(TestCatDelegate)
    system.makeVideo(3)
