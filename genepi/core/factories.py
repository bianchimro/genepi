"""
Factory methods for creating protogenes
"""

from genepi.core.protogene import ProtoGene

def protogene_factory(gene_class, prefix, number, **options):
    """
    Returns a list of protogene with the given class and options.
    Names of protogenes are constructed by prepending a prefix to the position
    in the list. All protogenes will share the same options.
    
    :param gene_class: subclass :class:`genepi.core.gene.BaseGene`
    :param prefix: a string used for building the name of the protogene
    :param number: the number of the protogenes to be created
    :param **options: the options to be passed to gene constructor
    """
    out = []
    for i in range(number):
        name = "%s%d" % (prefix, i)
        protogene =  ProtoGene(gene_class, name, **options)
        out.append(protogene)
    return out