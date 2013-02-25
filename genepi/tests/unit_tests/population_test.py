import unittest
from genepi.core.population import Population
from genepi.core.genome import Genome
from genepi.core.gene import IntGene
from genepi.core.protogene import ProtoGene
from genepi.core.protogenome import ProtoGenome

class PopulationTest(unittest.TestCase):

    def setUp(self):
        protogene_a = ProtoGene(IntGene, 'a')
        self.protogenome = ProtoGenome([protogene_a])
        

    def tearDown(self):
        pass
        
    
    def test_init(self):
        pop = Population(self.protogenome)
        
    
    def test_initialize(self):
        pop = Population(self.protogenome)
        pop.initialize()    
        print len(pop.individuals), pop.size
        assert len(pop.individuals) == pop.size
    
    
    def test_copy(self):
        pop = Population(self.protogenome)
        pop.initialize() 
        pop2 = pop.copy()   
    
        
    def test_sort(self):
        protogene_a = ProtoGene(IntGene, 'a')
        protogenome = ProtoGenome([protogene_a])
        pop = Population(protogenome, optimization_mode='min')
        pop.initialize()    
        for i in range(pop.size):
            pop.individuals[i].score = i
        pop.sort()
        assert pop.individuals[0].score == 0
        
        pop_2 = Population(protogenome, optimization_mode='max')
        pop_2.initialize(individuals=pop.individuals)
        pop_2.sort()
        assert pop_2.individuals[-1].score == 0
        assert pop_2.individuals[-1].score == pop.individuals[0].score
        
    
    def test_best_indivividual(self):
        protogene_a = ProtoGene(IntGene, 'a')
        protogenome = ProtoGenome([protogene_a])
        pop = Population(protogenome, optimization_mode='min')
        pop.initialize()    
        for i in range(pop.size):
            pop.individuals[i].score = i
        
        best_ind = pop.best_individual()
        assert pop.individuals[0].score == best_ind.score == 0
        assert pop.individuals[0].get_hash() == best_ind.get_hash()
        