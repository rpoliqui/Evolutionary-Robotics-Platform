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
        self.fitness_data_file.writelines("Generation,Max Fitness,Average Fitness\n")
        for parent in range(c.populationSize):
            self.parents[parent] = SOLUTION(self.nextAvailableID, version)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
             self.Evolve_For_One_Generation(currentGeneration)

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
        for parent in self.parents.values():
            running_total += parent.fitness
            if parent.fitness > max_fitness:
                max_fitness = parent.fitness
        self.fitness_data_file.writelines(f"{currentGeneration},{max_fitness},{running_total/c.populationSize}\n")

    def Plot_Data(self):
        self.fitness_data_file.close()
        df = pd.read_csv(self.fitness_data_filename)
        df.plot(x="Generation", y="Max Fitness")
        plt.savefig("Max Fitness")
        df.plot(x="Generation", y="Average Fitness")
        plt.savefig("Average Fitness")

    def Evolve_For_One_Generation(self, currentGeneration):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Save_Data(currentGeneration)
        self.Print()
        print(f"Generation {currentGeneration+1} of {c.numberOfGenerations}")
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