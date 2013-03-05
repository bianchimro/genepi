class ProtoGene(object):
    """
    Protogene class. Acts as a wrapper for various gene classes.    
    """    
    def __init__(self, gene_class, name=None, **kwargs):
        """
        
        :param gene_class: gene class to be instatiated (subclass of :class:`genepi.core.gene.BaseGene`
        :param name: the name of the protogene. Will be referenced in protogenome
        :param **kwargs: arguments to be passed to the gene class
        
        """
        self.gene_class=gene_class
        self.kwargs = kwargs
        self.name = name
        
    def get_gene(self):
        """
        Creates and returns a gene based on this protogene.
        """
        out =  self.gene_class(**self.kwargs)
        return out