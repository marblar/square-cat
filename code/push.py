from helpers.cat import ProgrammableCat, makeCycles
from helpers.delegate import System
from helpers.cat_actions import *
import itertools

class TestCat(ProgrammableCat):
    def getInstructions(self):
        return zip(itertools.repeat(75,10),itertools.cycle([wind,unwind])) + [(75,end)]

if __name__=='__main__':
    system = System(TestCat)
    system.makeVideo(1000)
