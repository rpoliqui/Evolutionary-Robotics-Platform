import constants as c
import numpy
from pyrosim import pyrosim
import pybullet as p

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName

        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency =  c.frequency
        self.offset = c.phaseOffset
        if self.jointName == b'Torso_FrontLeg':
            self.frequency /= 2

        x = numpy.linspace(0, 2*numpy.pi, c.loop_iterations)
        self.motorValues = self.amplitude * numpy.sin((self.frequency * x) + self.offset)

    def Set_Value(self, robotId, desiredAngle):
        # Update Motors
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.max_joint_force)

    def Save_Values(self):
        numpy.save(f"data\sensor_{self.jointName}", self.motorValues)