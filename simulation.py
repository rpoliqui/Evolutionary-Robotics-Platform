#__________Import Statements__________
import pybullet as p
import time

#__________Simulation Setup__________
print("====================Starting Simulation====================")
physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
print("===========================================================")

#__________Simulation Loop__________
for step in range(1000):
    p.stepSimulation()
    print(step)
    time.sleep(1./240.)

#_________Simulation End__________
print("=====================Ending Simulation=====================")
p.disconnect()
print("===========================================================")
