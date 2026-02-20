#__________Import Statements__________
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import numpy
import random

class ROBOT:

    def __init__(self, robot_file):
        self.sensors = {}
        self.motors = {}

        # Load robot into the environment
        self.robotId = p.loadURDF(robot_file)

        # Prepare the robot for simulation
        pyrosim.Prepare_To_Simulate(self.robotId)