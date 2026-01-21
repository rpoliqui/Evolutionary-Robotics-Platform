#__________Import Statements__________
import pybullet as p
import pybullet_data
import time

#__________Global Variables__________
debug_mode = True
world_file = "boxes.sdf"

#__________Simulation Setup__________
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

# Load the world file
p.loadSDF(world_file)

#__________Simulation Loop__________
for step in range(2000):
    p.stepSimulation()
    print(step)
    time.sleep(1./60.)

#_________Simulation End__________
print("\n=====================Ending Simulation=====================")
p.disconnect()
print("===========================================================\n")
