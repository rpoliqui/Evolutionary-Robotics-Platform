#__________Import Statements__________
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy

#__________Global Variables__________
debug_mode = True
loop_iterations = 1000
world_file = "world.sdf"
robot_file = "body.urdf"

#__________Simulation Setup__________
#=================================================================================================================
print("\n====================Starting Simulation====================")
# Connect to GUI
physicsClient = p.connect(p.GUI)

# Define data path for additional objects (Floor Plane)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Enter debug visuals if in debug mode
if debug_mode:
    p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
print("===========================================================\n")

# Define gravity force
p.setGravity(0,0,-9.8)
# Define floor normal force
planeId = p.loadURDF("plane.urdf")

# Load robot into the environment
robotId = p.loadURDF(robot_file)

# Load the world file
p.loadSDF(world_file)

# Prepare the robot for simulation
pyrosim.Prepare_To_Simulate(robotId)

# Create vector to store sensor data
backLegSensorValues = numpy.zeros(loop_iterations)
frontLegSensorValues = numpy.zeros(loop_iterations)

#__________Simulation Loop__________
#=================================================================================================================
for step in range(loop_iterations):
    p.stepSimulation()
    backLegSensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    time.sleep(1./60.)

#_________Simulation End__________
#=================================================================================================================
print("\n=====================Ending Simulation=====================")
numpy.save("data\BackLegSensorValues.npy", backLegSensorValues)
numpy.save("data\FrontLegSensorValues.npy", frontLegSensorValues)
p.disconnect()
print("===========================================================\n")

