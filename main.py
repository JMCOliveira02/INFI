import sys
sys.path.insert(0, "..")

from mes.manager import Manager
from utils import *




if __name__ == "__main__":

    printAuthorsCredits()

    manager = Manager(CONSTANTS["opcua_connection"], CONSTANTS["max_recipes"])

    manager.spin()