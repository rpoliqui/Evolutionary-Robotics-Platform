import matplotlib.pyplot
import numpy

# Load Data
backLegData = numpy.load("data\BackLegSensorValues.npy")
frontLegData = numpy.load("data\FrontLegSensorValues.npy")
BackLeg_targetAngles = numpy.load("data\BackLegTargetAngles.npy")
FrontLeg_targetAngles = numpy.load("data\FrontLegTargetAngles.npy")

# Plot Data
# matplotlib.pyplot.plot(backLegData, label="Back Leg", linewidth=3)
# matplotlib.pyplot.plot(frontLegData, label="Front Leg")
matplotlib.pyplot.plot(BackLeg_targetAngles, label="Back Leg Target Angles")
matplotlib.pyplot.plot(FrontLeg_targetAngles, label="Front Leg Target Angles")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()