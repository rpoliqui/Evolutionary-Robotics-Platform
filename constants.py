import numpy

#==================== Loop Constants ====================
loop_iterations = 1000
loop_delay = 1/100.

#==================== Robot Constants ====================
max_joint_force = 75

numSensorNeurons = 5
numMotorNeurons = 16
numBodyParams = 20

amplitude = -numpy.pi/4
frequency = 8.8
phaseOffset = 0

motorJointRange = 0.75

#==================== Environment Constants ====================
gravity = 9.81

#==================== Evolution Constants ====================
numberOfGenerations = 150
populationSize = 20
