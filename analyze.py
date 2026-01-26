import matplotlib.pyplot
import numpy

# Load Data
backLegData = numpy.load("data\BackLegSensorValues.npy")
frontLegData = numpy.load("data\FrontLegSensorValues.npy")

# Plot Data
matplotlib.pyplot.plot(backLegData, label="Back Leg", linewidth=3)
matplotlib.pyplot.plot(frontLegData, label="Front Leg")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()