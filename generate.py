# __________Import Statements__________
import pyrosim.pyrosim as pyrosim

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

def Create_Robot():
    # __________Name of file to store robot information__________
    pyrosim.Start_URDF("body.urdf")

    # __________Create the Root Link and Joint of the Robot__________
    pyrosim.Send_Cube(name="Link0", pos=[x, y, z], size=[length, width, height])

    # __________Create the Leg of the Robot__________
    pyrosim.Send_Cube(name="Link1", pos=[0.5, 0, .5], size=[length, width, height])

    # __________Link the Torso and Leg__________
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0.5, 0, 1])

    # __________Close the Robot File__________
    pyrosim.End()

#==============================================================================================================
#__________Main Code__________
Create_World()
Create_Robot()

