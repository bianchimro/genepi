import hashlib
from collections import OrderedDict

class Genome(object):
    """Genome is a collection of genes"""
    
    genes_dict = OrderedDict()
    score = None
    value = None
    
    def __init__(self, genes_dict):
        self.genes_dict = genes_dict
        
    def dict_value(self):
        out = {}
        for name in self.genes_dict:
            out[name] = self.genes_dict[name].value
        return out
        
    def list_value(self):
        out = []
        for name in self.genes_dict:
            out.append(self.genes_dict[name].value)
        return out        
        
    def get_hash(self):
        h = hashlib.md5()
        for name in self.genes_dict:
            gene = self.genes_dict[name]
            h.update(gene.get_hash())
            
        return h.hexdigest()
            
        
    