import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

os.system("del brain*.nndf")

os.system("del fitness*.nndf")

phc = PARALLEL_HILL_CLIMBER()

phc.Evolve()

phc.Show_Best()
