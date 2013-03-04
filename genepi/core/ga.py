"""
This module contains genetic algorithm class
"""

from genepi.core.population import Population, POPULATION_DEFAULT_SIZE
from genepi.cache.base import BaseCache, DictCache
from genepi.core import stopcriteria


class GeneticAlgorithm(object):
    """
    Genetic algorithm class
    
    :param protogenome: instance of :class:`genepi.core.protogenome.Protogenome`
    :param population_size: size of the population
    
    
    """
    
    population_size = 100
    selection_method = None
    step_callback = None
    termination_criteria = None
    
    fitness_evaluator = None
    optimization_mode = 'min'
    
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
        self.crossover_probability = options.get('crossover_probability', 0.5)

        


        self.selection_method = options.get('selection_method', None)
        
        #elitsm
        self.elitism = options.get('elitism', True)
        self.num_parents = options.get('num_parents', 2)
        
        
        #mutation wrapper
        self.mutation_wrapper_method = options.get('mutation_wrapper_method', None)
        #crossover wrapper
        self.crossover_wrapper_method = options.get('crossover_wrapper_method', None)
        
        
        
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
                crossover_probability=self.crossover_probability,
                elitism=self.elitism,
                num_parents=self.num_parents,
                mutation_wrapper_method=self.mutation_wrapper_method,
                crossover_wrapper_method=self.crossover_wrapper_method)

        self.generation = 0
        self.population_stats = []
        self.current_stats = None

    
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
        """
        Store an individual in the storage backend.
        """
        if self.storage:    
            self.storage.write_individual(hash, self.generation, individual )

        
    def evaluate_population(self, **options):
        """
        Evaluate current population, the following operations are performed:    
        
        * run fitness_evaluator (compute score on each individual)
        * calculate statistics
        * scale population individuals (compute scaled_score on each individual)
        """
        self.population.fit_individuals(self.fitness_evaluator, self.cache, eval_callback=self.store_individual)
        stats = self.stat_population(**options)
        self.population.scale_individuals(stats)
        
        
    def stat_population(self, **options):
        """
        Compute statistics for current population: min max and average scores, idle cycles.
        If a storage is set, stats are written to storage backend.
        After computation, stats are stored in population_stats property, that contains stats
        for all generations. 
        the current_generation property is set to stats.
        
        """
        scores = [individual.score for individual in self.population.individuals]
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)
        
        if self.optimization_mode == 'max':
            top_key = 'max_score'
        else:
            top_key = 'min_score'

        stats = { 'avg_score' : avg_score, 'min_score' : min_score, 'max_score' : max_score,
            'generation' : self.generation }
        
                
        self.population_stats.append(stats)
        self.current_stats = stats
        
        
        if self.generation == 0:
            stats['idle_cycles'] = 0
        else:
            if self.population_stats[self.generation][top_key] == self.population_stats[self.generation-1][top_key]:
                stats['idle_cycles'] = self.population_stats[self.generation-1]['idle_cycles'] +  1
            else:
                stats['idle_cycles'] = 0

        if options.get('debug', None):
            print stats

        if self.storage:
            self.storage.write_population_stats(self.generation, stats)
            
        return stats
        

    def best_individual(self):
        return self.population.best_individual()
        
        
    def evolve_population(self, **options):
        new_population = self.population.evolve(**options)
        self.population = new_population
        self.generation = new_population.generation_number
         
    
    def evolve(self, **options):
        if not self.termination_criteria:
            raise TypeError("You Must set one or more termination criteria")
        
        self.initialize()
        self.evaluate_population(**options)
        
        while 1:
            if self.should_terminate():
                break
            self.evolve_population(global_stats=self.population_stats, last_stats=self.current_stats, ga_engine=self)
            self.evaluate_population(**options)            
                     
        return self.best_individual()
            
    