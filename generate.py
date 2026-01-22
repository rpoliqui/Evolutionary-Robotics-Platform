import pyrosim.pyrosim as pyrosim

#__________Custom Functions__________
def Create_World():
    # __________Name of file to store world information__________
    pyrosim.Start_SDF("world.sdf")

    # __________Add a Box to the World__________
    # Define Box Dimensions
    length = 1
    width = 1
    height = 1
    # Define Box Location
    x = 0
    y = 0
    z = height / 2
    # Create the cube object
    pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])

    # __________Close the World File__________
    pyrosim.End()

def Create_Robot():
    # __________Name of file to store robot information__________
    pyrosim.Start_URDF("body.urdf")

    # __________Close the Robot File__________
    pyrosim.End()

#==============================================================================================================
#__________Main Code__________
Create_World()

