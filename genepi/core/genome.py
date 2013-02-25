import hashlib
import json
import random
try:
    from collections import OrderedDict
except:
    from genepi.utils.ordereddict import OrderedDict

class Genome(object):
    """Genome is a collection of genes"""
    
    genes_dict = OrderedDict()
    score = None
    
    def __init__(self, genes_dict, mutation_probability=0.1):
        self.genes_dict = genes_dict
        self.mutation_probability = mutation_probability
        
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
        

    def get_value(self, key):
        return self.genes_dict[key].value
    
    def set_value(self, key, value):
        self.genes_dict[key].value = value
        
    def get_hash(self):
        h = hashlib.md5()
        for name in self.genes_dict:
            gene = self.genes_dict[name]
            h.update(gene.get_hash())
            
        return h.hexdigest()
    
    def copy(self, genes_dict=None):
        if genes_dict is None:
            genes_dict = OrderedDict()
            for x in self.genes_dict:
                genes_dict[x] = self.genes_dict[x].copy()
        new_genome = Genome(genes_dict)
        new_genome.score = self.score
        new_genome.mutation_probability = self.mutation_probability
        return new_genome
        
        
    def to_json(self):
        dict_value = self.dict_value()
        return json.dumps(dict_value)
        
    
    def should_mutate_uniform_probability(self):
        random.seed()
        coin = random.random()
        if coin <= self.mutation_probability:
            return True
        return False
    
    
    def should_mutate(self, gene):
        return self.should_mutate_uniform_probability()
    
    def __add__(self, other):
        genes_dict = OrderedDict()
        for name in self.genes_dict:
            gene = self.genes_dict[name]
            other_gene = other.genes_dict[name]
            genes_dict[name] = gene + other_gene

        new_genome = self.copy(genes_dict=genes_dict)
        new_genome.score = None
        return new_genome
    
    def __eq__(self, other):
        out = True
        for name in self.genes_dict:
            gene = self.genes_dict[name]
            other_gene = other.genes_dict[name]
            out = out and (gene==other_gene)
        return out

        
        
    def mutate(self):
        """In place mutation"""
        has_mutated = False
        for name in self.genes_dict:
            gene = self.genes_dict[name]
            if self.should_mutate(gene):
                gene.mutate()
                has_mutated = True
            #reset score in case of mutation
            if has_mutated:
                self.score = None
        return has_mutated
            
        
    