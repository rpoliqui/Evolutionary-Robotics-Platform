import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import numpy
import random

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName

        self.values = numpy.zeros(c.loop_iterations)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        numpy.save(f"data\sensor_{self.linkName}", self.values)