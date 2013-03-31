from helpers.cat import ProgrammableCat, makeCycles
from helpers.delegate import System

class TestCat(ProgrammableCat):
    def getInstructions(self):
        return makeCycles(count=5,phaseLength=80)

if __name__=='__main__':
    system = System(TestCat)
    system.makeVideo(1000)
