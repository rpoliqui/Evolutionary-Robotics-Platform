import pybullet as p
physicsClient = p.connect(p.GUI)
for step in range(1000):
    p.stepSimulation()
p.disconnect()