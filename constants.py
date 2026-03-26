import numpy

#==================== Loop Constants ====================
loop_iterations = 1000
loop_delay = 1/1000.

#==================== Robot Constants ====================
max_joint_force = 50

numSensorNeurons = 9
numMotorNeurons = 8

amplitude = -numpy.pi/4
frequency = 8.8
phaseOffset = 0

#==================== Environment Constants ====================
gravity = 9.8

#==================== Evolution Constants ====================
numberOfGenerations = 1
populationSize = 10
