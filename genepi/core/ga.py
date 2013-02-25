"""Contains genetic algorithm glasses"""

from genepi.core.population import Population, POPULATION_DEFAULT_SIZE
from genepi.cache.base import BaseCache, DictCache
from genepi.core import stopcriteria

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
                    **options):
                 
        self.protogenome = protogenome
        self.fitness_evaluator = fitness_evaluator

        self.options = options
        self.population_size = options.get('population_size', POPULATION_DEFAULT_SIZE)
        
        self.optimization_mode = options.get('optimization_mode', 'min')
        self.termination_criteria = options.get('termination_criteria', None)
        if self.termination_criteria is None:
            self.termination_criteria = stopcriteria.convergence_stop
        
        self.step_callback = options.get('step_callback', None)
        
        #default crossover and selections are handled by population
        self.crossover_method = options.get('crossover_method', None)
        self.selection_method = options.get('selection_method', None)

        self.elitism = options.get('elitism', True)
        self.num_parents = options.get('num_parents', 2)
        
        cache_instance = options.get('cache_instance', None)
        if cache_instance is None:
            self.cache = DictCache()
        else:
            self.cache = cache_instance
        
        storage_instance = options.get('storage_instance', None)            
        if storage_instance:
            self.storage = storage_instance
        else:
            self.storage = None

        self.population = Population(self.protogenome,
                size=self.population_size, 
                optimization_mode=self.optimization_mode,
                selection_method=self.selection_method,
                crossover_method=self.crossover_method,
                elitism=self.elitism,
                num_parents=self.num_parents)

        self.generation = 0
        self.population_stats = {}

    
    def initialize(self):
        self.population.initialize()
        self.cache.initialize()
        if self.storage:
            self.storage.initialize()
        
        
    def should_terminate(self):
        if type(self.termination_criteria) == type(list()):
            for criterium in self.termination_criteria:
                if criterium(self, **self.options):
                    return True
        else:
            if self.termination_criteria(self, **self.options):
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
            
    