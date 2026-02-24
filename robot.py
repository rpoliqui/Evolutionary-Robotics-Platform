#__________Import Statements__________
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self, robot_file):
        # Load robot into the environment
        self.robotId = p.loadURDF(robot_file)

        # Prepare the robot for simulation
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()

        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)


    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)

    def Act(self, t):
        for motor in self.motors:
            self.motors[motor].Set_Value(self.robotId, t)

    def Save_Values(self):
        for sensor in self.sensors:
            numpy.save(f"data\sensor_{self.sensors[sensor]}", self.sensors[sensor].Get_Value())
        # # numpy.save("data\BackLegTargetAngles.npy", BackLeg_targetAngles)
        # # numpy.save("data\FrontLegTargetAngles.npy", FrontLeg_targetAngles)
        #

        #
        # #_________Simulation End__________
        # #=================================================================================================================
        # print("\n=====================Ending Simulation=====================")
        #
        # numpy.save("data\FrontLegSensorValues.npy", frontLegSensorValues)
        # print("===========================================================\n")
        #