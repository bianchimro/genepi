class ProtoGene(object):
    """
    Protogene class. Acts as a wrapper for various gene classes.    
    """    
    def __init__(self, gene_class, name=None, **kwargs):
        self.gene_class=gene_class
        self.kwargs = kwargs
        self.name = name
        
    def get_gene(self):
        out =  self.gene_class(value=None, **self.kwargs)
        return out