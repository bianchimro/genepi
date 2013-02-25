#TODO: refactor as needed. Not used now
class ComplexGene(BaseGene):
    """
    A gene whose value is a complex point number
    """
    # amount by which to mutate, will change value
    # by up to +/- this amount
    mutAmtReal = 0.1
    mutAmtImag = 0.1
    
    # used for random gene creation
    # override in subclasses
    randMin = -1.0
    randMax = 1.0
    
    def __add__(self, other):
        """
        Combines two genes in a gene pair, to produce an effect
    
        This is used to determine the gene's phenotype
    
        This class computes the arithmetic mean
        of the two genes' values, so is akin to incomplete
        dominance.
    
        Override if desired
        """
        return (self.value + other.value) / 2
        #return abs(complex(self.value.real, other.value.imag))
    
    
    def mutate(self):
        """
        Mutate this gene's value by a random amount
        within the range +/- self.mutAmt
        perform mutation IN-PLACE, ie don't return mutated copy
        """
        self.value += complex(
            random()*self.mutAmtReal*2 - self.mutAmtReal,
            random()*self.mutAmtImag*2 - self.mutAmtImag
            )
    
        # if the gene has wandered outside the alphabet,
        # rein it back in
        real = self.value.real
        imag = self.value.imag
        
        if real < self.randMin:
            real = self.randMin
        elif real > self.randMax:
            real = self.randMax
    
        if imag < self.randMin:
            imag = self.randMin
        elif imag > self.randMax:
            imag = self.randMax
    
        self.value = complex(real, imag)
    
    def random_value(self):
        """
        Generates a plausible random value
        for this gene.
        
        Override as needed
        """
        min = self.randMin
        range = self.randMax - min
    
        real = random() * range + min
        imag = random() * range + min
    
        return complex(real, imag)

