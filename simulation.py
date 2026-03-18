#__________Import Statements__________
import pybullet as p
import pybullet_data
import constants as c
import time
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

            self.robot.Think()

            self.robot.Act(t)

            #print(t)

            # Sleep
            time.sleep(c.loop_delay)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()