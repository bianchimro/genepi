
class Population(object):
    """A population is a collection of individuals"""

    individuals = []
    size = 100

    def __init__(self, protogenome, size=100, optimization_mode='min', **kwargs):
        
        self.protogenome = protogenome
        self.size = size
        self.optimization_mode=optimization_mode
        
        self.generation_number = 0
        self.sorted = False
    
    
    def initialize(self):
        for x in range(self.size):
            individual = self.protogenome.get_genome()
            self.individuals.append(individual)
            
    
    def evolve(self):
        pass
        
        
    def cmp_individual(self, a, b):
        #TODO: document, this is a bit tricky
        if self.optimization_mode == 'max':
            return cmp(a.score, b.score)
        else:
            return cmp(b.score, a.score)
        
    def sort(self):
        self.individuals.sort(self.cmp_individual)
        self.sorted = True
    
    
    def best_individual(self):
        if not self.sorted:
            self.sort()
        return self.individuals[0]
        
        
    