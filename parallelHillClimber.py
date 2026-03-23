from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        self.nextAvailableID = 0
        self.parents = {}
        for parent in range(c.populationSize):
            self.parents[parent] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
             self.Evolve_For_One_Generation()

    def Show_Best(self):
        min_fitness = float("inf")
        best_solution = 0
        for parent in self.parents.values():
            if parent.fitness < min_fitness:
                min_fitness = parent.fitness
                best_solution = parent
        best_solution.Start_Simulation("GUI")
        best_solution.Wait_For_Simulation_To_End()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
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
            if self.children[key].fitness <= self.parents[key].fitness:
                self.parents[key] = copy.deepcopy(self.children[key])

    def Print(self):
        print("")
        for parent in self.parents:
            print(self.parents[parent].fitness, self.children[parent].fitness)
        print("")