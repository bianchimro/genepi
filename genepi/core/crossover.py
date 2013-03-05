"""
Built-in crossover methods
"""

import random

def genome_add(genome_a, genome_b):
    """
    Crossover using the __add__ method of genes
    """
    return genome_a + genome_b
    
def genome_choose(genome_a, genome_b):
    """
    Choose between one of the two genomes
    """
    return random.choice([genome_a, genome_b])
    
def single_point_crossover(genome_a, genome_b):
    """
    Performs single point crossover using genome method)
    """
    return genome_a.crossover(genome_b)
