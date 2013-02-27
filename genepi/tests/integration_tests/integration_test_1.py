from genepi.core.ga import GeneticAlgorithm
from genepi.core.factories import protogene_factory
from genepi.core.protogenome import ProtoGenome
from genepi.core.gene import IntGene
from genepi.core.stopcriteria import raw_score_stop, convergence_stop
from genepi.core.crossover import single_point_crossover
from genepi.core.population import roulette_select

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def fitness_function(genome):
    score = 0.0
    for value in genome.list_value():
        score += value
        #if value == 0:
        #    score += 1
    return score
    
def test_1():
    protogenes = protogene_factory(IntGene, 'x', 14, min_value=0, max_value=100)
    protogenome = ProtoGenome(protogenes) 
    algo = GeneticAlgorithm(protogenome, fitness_function, 
        population_size = 100,
        optimization_mode = 'min',
        mutation_probability = 0.05,
        num_parents = 4,
        crossover_method = single_point_crossover,
        selection_method = roulette_select,
        termination_criteria=[raw_score_stop], stop_score=0)
    algo.evolve()
    bi = algo.best_individual()
    print bi.score
    print bi.dict_value()
    
    