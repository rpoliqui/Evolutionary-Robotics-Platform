#__________Import Statements__________
import pybullet as p
import pybullet_data
import constants as c
import time
import os
from world import WORLD
from robot import ROBOT

class SIMULATION:

    def __init__(self, directOrGUI, solutionID):
        self.debug_mode = True
        self.world_file = f"world{solutionID}.sdf"
        self.robot_file = f"body{solutionID}.urdf"
        self.solutionID = solutionID

        # Connect to GUI
        self.directOrGUI = directOrGUI
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        # Define data path for additional objects (Floor Plane)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # Enter debug visuals if in debug mode
        if self.debug_mode:
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        print("===========================================================\n")

        # Create World
        self.world = WORLD(self.world_file)

        # Define gravity force
        p.setGravity(0,0,-c.gravity)

        # Create Robot
        self.robot = ROBOT(self.robot_file, solutionID)

        if self.directOrGUI != 'GUI':
            os.system(f"del {self.robot_file}")
            os.system(f"del {self.world_file}")
            os.system(f"del brain{solutionID}.nndf")

    def Run(self):
        #__________Simulation Loop__________
        #=================================================================================================================
        print(f"Starting Simulation {self.solutionID}")
        for t in range(c.loop_iterations):
            # Step Simulation
            p.stepSimulation()

            self.robot.Sense(t)

            self.robot.Think()

            self.robot.Act(t)

            #print(t)

            # Sleep
            if self.directOrGUI == 'GUI':
                time.sleep(c.loop_delay)
        print(f"Finished Simulation {self.solutionID}")

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()