#__________Import Statements__________
import pybullet as p
import time

#__________Simulation Setup__________
print("====================Starting Simulation====================")
physicsClient = p.connect(p.GUI)
#p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
print("===========================================================")

# Define gravity force
p.setGravity(0,0,-9.8)

# Load the world file
p.loadSDF("box.sdf")

#__________Simulation Loop__________
for step in range(1000):
    p.stepSimulation()
    print(step)
    time.sleep(1./1000.)

#_________Simulation End__________
print("=====================Ending Simulation=====================")
p.disconnect()
print("===========================================================")
