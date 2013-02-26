from genepi.core.ga import GeneticAlgorithm
from genepi.core.factories import protogene_factory
from genepi.core.protogenome import ProtoGenome
from genepi.core.gene import IntGene
from genepi.core.stopcriteria import raw_score_stop, convergence_stop
from genepi.core.population import genome_choose, single_point_crossover

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def fitness_function(genome):
    score = 0.0
    for value in genome.list_value():
        score += value
    return score
    
def test_1():
    protogenes = protogene_factory(IntGene, 'x', 50, min_value=0, max_value=10)
    protogenome = ProtoGenome(protogenes) 
    algo = GeneticAlgorithm(protogenome, fitness_function, 
        population_size = 100,
        optimization_mode = 'min',
        crossover_method = single_point_crossover,
        num_parents = 2,
        termination_criteria=[raw_score_stop], stop_score=0)
    algo.evolve()
    bi = algo.best_individual()
    print bi.score
    print bi.dict_value()
    
    