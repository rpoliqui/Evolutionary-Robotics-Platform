#__________Import Statements__________
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import numpy
import random

class WORLD:

    def __init__(self, world_file):
        # Define floor normal force
        self.planeId = p.loadURDF("plane.urdf")

        # Load the world file
        p.loadSDF(world_file)