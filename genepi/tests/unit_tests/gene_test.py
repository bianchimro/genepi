import unittest
from nose.tools import assert_raises, raises
from genepi.core.gene import BaseGene
from genepi.core.gene import IntGene
from genepi.core.gene import FloatGene
from genepi.core.gene import DiscreteGene
from genepi.core.gene import BitGene, AndBitGene, OrBitGene, XorBitGene

class BaseGeneTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_init(self):
        gene = BaseGene(value=1)
        assert gene.value == 1

    @raises(NotImplementedError)
    def test_init_raises(self):
        gene = BaseGene()

    @raises(NotImplementedError)        
    def test_random_value(self):
        gene = BaseGene(value=1)
        val = gene.random_value()

    @raises(NotImplementedError)         
    def test_mutate(self):
        gene = BaseGene(value=1)
        gene.mutate()

    @raises(NotImplementedError)                 
    def test_add(self):
        gene_a = BaseGene(value=1)
        gene_b = BaseGene(value=10)
        gene_c = gene_a + gene_b
        
    def test_eq(self):
        gene_a = BaseGene(value=1)
        gene_b = BaseGene(value=1)
        assert gene_a == gene_b
                
    def test_get_hash(self):
        gene_a =BaseGene(value=1)
        hash_a = gene_a.get_hash()
        assert hash_a == 'BaseGene_1'
    
    def test_copy(self):
        gene_a =BaseGene(value=1)
        gene_b = gene_a.copy()
        assert gene_a.value == gene_b.value
        assert gene_a is not gene_b


class IntGeneTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_init(self):
        gene = IntGene(value=1, min_value=0, max_value=100, mutation_range=10)
        assert gene.value == 1
        
    @raises(ValueError)
    def test_init_raises(self):
        gene = IntGene(min_value=220, max_value=100)

    def test_random_value(self):
        gene = IntGene(value=1, min_value=0, max_value=100)
        val = gene.random_value()
        assert val >= gene.min_value and val <= gene.max_value
        
    def test_mutate(self):
        gene = IntGene(value=1, min_value=0, max_value=100)
        gene.mutate()
        gene_b = IntGene(value=1, min_value=0, max_value=0, mutation_range=10000000)
        gene_b.mutate()
        
    def test_add(self):
        gene_a = IntGene(value=1, min_value=0, max_value=100)
        gene_b = IntGene(value=1, min_value=0, max_value=200)
        gene_c = gene_a + gene_b
        assert gene_c.value >= gene_a.min_value and gene_c.value  <= gene_a.max_value
        assert gene_c.value in [gene_a.value, gene_b.value, (gene_a.value+gene_b.value)/2]    
        
    def test_get_hash(self):
        gene_a = IntGene(value=1, min_value=0, max_value=100)
        hash_a = gene_a.get_hash()
        gene_b = IntGene(value=1, min_value=0, max_value=100)
        hash_b = gene_b.get_hash()
        assert hash_a == hash_b




class DiscreteGeneTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_init(self):
        gene = DiscreteGene(alleles=[1,2], value=1)
        assert gene.value == 1

    @raises(ValueError)
    def test_init_valuerror(self):
        gene = DiscreteGene(alleles=[1,2], value=10)
        
    def test_random_value(self):
        alleles=[1,2,4,10]
        gene = DiscreteGene(alleles=alleles, value=1)
        val = gene.random_value()
        assert val in alleles
        
    def test_mutate(self):
        alleles_a=[1,2,4,10]
        gene_a = DiscreteGene(alleles=alleles_a, value=1)
        gene_a.mutate()
        assert gene_a.value in alleles_a
        
    def test_add(self):
        alleles_a = [1,2,4,10]
        gene_a = DiscreteGene(alleles=alleles_a, value=1)
        gene_b = DiscreteGene(alleles=alleles_a, value=2)
        gene_c = gene_a + gene_b
        assert gene_c.value in [gene_a.value, gene_b.value]


class FloatGeneTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_init(self):
        gene = FloatGene(min_value=0.0, max_value=100, mutation_speed=1.0)
        gene_b = FloatGene(value = 10 ,min_value=0.0, max_value=100, mutation_speed=1.0)
        assert gene_b.value == 10
        
    @raises(ValueError)
    def test_init_raises(self):
        gene = FloatGene(min_value=220.0, max_value=100)
        
    @raises(ValueError)
    def test_init_raises_mut(self):
        gene = FloatGene(min_value=10.0, max_value=100, mutation_speed=10)
        
    def test_random_value(self):
        gene = FloatGene(value=1, min_value=0, max_value=100)
        val = gene.random_value()
        assert val >= gene.min_value and val <= gene.max_value
        
    def test_mutate(self):
        gene = FloatGene(value=10.3, min_value=0, max_value=100)
        gene.mutate()
        
    def test_add(self):
        gene_a = FloatGene(value=11, min_value=0, max_value=100)
        gene_b = FloatGene(value=17, min_value=0, max_value=100)
        gene_c = gene_a + gene_b
        assert gene_c.value >= gene_a.min_value and gene_c.value  <= gene_a.max_value
        assert gene_c.value in [gene_a.value, gene_b.value, (gene_a.value+gene_b.value)/2]
    
    def test_get_hash(self):
        gene_a = IntGene(value=1, min_value=0, max_value=100)
        hash_a = gene_a.get_hash()
        gene_b = IntGene(value=1, min_value=0, max_value=200)
        hash_b = gene_b.get_hash()
        assert hash_a == hash_b


class BitGeneTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_init(self):
        gene = BitGene()
        
    def test_mutate(self):
        gene = BitGene()
        gene.mutate()
        assert gene.value in [0,1]

    def test_add(self):
        gene_a = BitGene()
        gene_b = BitGene()
        gene_c = gene_a + gene_b
        assert gene_c.value in [0,1]
        
    def test_add_and(self):
        gene_a = AndBitGene()
        gene_b = AndBitGene()
        gene_c = gene_a + gene_b
        assert gene_c.value == (gene_a.value and gene_b.value)
        
    def test_add_or(self):
        gene_a = OrBitGene()
        gene_b = OrBitGene()
        gene_c = gene_a + gene_b
        assert gene_c.value == gene_a.value or gene_b.value
        
    def test_add_xor(self):
        gene_a = XorBitGene()
        gene_b = XorBitGene()
        gene_c = gene_a + gene_b
        assert gene_c.value == gene_a.value ^ gene_b.value
        
        