import os
import unittest
from genepi.core.ga import GeneticAlgorithm
from genepi.core.gene import IntGene
from genepi.core.protogene import ProtoGene
from genepi.core.protogenome import ProtoGenome
from genepi.core.population import POPULATION_DEFAULT_SIZE
from genepi.core.stopcriteria import convergence_stop, raw_score_stop
from genepi.cache.base import NoCache
from genepi.storage.sqlite import SqliteStorage

def fitness_evaluator(genome):
     v = genome.get_value('a')
     return v


class GeneticAlgorithmTest(unittest.TestCase):

    def setUp(self):
        self.protogene_a = ProtoGene(IntGene, 'a', min_value=0, max_value=100)
        self.protogenome = ProtoGenome([self.protogene_a])

    def tearDown(self):
        pass
        
    def test_init(self):
        algo = GeneticAlgorithm(self.protogenome, fitness_evaluator, cache_instance=NoCache())
        assert algo.population.size == POPULATION_DEFAULT_SIZE
        
    def test_initialize(self):
        algo = GeneticAlgorithm(self.protogenome, fitness_evaluator)
        algo.initialize()
        
        
    def test_should_terminate(self):
        protogene = ProtoGene(IntGene, 'a', min_value=0, max_value=100, value=1)
        protogenome = ProtoGenome([protogene], mutation_probability=1)
        algo = GeneticAlgorithm(protogenome, fitness_evaluator, termination_criteria=convergence_stop)
        algo.initialize()
        
        for individual in algo.population.individuals:
            individual.score = 1
        
        for x in range(11):
            stats = {'min_score' : 0}
            algo.population_stats.append(stats)
        algo.generation = 10
        st = algo.should_terminate()
        assert st == True
        
        algo.generation = 1
        st = algo.should_terminate()
        assert st == False
        
        
    def test_evaluate_population(self):
        protogene = ProtoGene(IntGene, 'a', min_value=0, max_value=100)
        protogenome = ProtoGenome([protogene])
        algo = GeneticAlgorithm(protogenome, fitness_evaluator, termination_criteria=convergence_stop)
        algo.initialize()
        algo.evaluate_population()
        for individual in algo.population.individuals:
            assert individual.score == fitness_evaluator(individual)


    def test_best_individual(self):
        protogene = ProtoGene(IntGene, 'a', min_value=0, max_value=100)
        protogenome = ProtoGenome([protogene])
        algo = GeneticAlgorithm(protogenome, fitness_evaluator, termination_criteria=convergence_stop)
        algo.initialize()
        for i, individual in enumerate(algo.population.individuals):
            individual.set_value('a', i)
        algo.evaluate_population()

        bi = algo.best_individual()
        assert bi.score == 0
        
    
    def test_evolve_population(self):
        protogene = ProtoGene(IntGene, 'a', min_value=0, max_value=10)
        protogenome = ProtoGenome([protogene])
        algo = GeneticAlgorithm(protogenome, fitness_evaluator, termination_criteria=convergence_stop)
        algo.initialize()
        algo.evaluate_population()
        g1 = algo.generation
        algo.evolve_population()
        g2 = algo.generation
        assert g1 == 0 and g2 == 1
        
   
    def test_evolve(self):
        protogene = ProtoGene(IntGene, 'a', min_value=0, max_value=10)
        protogenome = ProtoGenome([protogene], mutation_probability=0.1)
        algo = GeneticAlgorithm(
            protogenome, 
            fitness_evaluator, 
            termination_criteria=[raw_score_stop,convergence_stop],
            termination_criteria_options = [{'stop_score':0}]    
            )
        algo.evolve()
        
        
    def test_evolve_storage(self):
        storage_instance = SqliteStorage("test.sqlite")
        protogene = ProtoGene(IntGene, 'a', min_value=0, max_value=10)
        protogenome = ProtoGenome([protogene], mutation_probability=0.1)
        algo = GeneticAlgorithm(protogenome, fitness_evaluator, 
            termination_criteria=convergence_stop, storage_instance=storage_instance)
        algo.evolve()

   
    def test_evolve_2(self):
        protogene = ProtoGene(IntGene, 'a', min_value=0, max_value=100)
        protogenome = ProtoGenome([protogene], mutation_probability=0.1)
        algo = GeneticAlgorithm(
            protogenome, 
            fitness_evaluator, 
            termination_criteria=[raw_score_stop,convergence_stop], 
            termination_criteria_options = [{'stop_score':0},{'num_generations':20}]
        )
        algo.evolve()
