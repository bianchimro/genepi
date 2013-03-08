"""
This module contains the core selector methods provided by genepi.
"""

import random


def select_from_top(population, num_individuals):
    """
    Select the first individuals ordered by score.
    """
    return population.individuals[:num_individuals]


def half_from_top(population, num_individuals):
    """
    Select the first individuals ordered by score.
    """
    best_ind = num_individuals/2
    set_1 = population.individuals[:best_ind]
    set_2 = []
    for x in range(num_individuals-best_ind):
        set_2.append(random.choice(population.individuals))
    return set_1 + set_2


    
    
def roulette_select(population, num_individuals):
    """ 
    Roulette selection, implemented according to:
    http://stackoverflow.com/questions/177271/roulette-selection-in-genetic-algorithms/177278#177278
    """
    
    current_scaled_scores = population.current_scaled_scores
#    print current_scaled_scores
#    total_sum = float(sum(current_scaled_scores))
#    print "t", total_sum
#    probs = [float(x.score)/total_sum for x in population.individuals]
#    print probs
#    print sum(probs)
#    assert sum(probs) == 1.0
#    raise
    
    # Generate probability intervals for each individual
    probs = [sum(current_scaled_scores[:i+1]) for i in range(len(current_scaled_scores))]
    if sum(probs) == 0:
        return random.sample(population.individuals, 2)
    # Draw new population
    new_population = []
    for n in xrange(num_individuals):
        r = random.random()
        for (i, individual) in enumerate(population.individuals):
            if r <= probs[i]:
                new_population.append(individual)
                break
    return new_population
