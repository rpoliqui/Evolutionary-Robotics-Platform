#__________Import Statements__________
import pybullet as p
import pybullet_data
import time

#__________Simulation Setup__________
print("\n====================Starting Simulation====================")
# Connect to GUI
physicsClient = p.connect(p.GUI)

# Define data path for additional objects (Floor Plane)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Uncomment line below to enable debug graphics
#p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
print("===========================================================\n")

# Define gravity force
p.setGravity(0,0,-9.8)
# Define floor normal force
planeId = p.loadURDF("plane.urdf")

# Load the world file
p.loadSDF("box.sdf")

#__________Simulation Loop__________
for step in range(1000):
    p.stepSimulation()
    print(step)
    time.sleep(1./1000.)

#_________Simulation End__________
print("\n=====================Ending Simulation=====================")
p.disconnect()
print("===========================================================\n")
