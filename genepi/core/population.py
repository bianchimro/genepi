from copy import copy, deepcopy
import random

#TODO: move to SELECTORS module
def select_from_top(population, num_individuals):
    return population.individuals[:num_individuals]

#TODO: move to CROSSOVER module    
def genome_add(genome_a, genome_b):
    return genome_a + genome_b
    

class Population(object):
    """A population is a collection of individuals"""

    individuals = []
    size = 100

    def __init__(self, protogenome, size=100, **options):
        
        self.protogenome = protogenome
        self.size = size
        
        self.options = options
        self.optimization_mode=options.get('optimization_mode', 'min')
        
        #number of selected parents
        self.num_parents = options.get('num_parents', 2)
        #elitism
        self.elitism = options.get('elitism', True)
        
        #selection method
        self.selection_method = options.get('selection_method', select_from_top)
        
        #crossover method
        self.crossover_method = options.get('crossover_method', genome_add)
        
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
    
            
    def select_individuals(self):
        return self.selection_method(self, self.num_parents)
    
    
    def fit_individuals(self, fitness_evaluator, cache=None, eval_callback= None):
        for individual in self.individuals:
            hash = individual.get_hash()
            if cache:
                score = cache.get_score(hash)
            else:
                score = None
            if not score:
                score = fitness_evaluator(individual)
                if cache:
                    cache.set_score(hash, score)
            individual.score = score
            if eval_callback:
                eval_callback(hash, individual)
    
        self.sort()
        
            
    def evolve(self):
        new_individuals = []
        num_individuals = 0
        
        parents_candidates = self.select_individuals()
        if self.elitism:
            for individual in parents_candidates:
                new_individuals.append(individual.copy())
            
        while num_individuals < self.size:
            #breeding and crossover
            parents = random.sample(parents_candidates, 2)
            new_individual = self.crossover_method(parents[0], parents[1])
            #mutation
            new_individual.mutate()
            new_individuals.append(individual)
            num_individuals += 1
    
        new_population = self.copy(individuals=new_individuals)
        
        new_population.generation_number = self.generation_number + 1
        return new_population
        
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
        
        
    def copy(self, individuals=[]):
        if not individuals:
            for individual in self.individuals:
                new_individual = individual.copy()
                individuals.append(new_individual)
        
        pop = Population(self.protogenome, self.size, **self.options) 
        return pop
        
        
        
    