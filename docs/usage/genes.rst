Built-in genes
==============

genepi comes with a set of built-in genes:

* IntGene
* FloatGene
* CharGene
* BitGene
* DiscreteGene


IntGene
-------


FloatGene
---------


CharGene
--------


BitGene
-------


DiscreteGene
------------

This gene represents a variable which domain is a predefined list of objects.
The list may contain any python object. In genepi, the domain of a discrete gene is
called **alleles** .

.. code-block:: python

    >>> from genepi.core.gene import DiscreteGene
    >>> g = DiscreteGene(alleles=[1,2,3])


