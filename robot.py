#__________Import Statements__________
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self, robot_file):
        # Load robot into the environment
        self.robotId = p.loadURDF(robot_file)

        # Prepare the robot for simulation
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()

        self.nn = NEURAL_NETWORK("brain.nndf")

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

    def Think(self):
        self.nn.Update()
        self.nn.Print()

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)