from genepi.core.protogene import ProtoGene


def protogene_factory(gene_class, prefix, number, **options):
    out = []
    for i in range(number+1):
        name = "%s%d" % (prefix, i)
        protogene =  ProtoGene(gene_class, name, **options)
        out.append(protogene)
    return out