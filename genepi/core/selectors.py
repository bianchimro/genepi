"""
This module contains the core selector methods provided by genepi.
"""

import random
from genepi.utils.random_helpers import weighted_choice


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
        
    current_scores = population.current_scaled_scores
    sum_score = sum(current_scores)
    if sum_score == 0:
        return random.sample(population.individuals, num_individuals)
    
    probs = []
    ub = 0
    for i, score in enumerate(current_scores):
        lb, ub = ub, ub + score
        probs.append((lb, ub))
        
    # Draw new population
    new_population = []
    for n in xrange(num_individuals):
        r = random.uniform(0, sum_score)
        for (i, individual) in enumerate(population.individuals):
            if r > probs[i][0] and r <= probs[i][1]:
                new_population.append(individual)
                break
    return new_population


def simple_tournament_select(population, num_individuals):
    tournament_size = int(population.size / 10)
    new_population = []
    scored_items = zip(population.individuals, population.current_scaled_scores)
    for n in xrange(num_individuals):
        items = []
        for x in xrange(tournament_size):
            items.append(weighted_choice(scored_items))
        items.sort(population.cmp_individual)
        new_population.append(items[0])
    return new_population

    
    
    