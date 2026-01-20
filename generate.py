import pyrosim.pyrosim as pyrosim

# __________Name of file to store world information__________
pyrosim.Start_SDF("box.sdf")

#__________Add a Box to the World__________
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[1,1,1])

#__________Close the World File__________
pyrosim.End()