# __________Import Statements__________
import pyrosim.pyrosim as pyrosim
import random

# __________Global Variables_________
# Define Box Dimensions
length = 1
width = 1
height = 1
# Define Box Location
x = 0
y = 0
z = height / 2

# __________Custom Functions__________
def Create_World():
    # __________Name of file to store world information__________
    pyrosim.Start_SDF("world.sdf")

    # __________Add a Box to the World__________
    pyrosim.Send_Cube(name="Box", pos=[-2, 2, z], size=[length, width, height])

    # __________Close the World File__________
    pyrosim.End()

def Generate_Body():
    # __________Name of file to store robot information__________
    pyrosim.Start_URDF("body.urdf")

    # __________Create the Root (Torso)__________
    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[length, width, height])

    # __________Create the Legs of the Robot__________
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1, 0, 1])

    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0, 1])

    # __________Close the Robot File__________
    pyrosim.End()

def Generate_Brain():
    # __________Name of file to store robot information__________
    pyrosim.Start_NeuralNetwork("brain.nndf")

    # __________Create Neurons__________
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    # __________Create Synapses__________
    # pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=3, weight=0.5)
    # pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=3, weight=-1)
    # pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=-1)
    # pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=0.5)

    for sensor in range(0,3):
        for motor in range(3,5):
            pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=(2*random.random())-1)



    # __________Close the Robot File__________
    pyrosim.End()

def Create_Robot():
    Generate_Body()

    Generate_Brain()


#==============================================================================================================
#__________Main Code__________
Create_World()
Create_Robot()

