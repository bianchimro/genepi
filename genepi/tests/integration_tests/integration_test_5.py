import math
from genepi.core.ga import GeneticAlgorithm
from genepi.core.protogenome import ProtoGenome
from genepi.core.protogene import ProtoGene
from genepi.core.gene import CharGene
from genepi.core.stopcriteria import raw_score_stop, convergence_stop
from genepi.core.crossover import single_point_crossover, genome_add, genome_choose
from genepi.core.selectors import roulette_select, select_from_top
from genepi.core.factories import protogene_factory


def findname(genome):
    values = genome.list_value()
    name = "".join(values) 
    ok = [ord(x) for x in "genepi"]
    ge = [ord(x) for x in values]
    score = 0
    for i,x in enumerate(ok):
        score += abs(ok[i] - ge[i])
    return score

    
def test_1():
    num_letters = len("genepi")
    protogenes = protogene_factory(CharGene, 'x', num_letters)
    protogenome = ProtoGenome(protogenes, mutation_probability = 0.05) 
    algo = GeneticAlgorithm(protogenome, findname, 
        population_size = 200,
        optimization_mode = 'min',
        num_parents = 8,
        #elitism = False,
        crossover_method = single_point_crossover,
        crossover_probability = 0.5,
        selection_method = select_from_top,
        termination_criteria = raw_score_stop, stop_score=0)
        
    algo.evolve(debug=True)
    bi = algo.best_individual()
    print bi.score
    print "".join(bi.list_value())
    
    