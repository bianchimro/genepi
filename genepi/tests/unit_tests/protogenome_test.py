import unittest
from genepi.core.protogenome import ProtoGenome
from genepi.core.protogene import ProtoGene
from genepi.core.gene import IntGene

class ProtoGenomeTest(unittest.TestCase):

    def setUp(self):
        self.protogene_a = ProtoGene(IntGene, 'a')
        self.protogene_b = ProtoGene(IntGene)

    def tearDown(self):
        pass
        
    def test_init(self):
        algo = ProtoGenome([self.protogene_a, self.protogene_b])
        
    def test_add_protogene(self):
        pg = ProtoGenome([self.protogene_a])
        pg.add_protogene(self.protogene_b)
        protogene_c = ProtoGene(IntGene, 'c')
        pg.add_protogene(protogene_c)