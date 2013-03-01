"""
Implements a collection of gene classes

Genes support the following python operators:
    - + - calculates the phenotype resulting from the
      combination of a pair of genes

These genes work via classical Mendelian genetics
"""

import sys
from random import randrange, random, uniform, choice,seed
from math import sqrt


class BaseGene(object):
    """
    Base class from which all the gene classes are derived.

    You cannot use this class directly, because there are
    some methods that must be overridden.    
    """
     
    def __init__(self, value=None, **options):
    
        # if value is not provided, it will be
        # randomly generated
        if value == None:
            value = self.random_value()   
        self.value = value    
        self.options=options
    
    def copy(self):
        """
        returns clone of this gene
        """
        return self.__class__(self.value, **self.options)
    
    def __add__(self, other):
        """
        Combines two genes in a gene pair, to produce an effect
        This is used to determine the gene's phenotype
        Must be overridden
        """
        raise NotImplementedError("Method __add__ must be overridden")
        
    def __eq__(self, other):
        return self.value == other.value
    
    def mutate(self):
        """
        Perform a mutation on the gene        
        You MUST override this in subclasses
        """
        raise NotImplementedError("method 'mutate' not implemented")
    
    def random_value(self):
        """
        Generates a plausible random value
        for this gene.        
        Must be overridden
        """
        raise NotImplementedError("Method 'random_value' not implemented")
              
    def get_hash(self):
        return "%s_%s" % (self.__class__.__name__ , str(self.value))
    

    

class FloatGene(BaseGene):
    """
    A gene whose value is a floating point number

    Class variables to override:

        - min_value - default -1.0 - minimum possible value
          for this gene. Mutation will never allow the gene's
          value to be less than this

        - max_value - default 1.0 - maximum possible value
          for this gene. Mutation will never allow the gene's
          value to be greater than this
    """
    
    def __init__(self, value=None, **options):
        
        
        max_value = options.get('max_value', 1.0)
        min_value = options.get('min_value', -1.0)
        mutation_speed = options.get('mutation_speed', 1.0)
        
        if min_value > max_value:
            raise ValueError("Max value should be greater than min value")
        
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.mutation_speed = float(mutation_speed)
        if mutation_speed < 0 or mutation_speed > 1:
            raise ValueError("Mutation speed should be between 0 and 1")
        if value:
            value = float(value)
        super(FloatGene, self).__init__(value=value, **options)
    
    def __add__(self, other):
        """
        Combines two genes in a gene pair, to produce an effect
        returns a new FloatGene, based on a random choice between the two and their mean
    """
        meanValue = (self.value + other.value) / 2
        new_value = choice([meanValue, self.value, other.value])
        return FloatGene(value=new_value, min_value=self.min_value, max_value=self.max_value)     
    
    
    def set_value(self, value):
        # if the gene has wandered outside the alphabet,
        # bring it back in
        if value <= self.min_value:
            self.value = self.min_value
        elif value >= self.max_value:
            value = self.max_value
        else:
            self.value = value
            
    
    def mutate(self):
        """
        Mutate this gene's value by a random amount
        within the range, which is determined by
        multiplying self.mutation_speed by the distance of the
        gene's current value from either endpoint of legal values
        perform mutation IN-PLACE, ie don't return mutated copy
        """
        
        #self.value = self.random_value()
        #return
        
        if random() < 0.5:
            # mutate downwards
            max_abs_mut = (self.value - self.min_value) * self.mutation_speed
            value = self.value - uniform(0, max_abs_mut)
        else:
            max_abs_mut =  (self.max_value - self.value) * self.mutation_speed
            value = self.value + uniform(0, max_abs_mut)
            
        self.set_value(value)
    
    def random_value(self):
        """
        Generates a plausible random value
        for this gene.
        """
        return uniform(self.min_value, self.max_value)    


class IntGene(BaseGene):
    """
    Implements a gene whose values are ints,
    constrained within the min_value,max_value range
    """

    def __init__(self, value=None, **options):
        
        min_value = options.get('min_value', -sys.maxint)
        max_value = options.get('max_value', sys.maxint)
        mutation_range = options.get('mutation_range', None)
        
        
        if min_value > max_value:
            raise ValueError("Max value should be greater than min value")
            
        self.min_value = min_value
        self.max_value = max_value
        if not mutation_range:
            mutation_range = (self.max_value-self.min_value) / 2
            mutation_range=min(mutation_range,1)
        self.mutation_range = mutation_range

        super(IntGene, self).__init__(value=value, **options) 
                            


    def set_value(self, value):
        # if the gene has wandered outside the alphabet,
        # bring it back in
        if value < self.min_value:
            value = value + self.min_value
            self.value = self.min_value
        elif value > self.max_value:
            self.value = self.max_value
        else:
            self.value = value
        
    def mutate(self):
        """
        perform mutation IN-PLACE, ie don't return mutated copy
        """
        
        mut_amt = randrange(1, self.mutation_range+1)
        if random() < 0.5:
            mut_amt = -mut_amt
        value = self.value + mut_amt    
        self.set_value(value)
        
        
        
    def random_value(self):
        """
        return a legal random value for this gene
        which is in the range [self.min_value, self.max_value]
        """
        return randrange(self.min_value, self.max_value+1)
    

    def __add__(self, other):
        """
        produces the phenotype resulting from combining
        this gene with another gene in the pair
        returns a new IntGene, based on a random choice between the two and their mean
        """
        mean_value = int((self.value + other.value) / 2)
        new_value = choice([self.value, mean_value, other.value])
        return IntGene(value=new_value, min_value=self.min_value, max_value=self.max_value,
                    mutation_range = self.mutation_range)


class DiscreteGene(BaseGene):
    """
    Gene type with a fixed set of possible values, typically
    strings
    
    Mutation behaviour is that the gene's value may
    spontaneously change into one of its alleles
    """
    
    def __init__(self, value=None, **options):
    
        alleles=options.get('alleles', [])
        
        self.alleles = alleles
        if value is not None and value not in alleles:
            raise ValueError("Provided value must be in alleles")
        super(DiscreteGene, self).__init__(value=value, **options)
    
    def mutate(self):
        """
        Change the gene's value into any of the possible alleles,
        subject to mutation probability 'self.mutProb'
    
        perform mutation IN-PLACE, ie don't return mutated copy
        """
        self.value = self.random_value()
    
    def random_value(self):
        """
        returns a random allele
        """
        return choice(self.alleles)
    
    def __add__(self, other):
        """
        was: determines the phenotype, subject to dominance properties
        is: random choice
        """
        #new code
        new_value=choice([self.value, other.value])
        return DiscreteGene(value=new_value, alleles=self.alleles)

    
class BitGene(BaseGene):
    """
    Implements a single-bit gene
    """
    
    def __init__(self, value=None):
        super(BitGene, self).__init__(value=value)
    
    def __add__(self, other):
        """
        Produces the 'phenotype' as xor of gene pair values
        """
        value = choice([self.value, other.value])
        return BitGene(value=value)
        
    def mutate(self):
        """
        mutates this gene, toggling the bit
        probabilistically
        perform mutation IN-PLACE, ie don't return mutated copy
        """
        self.value ^= 1
    
    def random_value(self):
        """
        Returns a legal random (boolean) value
        """
        if random() < 0.5:
            return 1
        else:
            return 0
    


class AndBitGene(BitGene):
    """
    Implements a single-bit gene, whose
    phenotype is the AND of each gene in the pair
    """
    def __add__(self, other):
        """
        Produces the 'phenotype' as xor of gene pair values
        """
        return BitGene(self.value and other.value)
    

class OrBitGene(BitGene):
    """
    Implements a single-bit gene, whose
    phenotype is the OR of each gene in the pair
    """
    def __add__(self, other):
        """
        Produces the 'phenotype' as xor of gene pair values
        """
        return BitGene(self.value or other.value)
    


class XorBitGene(BitGene):
    """
    Implements a single-bit gene, whose
    phenotype is the exclusive-or of each gene in the pair
    """
    def __add__(self, other):
        """
        Produces the 'phenotype' as xor of gene pair values
        """
        return BitGene(self.value ^ other.value)
    
