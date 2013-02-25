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
        assert len(pop.individuals) == pop.size
        