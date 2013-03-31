from helpers.cat import SquareCatPhysicsDelegate
from helpers.delegate import System


if __name__=='__main__':
    system = System(SquareCatPhysicsDelegate)
    system.makeVideo(3)
