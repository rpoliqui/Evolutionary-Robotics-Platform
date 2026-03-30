#__________Import Statements__________
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
import os
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self, robot_file, solutionID):
        # Load robot into the environment
        self.robotId = p.loadURDF(robot_file)
        self.solutionID = solutionID

        # Prepare the robot for simulation
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()

        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")

        self.Prepare_To_Act()

        os.system(f"del brain{solutionID}.nndf")

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

    def Think(self):
        self.nn.Update()

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = c.motorJointRange*self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        with open(f"tmp{self.solutionID}.txt", "w") as f:
            f.write(str(xCoordinateOfLinkZero))
        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")