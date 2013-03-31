from helpers.cat import ProgrammableCat
from helpers.cat_actions import *
from helpers.delegate import System
import itertools

class TestCat(ProgrammableCat):
    def getInstructions(self):
        return zip(itertools.repeat(75,10),itertools.cycle([push,pull])) + [(55,end)]

if __name__=='__main__':
    system = System(TestCat)
    system.makeVideo(1000)
