import math
from genepi.core.ga import GeneticAlgorithm
from genepi.core.protogenome import ProtoGenome
from genepi.core.protogene import ProtoGene
from genepi.core.gene import FloatGene
from genepi.core.stopcriteria import raw_score_stop, convergence_stop
from genepi.core.crossover import single_point_crossover, genome_add, genome_choose
from genepi.core.selectors import roulette_select, select_from_top



def schafferF6(genome):
    values = genome.list_value()
    t1 = math.sin(math.sqrt(values[0]**2 + values[1]**2));
    t2 = 1.0 + 0.001*(values[0]**2 + values[1]**2);
    score = 0.5 + (t1*t1 - 0.5)/(t2*t2)
    return score

    
def test_1():
    pg_1 = ProtoGene(FloatGene, max_value=150.0, min_value=-150.0, mutation_max_step=10)
    pg_2 = ProtoGene(FloatGene, max_value=150.0, min_value=-150.0, mutation_max_step=10)
    protogenes = [pg_1, pg_2]
    protogenome = ProtoGenome(protogenes, mutation_probability = 0.15) 
    algo = GeneticAlgorithm(protogenome, schafferF6, 
        population_size = 200,
        optimization_mode = 'min',
        num_parents = 8,
        #elitism = False,
        crossover_method = single_point_crossover,
        crossover_probability = 0.5,
        selection_method = roulette_select,
        termination_criteria = convergence_stop, num_generations=20)
        
    algo.evolve(debug=True)
    bi = algo.best_individual()
    print bi.score
    print bi.dict_value()
    
    