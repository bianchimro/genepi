class BaseStorage(object):
    def initialize(self):
        raise NotImplementedError()
    
    def write_individual(self, hash, generation, individual):
        raise NotImplementedError()
        
    def write_population_stats(self, generation, stats):
        raise NotImplementedError()