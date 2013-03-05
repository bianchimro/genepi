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
    :param fitness_evaluator: the fitness function
    :param termination_criteria: one or more termination criteria for evolution
    :param termination_criteria_options: options for each termination criteria, each option
     set is passed as a dictionary. Options must be passed in the same order as termination 
     criteria

    
    :param population_size: size of the population
    
    
    """
    
    population_size = 100
    selection_method = None
    step_callback = None
    termination_criteria = None
    termination_criteria_options = None
    
    fitness_evaluator = None
    optimization_mode = 'min'
    
    crossover_probability = 0
    
    def __init__(self, 
                    protogenome,
                    fitness_evaluator,
                    optimization_mode='min',
                    termination_criteria=stopcriteria.convergence_stop,
                    termination_criteria_options={},
                    population_size=POPULATION_DEFAULT_SIZE,
                    step_callback=None,        
                    selection_method=None,
                    elitism=True,
                    num_parents=2,
                    crossover_method=None,
                    crossover_probability=0.1,
                    crossover_wrapper_method = None,
                    mutation_wrapper_method=None,
                    storage_instance=None,
                    cache_instance=None,
                    **options):
                 
        """
        """
        
        self.protogenome = protogenome
        self.fitness_evaluator = fitness_evaluator
        self.optimization_mode = optimization_mode
        self.termination_criteria = termination_criteria 
        self.termination_criteria_options = termination_criteria_options 
        self.population_size = population_size
        self.selection_method = selection_method
        self.elitism = elitism
        self.num_parents = num_parents
        self.step_callback = step_callback

        #default crossover and selections are handled by population
        self.crossover_method = crossover_method
        self.crossover_probability = crossover_probability
        
        #mutation wrapper
        self.mutation_wrapper_method = mutation_wrapper_method
        #crossover wrapper
        self.crossover_wrapper_method = crossover_wrapper_method
        
        #cache configuration
        if cache_instance is None:
            self.cache = DictCache()
        else:
            self.cache = cache_instance
        
        #storage configuration
        if storage_instance:
            self.storage = storage_instance
        else:
            self.storage = None
        
        self.options = options
        
        #termination criteria and options check
        if type(self.termination_criteria) == type(list):
            if type(self.termination_criteria_options) != type(list):
                raise ValueError("You must pass options for each termination criteria")
            if len(self.termination_criteria_options) != len(self.termination_criteria):
                raise ValueError("You must pass options for each termination criteria")

        #instantiating population
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
        """
        Initializes population, cache and storage
        """
        self.population.initialize()
        self.cache.initialize()
        if self.storage:
            self.storage.initialize()
        
        
    def should_terminate(self):
        """
        Called after each evolution cycle
        """
        if type(self.termination_criteria) == type(list()):
            for i,criterium in enumerate(self.termination_criteria):
                if criterium(self, **self.termination_criteria_options[i]):
                    return True
        else:
            if self.termination_criteria(self, **self.termination_criteria_options):
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
        
        stats = { 'avg_score' : avg_score, 'min_score' : min_score, 'max_score' : max_score,
            'generation' : self.generation }
        
         
        #setting stats properties       
        self.population_stats.append(stats)
        self.current_stats = stats
        
        #idle cycles calculation: it counts consequent generations without improvements
        if self.optimization_mode == 'max':
            top_key = 'max_score'
        else:
            top_key = 'min_score'

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
        """
        Returns best individual in population (relies on Population method)
        """
        return self.population.best_individual()
        
        
    def evolve_population(self, **options):
        """
        creates a new population with population.evolve, sets the new population as 
        the current and increment generation.
        After this the population in the previous generation is lost
        """
        new_population = self.population.evolve(**options)
        self.population = new_population
        self.generation = new_population.generation_number
         
    
    def evolve(self, **options):
        """
        Performs the evolution cycle.
        This is the main method that should be normally called.
        Evolution goes on until a termination criterium becomes True.
        At the end the best individual is returned.

        """
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
            
    