"""Contains genetic algorithm glasses"""

from genepi.core.population import Population
from genepi.cache.base import BaseCache, DictCache

class GeneticAlgorithm(object):
    """Genetic algorithm class"""
    
    population_size = 100
    selection_method = None
    step_callback = None
    termination_criteria = None
    
    fitness_evaluator = None
    optimization_mode = 'min'
    
    mutation_probability = 0
    crossover_probability = 0
    
    def __init__(self, 
                    protogenome,
                    fitness_evaluator,
                    population_size=population_size,
                    optimization_mode='min',
                    termination_criteria=None,
                    selection_method=None,
                    step_callback=None,
                    mutation_probability=0,
                    crossover_probability=0,
                    crossover_method=None,
                    cache_instance=None):

        self.protogenome = protogenome
        self.fitness_evaluator = fitness_evaluator
        self.population_size = population_size
        self.optimization_mode = optimization_mode
        self.termination_criteria = termination_criteria
        self.step_callback = step_callback
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.crossover_method = crossover_method
        
        self.population = Population(self.protogenome,
            size=self.population_size, 
            selection_method=self.selection_method,
            crossover_probability=self.crossover_probability, 
            crossover_method=self.crossover_method, 
            mutation_probability=self.mutation_probability)

        self.generation = 0
        
        if cache_instance is None:
            self.cache = DictCache()
        else:
            self.cache = cache_instance
        
    
    def initialize(self):
        self.population.initialize()
        self.cache.initialize()
        if self.storage:
            self.storage.initialize()
        
        
    def should_terminate(self):
        if type(self.termination_criteria) == type(list()):
            for criterium in self.termination_criteria:
                if criterium(self):
                    return True
        else:
            if self.termination_criteria(self):
                return True
                
        return False
        
    def store_individual(self, hash, individual):
        if self.storage:    
            self.storage.write_individual(hash, self.generation, individual )

        
    def evaluate_population(self):
        self.population.fit_individuals(self.fitness_evaluator, self.cache, eval_callback=self.store_individual)
        self.stat_population()
        
        
    def stat_population(self):
        #TODO: implement
        """stats for current population: min max average etc.."""
        stats = {}
        self.population_stats[self.generation] = stats
        if self.storage:
            self.storage.write_population_stats(self.generation, stats)
        

    def best_individual(self):
        return self.population.best_individual()
        
        
    def evolve_population(self):
        new_population = self.population.evolve()
        self.population = new_population
        self.generation = new_population.generation_number
         
    
    def evolve(self):
        if not self.termination_criteria:
            raise TypeError("You Must set one or more termination criteria")
        
        self.initialize()
        self.evaluate_population()
        
        while 1:
            if self.should_terminate():
                break
            self.evolve_population()
            self.evaluate_population()
                      
        
        return self.best_individual()
            
    