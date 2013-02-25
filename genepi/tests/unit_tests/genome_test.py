import unittest
from collections import OrderedDict
from genepi.core.genome import Genome
from genepi.core.gene import IntGene

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
        
    def test_to_json(self):
        genome = Genome(self.genes_dict)
        genome.to_json()