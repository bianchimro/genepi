from collections import OrderedDict
from genome import Genome

class ProtoGenome(object):
    """
    ProtoGenome class. Basically a collection of protogenes.
    """
    
    def __init__(self, protogenes=[]):
        self.protogenes = OrderedDict()
        for i, protogene in enumerate(protogenes):
            if protogene.name:
                name = protogene.name
            else:
                name = str(i)
            self.protogenes[name] = protogene
    
    def num_protogenes(self):
        return len(self.protogenes.keys())
        
    def add_protogene(self, protogene):
        if protogene.name:
            name = protogene.name
        else:
            name = str(self.num_protogenes())
        self.protogenes[name] = protogene
    
    def get_genome(self):
        genes_dict = OrderedDict()
        for name in self.protogenes:
            gene = self.protogenes[name].get_gene()
            genes_dict[name] = gene
        return Genome(genes_dict)
        