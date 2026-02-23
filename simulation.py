#__________Import Statements__________
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import numpy
import random
from world import WORLD
from robot import ROBOT

class SIMULATION:

    def __init__(self):
        self.debug_mode = True
        self.world_file = "world.sdf"
        self.robot_file = "body.urdf"

        # Connect to GUI
        self.physicsClient = p.connect(p.GUI)

        # Define data path for additional objects (Floor Plane)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # Enter debug visuals if in debug mode
        if self.debug_mode:
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        print("===========================================================\n")

        # Define gravity force
        p.setGravity(0,0,-c.gravity)

        # Create World
        self.world = WORLD(self.world_file)

        # Create Robot
        self.robot = ROBOT(self.robot_file)

    def Run(self):
        #__________Simulation Loop__________
        #=================================================================================================================
        for t in range(c.loop_iterations):
            # Step Simulation
            p.stepSimulation()

            self.robot.Sense(t)

            print(t)

            # # Read Sensor Data
            # backLegSensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[step] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            #
            # # Update Motors
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex=robotId,
            #     jointName=b'Torso_BackLeg',
            #     controlMode=p.POSITION_CONTROL,
            #     targetPosition=BackLeg_targetAngles[step],
            #     maxForce=c.max_joint_force)
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex=robotId,
            #     jointName=b'Torso_FrontLeg',
            #     controlMode=p.POSITION_CONTROL,
            #     targetPosition=FrontLeg_targetAngles[step],
            #     maxForce=c.max_joint_force)

            # Sleep
            time.sleep(c.loop_delay)
    def __del__(self):
        p.disconnect()