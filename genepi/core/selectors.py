"""
This module contains the core selector methods provided by genepi.
"""

import random


def select_from_top(population, num_individuals):
    """
    Select the first individuals ordered by score.
    """
    return population.individuals[:num_individuals]
    
    
def roulette_select(population, num_individuals):
    """ 
    Roulette selection, implemented according to:
    http://stackoverflow.com/questions/177271/roulette-selection-in-genetic-algorithms/177278#177278
    """
    
    current_scaled_scores = population.current_scaled_scores
    
    # Generate probability intervals for each individual
    probs = [sum(current_scaled_scores[:i+1]) for i in range(len(current_scaled_scores))]
    # Draw new population
    new_population = []
    for n in xrange(num_individuals):
        r = random.random()
        for (i, individual) in enumerate(population.individuals):
            if r <= probs[i]:
                new_population.append(individual)
                break
    return new_population
