class BaseStorage(object):
    def initialize(self):
        raise NotImplementedError()
    
    def write_individual(hash, generation, individual):
        raise NotImplementedError()
        
    def write_population_stats(generation, stats):
        raise NotImplementedError()