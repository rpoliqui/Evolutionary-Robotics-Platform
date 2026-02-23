from simulation import SIMULATION

simulation = SIMULATION()

simulation.Run()



#
# # Create vector to store sensor data
#
# frontLegSensorValues = numpy.zeros(c.loop_iterations)
#
# # Define sinusoidal array
# BackLeg_x = numpy.linspace(0, 2*numpy.pi, c.loop_iterations)
# BackLeg_targetAngles = c.BackLeg_amplitude * numpy.sin((c.BackLeg_frequency * BackLeg_x) + c.BackLeg_phaseOffset)
#
# FrontLeg_x = numpy.linspace(0, 2*numpy.pi, c.loop_iterations)
# FrontLeg_targetAngles = c.FrontLeg_amplitude * numpy.sin((c.FrontLeg_frequency * FrontLeg_x) + c.FrontLeg_phaseOffset)
# # numpy.save("data\BackLegTargetAngles.npy", BackLeg_targetAngles)
# # numpy.save("data\FrontLegTargetAngles.npy", FrontLeg_targetAngles)
#

#
# #_________Simulation End__________
# #=================================================================================================================
# print("\n=====================Ending Simulation=====================")
# numpy.save("data\BackLegSensorValues.npy", backLegSensorValues)
# numpy.save("data\FrontLegSensorValues.npy", frontLegSensorValues)
# print("===========================================================\n")
#
