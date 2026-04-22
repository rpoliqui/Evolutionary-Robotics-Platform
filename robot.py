#__________Import Statements__________
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
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

        self.fallTime = 0

        self.Prepare_To_Sense()

        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")

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
            # if hand is touching the ground, increment hand contact time
            if (sensor == 'LeftHand' or sensor == 'RightHand') and self.sensors[sensor].values[t]==1:
                self.fallTime += 1
            if sensor == 'Torso' and self.sensors[sensor].values[t]==1:
                self.fallTime += 2


    def Think(self):
        self.nn.Update(self.robotId)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = c.motorJointRange*self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Get_Fitness(self):
        # Get Data from Simulation
        position, orientation = p.getBasePositionAndOrientation(self.robotId)

        xPosition = position[0]

        zPosition = position[2]

        roll, pitch, yaw = p.getEulerFromQuaternion(orientation)

        roll = np.rad2deg(roll)
        pitch = np.rad2deg(pitch)
        yaw = np.rad2deg(yaw)

        orientationError = np.sqrt(roll ** 2 + pitch ** 2)

        fallRate = self.fallTime / c.loop_iterations

        fitness = (xPosition+5) * zPosition / orientationError

        with open(f"tmp{self.solutionID}.txt", "w") as f:
            f.write(str(fitness))
        os.system(f"rename tmp{self.solutionID}.txt fitness{self.solutionID}.txt")