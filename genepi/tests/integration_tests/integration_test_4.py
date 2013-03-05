"""
testing mutation_wrapper_method and crossover_wrapper_method
"""

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


def mutation_wrapper_method(population, genome, **options):
    fact = options['last_stats']['idle_cycles'] * 0.01
    mutation_probability = genome.mutation_probability * ( 1 + fact )
    #print "m", mutation_probability, options['last_stats']['idle_cycles']
    g = genome.mutate(probability=mutation_probability)
    return g
    
def crossover_wrapper_method(genome_a, genome_b, **options):
    ga_engine = options['ga_engine']
    fact = options['last_stats']['idle_cycles'] * 0.01
    options['crossover_probability'] = ga_engine.crossover_probability * ( 1 + fact )
    out = ga_engine.population.apply_crossover([genome_a, genome_b], **options)
    return out
    
def test_4():
    pg_1 = ProtoGene(FloatGene, max_value=150.0, min_value=-150.0, mutation_max_step=10)
    pg_2 = ProtoGene(FloatGene, max_value=150.0, min_value=-150.0, mutation_max_step=10)
    protogenes = [pg_1, pg_2]
    protogenome = ProtoGenome(protogenes, mutation_probability = 0.05) 
    algo = GeneticAlgorithm(protogenome, schafferF6, 
        population_size = 400,
        optimization_mode = 'min',
        mutation_wrapper_method = mutation_wrapper_method,
        crossover_wrapper_method = crossover_wrapper_method,
        num_parents = 10,
        #elitism = False,
        crossover_method = [single_point_crossover, genome_add],
        crossover_probability = 0.5,
        selection_method = select_from_top,
        termination_criteria = convergence_stop,
        termination_criteria_options={'num_generations':50}
    )
        
    algo.evolve(debug=True)
    bi = algo.best_individual()
    print bi.score
    print bi.dict_value()
    

if __name__ == '__main__':
    test_4()