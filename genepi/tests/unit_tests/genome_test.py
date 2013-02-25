import unittest
from genepi.core.genome import Genome
from genepi.core.gene import IntGene
try:
    from collections import OrderedDict
except:
    from genepi.utils.ordereddict import OrderedDict


class GenomeTest(unittest.TestCase):

    def setUp(self):
        self.genes_dict = OrderedDict()
        self.genes_dict['a'] = IntGene(value=1)
        self.genes_dict['b'] = IntGene(value=2)

    def tearDown(self):
        pass
        
    def test_init(self):
        genome = Genome(self.genes_dict)
        
        
    def test_dict_value(self):
        genome = Genome(self.genes_dict)
        dict_value = genome.dict_value()
        
    def test_list_value(self):
        genome = Genome(self.genes_dict)
        list_value = genome.list_value()
    
    def test_get_hash(self):
        genome = Genome(self.genes_dict)
        genome.get_hash()
        
    def test_mutate(self):
        genome = Genome(self.genes_dict, mutation_probability=1)
        has_mutated = genome.mutate()
        assert has_mutated == True
        genome_b = Genome(self.genes_dict, mutation_probability=0)
        has_mutated = genome_b.mutate()
        assert has_mutated == False
        
    def test_add(self):
        genome_a = Genome(self.genes_dict)
        genome_a.score = 1
        genome_b = Genome(self.genes_dict)
        genome_b.score = 2
        genome_c = genome_a + genome_b
        assert genome_c.score is None

        
        
    def test_to_json(self):
        genome = Genome(self.genes_dict)
        genome.to_json()