"""
This module contains Population class and some defaults
"""

from copy import copy, deepcopy
import random
from genepi.core.crossover import single_point_crossover
from genepi.core.selectors import select_from_top, roulette_select

#TODO: move to SELECTORS module


    
POPULATION_DEFAULT_SIZE = 100

class Population(object):
    """
    A population is a collection of individuals.
    Normally, this class should be instantiated by a :class:`genepi.core.ga.GeneticAlgorithm` object.
    
    :param protogenome: instance of :class:`genepi.core.protogenome.Protogenome`
    :param size: integer indicating the size (number of individuals) of the population.\
    (defaults to :data:`genepi.core.population.POPULATION_DEFAULT_SIZE`)
    
    The following other parameters can be passed as **options:
    
    :param optimization_mode: 'min' or 'max', defaults to 'min'
    :param selection_method: the selection method to be used, defaults to :function: `genepi.core.selectors.select_from_top`
    :param num_parents: number of parents chosen by the selection method
    :param elitism: whether use or not elitism, defaults to True
    
    
    
    
    """

    individuals = []
    size = 100

    def __init__(self, protogenome, size=POPULATION_DEFAULT_SIZE, **options):

        
        self.protogenome = protogenome
        self.size = size
        
        self.options = options
        
        #optimization mode - 'min' or 'max'
        self.optimization_mode=options.get('optimization_mode', 'min')
        
        #number of selected parents
        self.num_parents = options.get('num_parents', 2)
        #elitism
        self.elitism = options.get('elitism', True)
        
        #selection method
        self.selection_method = options.get('selection_method', None)
        if self.selection_method is None:
            self.selection_method = select_from_top
        
        #crossover method
        self.crossover_method = options.get('crossover_method', None)
        if self.crossover_method is None:
            self.crossover_method = single_point_crossover
        self.crossover_probability = options.get('crossover_probability', 0.5)
        
        #crossover wrapper
        self.crossover_wrapper_method = options.get('crossover_wrapper_method', None)
        
        #mutation wrapper
        self.mutation_wrapper_method = options.get('mutation_wrapper_method', None)
        

        #internal state
        self.generation_number = 0
        self.sorted = False
        
    
    def initialize(self, individuals=[]):
        """
        Initialize the population with individuals, represented by 
        :class:`genepi.core.genome.Genome` instances. 
        
        :param individuals: an optional list of genome instance to be used to initialize the population.
        """
        new_individuals = []
        for individual in individuals:
            new_individual = individual.copy()
            new_individuals.append(new_individual)

        self.individuals = new_individuals
        start_index = len(self.individuals)
        
        for x in range(start_index, self.size):
            individual = self.protogenome.get_genome()
            self.individuals.append(individual)
    
    
    def mutate(self):
        """In place mutation for the population"""
        for individual in self.individuals:
            individual.mutate()
            
            
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
        
    def scale_individuals(self, stats):

        if self.optimization_mode == 'max':
            ref = (stats['max_score']) + 1
        else:
            ref = (stats['max_score'] - stats['min_score']) + 1
        
        for individual in self.individuals:
            if self.optimization_mode == 'max':
                score = (individual.score)
            else:
                score = (stats['max_score'] - individual.score) + 1
           
            individual.scaled_score = float(score) / ref
        #todo: kinda cache ...
        self.current_scaled_scores = [x.scaled_score for x in self.individuals]
    
    
    def should_crossover(self, **options):
        probability = options.get('crossover_probability', None)
        probability = probability or self.crossover_probability
        coin = random.random()
        if coin <= probability:
            return True
        return False
        
        
    def crossover_wrapper(self, parents, **options):
        if self.crossover_wrapper_method:
            return self.crossover_wrapper_method(parents[0], parents[1], **options)
        return self.crossover(parents[0], parents[1])
        
    def crossover(self, genome_a, genome_b):
        if type(self.crossover_method) == type(list()):
            meth = random.choice(self.crossover_method)
        else:
            meth = self.crossover_method
        return meth(genome_a, genome_b)
        
        
    def apply_crossover(self, parents, **options):
        if self.should_crossover(**options):
            return self.crossover(parents[0], parents[1])
            #new_individual = method(parents[0], parents[1])
        else:
            new_individual = random.choice(parents).copy()
        return new_individual
    
    
    def mutation_wrapper(self, genome, **options):
        if self.mutation_wrapper_method:
            return self.mutation_wrapper_method(self, genome, **options)
        return genome.mutate()
        
            
    def evolve(self, **options):
        new_individuals = []
        num_individuals = 0
        
        if self.elitism:
            parents_candidates = select_from_top(self, self.num_parents)
            for individual in parents_candidates:
                new_individual = individual.copy()
                new_individuals.append(new_individual)
                num_individuals += 1

        parents_candidates = self.select_individuals()            
        while num_individuals < self.size:
            #breeding and crossover
            
            parents = random.sample(parents_candidates, 2)
            new_individual = self.crossover_wrapper(parents, **options)
            #mutate
            self.mutation_wrapper(new_individual, **options)
            new_individuals.append(new_individual)
            num_individuals += 1
    
        new_population = self.copy(individuals=new_individuals)
        
        new_population.generation_number = self.generation_number + 1
        return new_population
        
        
    def cmp_individual(self, a, b):
        """
        Compares individuals, according to their score. Comparing takes in account the population\
        optimization_mode.
        """
        #TODO: document, this is a bit tricky
        if self.optimization_mode == 'min':
            return cmp(a.score, b.score)
        else:
            return cmp(b.score, a.score)
        
        
    def sort(self):
        """
        sorts individual using internal cmp_individual method and sets sorted flag to True
        """
        self.individuals.sort(self.cmp_individual)
        self.sorted = True
    
    
    def best_individual(self):
        """
        Returns best individual. Individual are sorted if sorted flag is false.
        """
        if not self.sorted:
            self.sort()
        return self.individuals[0]
        
        
    def copy(self, individuals=[]):
        """
        Returns a new instance of :class:`genepi.core.population.Population` with the same
        options and individuals of this one. Individuals are copied.
        
        :param individuals: an optional list of individuals (:class:`genepi.core.genome.Genome` instances.)\
        to initialize the population
        """
        if not individuals:
            for individual in self.individuals:
                new_individual = individual.copy()
                individuals.append(new_individual)
        
        pop = Population(self.protogenome, self.size, **self.options)
        pop.initialize(individuals=individuals) 
        return pop
        
        
        
    