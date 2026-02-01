#__________Import Statements__________
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy
import random

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

# Define sinusoidal array
BackLeg_amplitude = -numpy.pi/4
BackLeg_frequency = 9
BackLeg_phaseOffset = 0
BackLeg_x = numpy.linspace(0, 2*numpy.pi, loop_iterations)
BackLeg_targetAngles = BackLeg_amplitude * numpy.sin((BackLeg_frequency * BackLeg_x) + BackLeg_phaseOffset)

FrontLeg_amplitude = -numpy.pi/4
FrontLeg_frequency = 9
FrontLeg_phaseOffset = 0
FrontLeg_x = numpy.linspace(0, 2*numpy.pi, loop_iterations)
FrontLeg_targetAngles = FrontLeg_amplitude * numpy.sin((FrontLeg_frequency * FrontLeg_x) + FrontLeg_phaseOffset)
numpy.save("data\BackLegTargetAngles.npy", BackLeg_targetAngles)
numpy.save("data\FrontLegTargetAngles.npy", FrontLeg_targetAngles)

#__________Simulation Loop__________
#=================================================================================================================
for step in range(loop_iterations):
    # Step Simulation
    p.stepSimulation()

    # Read Sensor Data
    backLegSensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    # Update Motors
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_BackLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=BackLeg_targetAngles[step],
        maxForce=50)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_FrontLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=FrontLeg_targetAngles[step],
        maxForce=50)

    # Sleep
    time.sleep(1./1000000.)

#_________Simulation End__________
#=================================================================================================================
print("\n=====================Ending Simulation=====================")
numpy.save("data\BackLegSensorValues.npy", backLegSensorValues)
numpy.save("data\FrontLegSensorValues.npy", frontLegSensorValues)
p.disconnect()
print("===========================================================\n")

