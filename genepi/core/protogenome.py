from genome import Genome
try:
    from collections import OrderedDict
except:
    from genepi.utils.ordereddict import OrderedDict


class ProtoGenome(object):
    """
    ProtoGenome class. 
    It is the "model" of a Genome, in the same way as ProtoGene is a model of Gene.
    Basically a collection of protogenes.
    """
    
    def __init__(self, protogenes=[], **options):
        """
        :param protogenes: a list of :class:`genepi.core.protogene.Protogene` instances,
        to be used as protogenomes
        :param  **options: options to be bassed to the Genome constructor
        """
        self.protogenes = OrderedDict()
        self.options = options
        
        for i, protogene in enumerate(protogenes):
            if protogene.name:
                name = protogene.name
            else:
                name = str(i)
            self.protogenes[name] = protogene
    
    def num_protogenes(self):
        """
        Returns the number of protogenes.
        """
        return len(self.protogenes.keys())
        
    def add_protogene(self, protogene):
        """
        Add a new protogene
        """
        if protogene.name:
            name = protogene.name
        else:
            name = str(self.num_protogenes())
        self.protogenes[name] = protogene
    
    def get_genome(self):
        """
        Creates and returns an instance of genome, composed by genes corresponding to protogenes
        """
        genes_dict = OrderedDict()
        for name in self.protogenes:
            gene = self.protogenes[name].get_gene()
            genes_dict[name] = gene
        return Genome(genes_dict, **self.options)
        