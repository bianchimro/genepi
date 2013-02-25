ass FloatGeneRandom(FloatGene):
    """
    Variant of FloatGene where mutation always randomises the value
    """
    def mutate(self):
        """
        Randomise the gene
        perform mutation IN-PLACE, ie don't return mutated copy
        """
        self.value = self.random_value()
    

class FloatGeneMax(FloatGene):
    """
    phenotype of this gene is the greater of the values
    in the gene pair
    """
    def __add__(self, other):
        """
        produces phenotype of gene pair, as the greater of this
        and the other gene's values
        """
        new_value = max(self.value, other.value)
        return FloatGene(value=new_value, min_value=self.min_value, max_value=self.max_value)     
    
