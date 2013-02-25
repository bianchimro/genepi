
class Population(object):
    """A population is a collection of individuals"""

    individuals = []
    size = 100

    def __init__(self, protogenome, size=100, **kwargs):
        self.protogenome = protogenome
        self.size = size
        self.generation_number = 0
    
    
    def initialize(self):
        for x in range(self.size):
            individual = self.protogenome.get_genome()
            self.individuals.append(individual)
            
    
    def evolve(self):
        pass