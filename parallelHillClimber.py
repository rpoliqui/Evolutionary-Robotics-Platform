import time

from matplotlib import pyplot as plt
from solution import SOLUTION
import constants as c
import copy
import pandas as pd

class PARALLEL_HILL_CLIMBER:

    def __init__(self, version):
        self.nextAvailableID = 0
        self.parents = {}
        self.fitness_data_filename = f"fitness_data_{version}.csv"
        self.fitness_data_file = open( self.fitness_data_filename, 'w')
        self.fitness_data_file.writelines(f"Generation,Max Fitness {version},Average Fitness {version}\n")
        self.version = version
        self.generations_completed = 0
        self.total_generations = 0
        for parent in range(c.populationSize):
            self.parents[parent] = SOLUTION(self.nextAvailableID, version)
            self.nextAvailableID += 1

    def Evolve(self):
        self.startTime = time.time()
        self.Evaluate(self.parents)
        self.total_generations += c.numberOfGenerations

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(self.generations_completed)
            self.generations_completed += 1

    def Show_Best(self):
        max_fitness = float("-inf")
        best_solution = 0
        for parent in self.parents.values():
            if parent.fitness > max_fitness:
                max_fitness = parent.fitness
                best_solution = parent
        best_solution.Start_Simulation("GUI")
        best_solution.Wait_For_Simulation_To_End()
        best_solution.Create_Brain()
        best_solution.Create_Body()
        best_solution.Create_World()

    def Save_Data(self, currentGeneration):
        max_fitness = float("-inf")
        running_total = 0
        if self.fitness_data_file is None:
            self.fitness_data_file = open(self.fitness_data_filename, 'a')
        for parent in self.parents.values():
            running_total += parent.fitness
            if parent.fitness > max_fitness:
                max_fitness = parent.fitness
        self.fitness_data_file.writelines(f"{currentGeneration},{max_fitness},{running_total/c.populationSize}\n")

    def Plot_Data(self):
        self.fitness_data_file.close()
        df = pd.read_csv(self.fitness_data_filename)
        df.plot(x="Generation", y=f"Max Fitness {self.version}")
        plt.savefig(f"Max Fitness {self.version}")
        df.plot(x="Generation", y=f"Average Fitness {self.version}")
        plt.savefig(f"Average Fitness {self.version}")

    def Evolve_For_One_Generation(self, currentGeneration):
        startTime = time.time()
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Save_Data(currentGeneration)
        self.Print()
        endTime = time.time()
        print(f"Generation {currentGeneration+1} of {self.total_generations}")
        print(f"Generation Time: {endTime-startTime} seconds")
        print(f"Total Time: {(endTime - self.startTime)/60} minutes ")
        self.Select()

    def Spawn(self):
        self.children = {}
        for parent in self.parents:
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation("DIRECT")
            time.sleep(0.1)  # small stagger between launches

        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()

    def Select(self):
        for key in self.parents:
            if self.children[key].fitness >= self.parents[key].fitness:
                self.parents[key] = copy.deepcopy(self.children[key])

    def Print(self):
        print("")
        for parent in self.parents:
            print(self.parents[parent].fitness, self.children[parent].fitness)
        print("")