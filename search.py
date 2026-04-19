import os
import pandas as pd
import matplotlib.pyplot as plt
from parallelHillClimber import PARALLEL_HILL_CLIMBER

print("="*50)
print("Clearing Old Files")
print("="*50)

os.system("del brain*.nndf")

os.system("del body*.urdf")

os.system("del world*.sdf")

os.system("del fitness*.txt")

print("="*50)
print("Evolving Robot A")
print("="*50)

phc_A = PARALLEL_HILL_CLIMBER('A')

phc_A.Evolve()

phc_A.Plot_Data()

print("="*50)
print("Evolving Robot B")
print("="*50)

# phc_B = PARALLEL_HILL_CLIMBER('B')
#
# phc_B.Evolve()

# phc_B.Plot_Data()

print("="*50)
print("Showing Results")
print("="*50)

phc_A.Show_Best()

# phc_B.Show_Best()

print("="*50)
print("Plotting Data")
print("="*50)

# df_A = pd.read_csv("fitness_data_A.csv")
# df_B = pd.read_csv("fitness_data_B.csv")
#
# df = pd.merge(df_A, df_B, on='Generation')
#
# df.plot(x="Generation", y=["Max Fitness A", "Max Fitness B"])
# plt.savefig("Max Fitness AB")
#
# df.plot(x="Generation", y=["Average Fitness A", "Average Fitness B"])
# plt.savefig("Average Fitness AB")