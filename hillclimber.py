from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:

    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate("GUI")

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

        self.Show_Best()

    def Show_Best(self):
        self.parent.Evaluate("GUI")

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        print("")
        print(self.parent.fitness,self.child.fitness)
        if self.child.fitness <= self.parent.fitness:
            self.parent = copy.deepcopy(self.child)