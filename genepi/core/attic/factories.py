
#TODO: investigate these factory methods
def FloatGeneFactory(name, **kw):
    """
    Returns a new class object, being a subclass
    of FloatGene, with class attributes
    set from keywords
    """
    return new.classobj(name, (FloatGene,), **kw)


def IntGeneFactory(name, **kw):
    """
    Returns a new class object, being a subclass
    of IntGene, with class attributes
    set from keywords
    """
    return new.classobj(name, (IntGene,), **kw)


def CharGeneFactory(name, **kw):
    """
    Returns a new class object, being a subclass
    of CharGene, with class attributes
    set from keywords
    """
    return new.classobj(name, (CharGene,), **kw)


def AsciiCharGeneFactory(name, **kw):
    """
    Returns a new class object, being a subclass
    of AsciiCharGene, with class attributes
    set from keywords
    """
    return new.classobj(name, (AsciiCharGene,), **kw)

def PrintableCharGeneFactory(name, **kw):
    """
    Returns a new class object, being a subclass
    of PrintableGene, with class attributes
    set from keywords
    """
    return new.classobj(name, (AsciiCharGene,), **kw)

def DiscreteGeneFactory(name, **kw):
    """
    Returns a new class object, being a subclass
    of DiscreteGene, with class attributes
    set from keywords
    """
    return new.classobj(name, (DiscreteGene,), **kw)

# utility functions

def rndPair(geneclass):
    """
    Returns a gene pair, comprising two random
    instances of the given gene class
    """
    return (geneclass(), geneclass())



