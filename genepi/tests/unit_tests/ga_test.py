import unittest
from genepi.core.ga import GeneticAlgorithm

class GeneticAlgorithmTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_init(self):
        algo = GeneticAlgorithm(1,2)
        