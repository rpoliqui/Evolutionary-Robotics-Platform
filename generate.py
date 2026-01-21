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

# Create the cube objects
for i in range(5):
    for j in range(5):
        for k in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])
            last_height = height
            length *= 0.9
            width *= 0.9
            height *= 0.9
            z += (last_height + height)/2
        y += 1
        length = 1
        width = 1
        height = 1
        z = height/2
    x += 1
    y = 0


#__________Close the World File__________
pyrosim.End()