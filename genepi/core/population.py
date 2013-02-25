from copy import copy, deepcopy

class Population(object):
    """A population is a collection of individuals"""

    individuals = []
    size = 100

    def __init__(self, protogenome, size=100, optimization_mode='min', **kwargs):
        
        self.protogenome = protogenome
        self.size = size
        self.optimization_mode=optimization_mode
        
        self.generation_number = 0
        self.sorted = False
    
    
    def initialize(self, individuals=[]):
        
        new_individuals = []
        for individual in individuals:
            new_individual = individual.copy()
            new_individuals.append(new_individual)

        self.individuals = new_individuals
        start_index = len(self.individuals)
        
        for x in range(start_index, self.size):
            individual = self.protogenome.get_genome()
            self.individuals.append(individual)
            
    def evolve(self):
        pass
        
    def cmp_individual(self, a, b):
        #TODO: document, this is a bit tricky
        if self.optimization_mode == 'min':
            return cmp(a.score, b.score)
        else:
            return cmp(b.score, a.score)
        
    def sort(self):
        self.individuals.sort(self.cmp_individual)
        self.sorted = True
    
    
    def best_individual(self):
        if not self.sorted:
            self.sort()
        return self.individuals[0]
        
        
    def copy(self):
        individuals = []
        for individual in self.individuals:
            new_individual = individual.copy()
            individuals.append(new_individual)
        
        pop = Population(self.protogenome, self.size, 
            optimization_mode=self.optimization_mode)
        pop.initialize(individuals)
        
        
        
    