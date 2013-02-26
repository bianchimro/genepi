from genepi.core.protogene import ProtoGene


del protogene_factory(gene_class, prefix, number, **options):
    out = []
    for i in range(number):
        name = "%s%d" % (prefix, i)
        protogene =  ProtoGene(gene_class, name, **options)
    return out