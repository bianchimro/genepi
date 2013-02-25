        return IntGene(value=new_value, min_value=self.min_value, mutation_range=self.mutation_range)
    

#TODO: refactor as needed
class CharGene(BaseGene):
    """
    Gene that holds a single ASCII character,
    as a 1-byte string
    """
    # minimum possible value for gene
    # override in subclasses as needed
    min_value = chr(0)
    
    # maximum possible value for gene
    # override in subclasses as needed
    max_value = chr(255)
    
    def __repr__(self):
        """
        Returns safely printable value
        """
        return str(self.value)
    
    def mutate(self):
        """
        perform gene mutation
    
        perform mutation IN-PLACE, ie don't return mutated copy
        """
        self.value = chr(ord(self.value) + randrange(-self.mutAmt, self.mutAmt + 1))
    
        # if the gene has wandered outside the alphabet,
        # rein it back in
        if self.value < self.min_value:
            self.value = self.min_value
        elif self.value > self.max_value:
            self.value = self.max_value
    
    def random_value(self):
        """
        return a legal random value for this gene
        which is in the range [self.min_value, self.max_value]
        """
        return chr(randrange(ord(self.min_value), ord(self.max_value)+1))
    
    def __add__(self, other):
        """
        produces the phenotype resulting from combining
        this gene with another gene in the pair
        
        returns an int value, based on a formula of higher
        numbers dominating
        """
        return max(self.value, other.value)
    
#TODO: refactor as needed
class AsciiCharGene(CharGene):
    """
    Specialisation of CharGene that can only
    hold chars in the legal ASCII range
    """
    # minimum possible value for gene
    # override in subclasses as needed
    min_value = chr(0)

    # maximum possible value for gene
    # override in subclasses as needed
    max_value = chr(255)

    def __repr__(self):
        """
        still need to str() the value, since the range
        includes control chars
        """
        return self.value

class PrintableCharGene(AsciiCharGene):
    """
    Specialisation of AsciiCharGene that can only
    hold printable chars
    """
    # minimum possible value for gene
    # override in subclasses as needed
    min_value = ' '

    # maximum possible value for gene
    # override in subclasses as needed
    max_value = chr(127)

    def __repr__(self):
        """
        don't need to str() the char, since
        it's already printable
        """
        return self.value