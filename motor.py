import constants as c
import numpy
from pyrosim import pyrosim
import pybullet as p

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName

    def Set_Value(self, robotId, desiredAngle):
        # Update Motors
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.max_joint_force)
