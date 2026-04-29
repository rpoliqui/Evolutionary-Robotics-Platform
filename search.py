import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from parallelHillClimber import PARALLEL_HILL_CLIMBER

CONTINUE = False

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

if CONTINUE:
    try:
        phc_A = joblib.load('PHC_A.joblib')
        print("=" * 50)
        print(f"Continuing From Last Run of {phc_A.total_generations} Generations")
        print("=" * 50)
    except FileNotFoundError:
        phc_A = PARALLEL_HILL_CLIMBER('A')
else:
    phc_A = PARALLEL_HILL_CLIMBER('A')

phc_A.Evolve()

phc_A.Plot_Data()

print("="*50)
print("Evolving Robot B")
print("="*50)

if CONTINUE:
    try:
      phc_B = joblib.load('PHC_B.joblib')
      print("=" * 50)
      print(f"Continuing From Last Run of {phc_B.total_generations}")
      print("=" * 50)
    except FileNotFoundError:
      phc_B = PARALLEL_HILL_CLIMBER('B')

else:
    phc_B = PARALLEL_HILL_CLIMBER('B')


phc_B.Evolve()

phc_B.Plot_Data()

print("="*50)
print("Showing Results")
print("="*50)

phc_A.Show_Best()
phc_A.fitness_data_file.close()
phc_A.fitness_data_file = None
joblib.dump(phc_A, 'PHC_A.joblib')

phc_B.Show_Best()
phc_B.fitness_data_file.close()
phc_B.fitness_data_file = None
joblib.dump(phc_B, 'PHC_B.joblib')

print("="*50)
print("Plotting Data")
print("="*50)

df_A = pd.read_csv("fitness_data_A.csv")
df_B = pd.read_csv("fitness_data_B.csv")

df = pd.merge(df_A, df_B, on='Generation')

df.plot(x="Generation", y=["Max Fitness A", "Max Fitness B"])
plt.savefig("Max Fitness AB")

df.plot(x="Generation", y=["Average Fitness A", "Average Fitness B"])
plt.savefig("Average Fitness AB")