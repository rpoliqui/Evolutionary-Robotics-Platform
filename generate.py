import pyrosim.pyrosim as pyrosim

# __________Name of file to store world information__________
pyrosim.Start_SDF("boxes.sdf")

#__________Add a Box to the World__________
# Define Box Dimensions
length = 1
width = 1
height = 1

# Define Box Location
x = 0
y = 0
z = height/2

# Create the cube object
pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])

x += 1
y = 0
z += 1
pyrosim.Send_Cube(name="Box2", pos=[x,y,z] , size=[length,width,height])

#__________Close the World File__________
pyrosim.End()