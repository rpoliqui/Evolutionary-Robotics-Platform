import numpy

#==================== Loop Constants ====================
loop_iterations = 1000
loop_delay = 1/1000.

#==================== Robot Constants ====================
max_joint_force = 75

numSensorNeurons = 8
numMotorNeurons = 16
numBodyParams = 20

amplitude = -numpy.pi/4
frequency = 8.8
phaseOffset = 0

motorJointRange = 0.75

#==================== Environment Constants ====================
gravity = 9.81

#==================== Evolution Constants ====================
numberOfGenerations = 50
populationSize = 20
