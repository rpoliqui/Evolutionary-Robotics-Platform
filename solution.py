import numpy
import random
import os
import time
import constants as c
from pyrosim import pyrosim

class SOLUTION:

    def __init__(self, ID, version):
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.myID = ID

        self.version = version

        self.start_position = -5

        # Body Variables
        self.torso_width = 0.75
        self.torso_height = 1
        self.torso_depth = 0.4

        self.head_size = 0.5

        self.shoulder_size = 0.3

        self.bicep_size = 0.25
        self.bicep_length = 0.5

        self.forearm_size = 0.25
        self.forearm_length = 0.5

        self.pelvis_size = 0.25
        self.pelvis_width = 0.5

        self.hip_size = 0.25

        self.quad_size = 0.25
        self.quad_length = 0.75

        self.shin_size = 0.25
        self.shin_length = 0.5

        self.foot_width = 0.3
        self.foot_length = 0.5
        self.foot_height = 0.1

        self.hand_size = 0.3

        self.torso_position = self.foot_height + self.shin_length + self.quad_length + self.pelvis_size + (self.torso_height/2)

        self.body_parameters = [self.torso_width,
                                self.torso_height,
                                self.torso_depth,
                                self.head_size,
                                self.shoulder_size,
                                self.bicep_size,
                                self.bicep_length,
                                self.forearm_size,
                                self.forearm_length,
                                self.pelvis_size,
                                self.pelvis_width,
                                self.hip_size,
                                self.quad_size,
                                self.quad_length,
                                self.shin_size,
                                self.shin_length,
                                self.foot_width,
                                self.foot_length,
                                self.foot_height,
                                self.hand_size]


    def Start_Simulation(self, directOrGui):
        self.Create_World()
        self.Create_Brain()
        self.Create_Body()

        os.system("start /B python3 simulate.py " + directOrGui + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"

        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        time.sleep(0.01)
        fitnessFile = open(fitnessFileName)
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system(f"del {fitnessFileName}")


    def Create_World(self):
        # __________Name of file to store world information__________
        pyrosim.Start_SDF(f"world{self.myID}.sdf")

        # __________Close the World File__________
        pyrosim.End()

        # __________Make Sure File Exists__________
        while not os.path.exists(f"world{self.myID}.sdf"):
            time.sleep(0.01)

    def Create_Body(self):
        # __________Name of file to store robot information__________
        pyrosim.Start_URDF(f"body{self.myID}.urdf")

        # __________Create the Root (Torso)__________
        pyrosim.Send_Cube(name="Torso", pos=[self.start_position, 0, self.torso_position], size=[self.body_parameters[2], self.body_parameters[0], self.body_parameters[1]])

        # __________Create Connections to Torso__________
        pyrosim.Send_Cube(name="Head", pos=[0, 0, self.body_parameters[3]/2], size=[self.body_parameters[3], self.body_parameters[3], self.body_parameters[3]])
        pyrosim.Send_Joint(name="Torso_Head", parent="Torso", child="Head", type="revolute", position=[self.start_position, 0, self.torso_position+(self.body_parameters[1]/2)], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LeftShoulder", pos=[0, -self.body_parameters[4]/2, 0], size=[self.body_parameters[4], self.body_parameters[4], self.body_parameters[4]])
        pyrosim.Send_Joint(name="Torso_LeftShoulder", parent="Torso", child="LeftShoulder", type="revolute", position=[self.start_position, -self.body_parameters[0]/2, self.torso_position + (self.body_parameters[1] / 2) - (self.body_parameters[4]/2)], jointAxis="1 0 0")

        pyrosim.Send_Cube(name="RightShoulder", pos=[0, self.body_parameters[4] / 2, 0], size=[self.body_parameters[4], self.body_parameters[4], self.body_parameters[4]])
        pyrosim.Send_Joint(name="Torso_RightShoulder", parent="Torso", child="RightShoulder", type="revolute", position=[self.start_position, self.body_parameters[0] / 2, self.torso_position + (self.body_parameters[1] / 2) - (self.body_parameters[4] / 2)], jointAxis="1 0 0")

        pyrosim.Send_Cube(name="Pelvis", pos=[0, 0, -self.body_parameters[9] / 2], size=[self.body_parameters[9], self.body_parameters[10], self.body_parameters[9]])
        pyrosim.Send_Joint(name="Torso_Pelvis", parent="Torso", child="Pelvis", type="revolute", position=[self.start_position, 0, self.torso_position - (self.body_parameters[1] / 2)], jointAxis="0 0 1")

        # __________Create Lower Body__________
        pyrosim.Send_Cube(name="LeftHip", pos=[0, -self.body_parameters[11] / 2, 0], size=[self.body_parameters[11], self.body_parameters[11], self.body_parameters[11]])
        pyrosim.Send_Joint(name="Pelvis_LeftHip", parent="Pelvis", child="LeftHip", type="revolute", position=[0, -self.body_parameters[10]/2, -self.body_parameters[9]/2], jointAxis="1 0 0")

        pyrosim.Send_Cube(name="RightHip", pos=[0, self.body_parameters[11] / 2, 0], size=[self.body_parameters[11], self.body_parameters[11], self.body_parameters[11]])
        pyrosim.Send_Joint(name="Pelvis_RightHip", parent="Pelvis", child="RightHip", type="revolute", position=[0, self.body_parameters[10]/2, -self.body_parameters[9]/2], jointAxis="1 0 0")

        pyrosim.Send_Cube(name="LeftQuad", pos=[0, 0, -self.body_parameters[13]/2], size=[self.body_parameters[12], self.body_parameters[12], self.body_parameters[13]])
        pyrosim.Send_Joint(name="LeftHip_LeftQuad", parent="LeftHip", child="LeftQuad", type="revolute", position=[0, -self.body_parameters[11]/2, -self.body_parameters[11]/2], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightQuad", pos=[0, 0, -self.body_parameters[13]/2], size=[self.body_parameters[12], self.body_parameters[12], self.body_parameters[13]])
        pyrosim.Send_Joint(name="RightHip_RightQuad", parent="RightHip", child="RightQuad", type="revolute", position=[0, self.body_parameters[11]/2, -self.body_parameters[11]/2], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LeftShin", pos=[0, 0, -self.body_parameters[15]/2], size=[self.body_parameters[14], self.body_parameters[14], self.body_parameters[15]])
        pyrosim.Send_Joint(name="LeftQuad_LeftShin", parent="LeftQuad", child="LeftShin", type="revolute", position=[0, 0, -self.body_parameters[13]], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightShin", pos=[0, 0, -self.body_parameters[15]/2], size=[self.body_parameters[14], self.body_parameters[14], self.body_parameters[15]])
        pyrosim.Send_Joint(name="RightQuad_RightShin", parent="RightQuad", child="RightShin", type="revolute", position=[0, 0, -self.body_parameters[13]], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LeftFoot", pos=[self.body_parameters[17]/4, 0, -self.body_parameters[18]/2], size=[self.body_parameters[17], self.body_parameters[16], self.body_parameters[18]])
        pyrosim.Send_Joint(name="LeftShin_LeftFoot", parent="LeftShin", child="LeftFoot", type="revolute", position=[0, 0, -self.body_parameters[15]], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightFoot", pos=[self.body_parameters[17]/4, 0, -self.body_parameters[18]/2], size=[self.body_parameters[17], self.body_parameters[16], self.body_parameters[18]])
        pyrosim.Send_Joint(name="RightShin_RightFoot", parent="RightShin", child="RightFoot", type="revolute", position=[0, 0, -self.body_parameters[15]], jointAxis="0 1 0")

        # __________Create Upper Body__________
        pyrosim.Send_Cube(name="LeftBicep", pos=[0, 0, -self.body_parameters[6]/2], size=[self.body_parameters[5], self.body_parameters[5], self.body_parameters[6]])
        pyrosim.Send_Joint(name="LeftShoulder_LeftBicep", parent="LeftShoulder", child="LeftBicep", type="revolute", position=[0, -self.body_parameters[4]/2, -self.body_parameters[4]/2], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightBicep", pos=[0, 0, -self.body_parameters[6]/2], size=[self.body_parameters[5], self.body_parameters[5], self.body_parameters[6]])
        pyrosim.Send_Joint(name="RightShoulder_RightBicep", parent="RightShoulder", child="RightBicep", type="revolute", position=[0, self.body_parameters[4]/2, -self.body_parameters[4]/2], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LeftForearm", pos=[0, 0, -self.body_parameters[8]/2], size=[self.body_parameters[7], self.body_parameters[7], self.body_parameters[8]])
        pyrosim.Send_Joint(name="LeftBicep_LeftForearm", parent="LeftBicep", child="LeftForearm", type="revolute", position=[0, 0, -self.body_parameters[6]], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightForearm", pos=[0, 0, -self.body_parameters[8]/2], size=[self.body_parameters[7], self.body_parameters[7], self.body_parameters[8]])
        pyrosim.Send_Joint(name="RightBicep_RightForearm", parent="RightBicep", child="RightForearm", type="revolute", position=[0, 0, -self.body_parameters[6]], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LeftHand", pos=[0, 0, -self.body_parameters[19]/2], size=[self.body_parameters[19], self.body_parameters[19], self.body_parameters[19]])
        pyrosim.Send_Joint(name="LeftForearm_LeftHand", parent="LeftForearm", child="LeftHand", type="fixed", position=[0, 0, -self.body_parameters[8]], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RightHand", pos=[0, 0, -self.body_parameters[19]/2], size=[self.body_parameters[19], self.body_parameters[19], self.body_parameters[19]])
        pyrosim.Send_Joint(name="RightForearm_RightHand", parent="RightForearm", child="RightHand", type="fixed", position=[0, 0, -self.body_parameters[8]], jointAxis="0 1 0")

        # __________Close the Robot File__________
        pyrosim.End()

        # __________Make Sure File Exists__________
        while not os.path.exists(f"body{self.myID}.urdf"):
            time.sleep(0.01)

    def Create_Brain(self):
        # __________Name of file to store robot information__________
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # __________Create Neurons__________
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso", type="touch_sensor")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LeftFoot", type="touch_sensor")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="RightFoot", type="touch_sensor")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftHand", type="touch_sensor")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightHand", type="touch_sensor")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="Torso", type="orientation_pitch_sensor")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="Torso", type="orientation_roll_sensor")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="Torso", type="orientation_yaw_sensor")
        pyrosim.Send_Motor_Neuron(name=8, jointName="LeftShin_LeftFoot")
        pyrosim.Send_Motor_Neuron(name=9, jointName="RightShin_RightFoot")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftQuad_LeftShin")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightQuad_RightShin")
        pyrosim.Send_Motor_Neuron(name=12, jointName="LeftHip_LeftQuad")
        pyrosim.Send_Motor_Neuron(name=13, jointName="RightHip_RightQuad")
        pyrosim.Send_Motor_Neuron(name=14, jointName="Pelvis_LeftHip")
        pyrosim.Send_Motor_Neuron(name=15, jointName="Pelvis_RightHip")
        pyrosim.Send_Motor_Neuron(name=16, jointName="Torso_Pelvis")
        pyrosim.Send_Motor_Neuron(name=17, jointName="Torso_Head")
        pyrosim.Send_Motor_Neuron(name=18, jointName="Torso_LeftShoulder")
        pyrosim.Send_Motor_Neuron(name=19, jointName="Torso_RightShoulder")
        pyrosim.Send_Motor_Neuron(name=19, jointName="LeftShoulder_LeftBicep")
        pyrosim.Send_Motor_Neuron(name=20, jointName="RightShoulder_RightBicep")
        pyrosim.Send_Motor_Neuron(name=21, jointName="LeftBicep_LeftForearm")
        pyrosim.Send_Motor_Neuron(name=22, jointName="RightBicep_RightForearm")

        # __________Create Synapses__________
        for currentRow in range(0, c.numSensorNeurons):
            for currentColumn in range(0, c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, weight=self.weights[currentRow][currentColumn])

        # __________Close the Robot File__________
        pyrosim.End()

        # __________Make Sure File Exists__________
        while not os.path.exists(f"brain{self.myID}.nndf"):
            time.sleep(0.01)

    def Mutate(self):
        num_mutations = random.randint(1, 10)

        for mutation in range(0, num_mutations):
            if self.version == 'A':
                mutation_strategy = random.choice(["BRAIN"])
            elif self.version == 'B':
                mutation_strategy = random.choice(["BRAIN", "BRAIN", "BRAIN", "BRAIN", "BODY"])

            # Completely replace one neuron weight
            if mutation_strategy == "BRAIN":
                randomRow = random.randint(0, c.numSensorNeurons-1)
                randomColumn = random.randint(0, c.numMotorNeurons-1)
                self.weights[randomRow, randomColumn] = random.random() * 2 - 1

            elif mutation_strategy == "BODY":
                randomIndex = random.randint(0, c.numBodyParams-1)
                self.body_parameters[randomIndex] += random.random() * 2 * 0.1 - 0.1
                if self.body_parameters[randomIndex] <= 0:
                    self.body_parameters[randomIndex] = 0.001

    def Set_ID(self, ID):
        self.myID = ID