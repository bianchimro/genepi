import math
from genepi.core.ga import GeneticAlgorithm
from genepi.core.protogenome import ProtoGenome
from genepi.core.protogene import ProtoGene
from genepi.core.gene import FloatGene, DiscreteGene
from genepi.core.stopcriteria import raw_score_stop, convergence_stop
from genepi.core.crossover import single_point_crossover, genome_add, genome_choose
from genepi.core.selectors import roulette_select, select_from_top



def schafferF6(genome):
    values = genome.list_value()
    t1 = math.sin(math.sqrt(values[0]**2 + values[1]**2));
    t2 = 1.0 + 0.001*(values[0]**2 + values[1]**2);
    score = 0.5 + (t1*t1 - 0.5)/(t2*t2)
    return score

    
def genetic_fitness(genome):
    values = genome.dict_value()
    
    pg_1 = ProtoGene(FloatGene, max_value=150.0, min_value=-150.0, mutation_max_step=5)
    pg_2 = ProtoGene(FloatGene, max_value=150.0, min_value=-150.0, mutation_max_step=5)
    protogenes = [pg_1, pg_2]
    protogenome = ProtoGenome(protogenes) 
    algo = GeneticAlgorithm(protogenome, schafferF6, 
        population_size = values['pop_size'],
        optimization_mode = 'min',
        mutation_probability = values['mutation_probability'],
        num_parents = values['num_parents'],
        #elitism = False,
        crossover_method = values['crossover_method'],
        crossover_probability =values['crossover_probability'],
        selection_method = select_from_top,
        termination_criteria = convergence_stop, num_generations=5)
        
    algo.evolve()
    bi = algo.best_individual()
    print bi.score
    return bi.score
    
    
def test_3():
    pop_size = ProtoGene(DiscreteGene, 'pop_size', alleles=[100,200,300])
    mutation_probability = ProtoGene(DiscreteGene, 'mutation_probability', alleles=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5])
    num_parents = ProtoGene(DiscreteGene, 'num_parents', alleles=[2,4,8,16])
    crossover_probability = ProtoGene(DiscreteGene, 'crossover_probability', alleles=[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    crossover_method = ProtoGene(DiscreteGene, 'crossover_method', alleles=[single_point_crossover, genome_add, genome_choose])
    protogenome = ProtoGenome([pop_size, mutation_probability, num_parents, crossover_probability, crossover_method]) 
    
    algo = GeneticAlgorithm(protogenome, genetic_fitness, 
        population_size = 10,
        optimization_mode = 'min',
        termination_criteria = convergence_stop, num_generations=5)
        
    algo.evolve(debug=True)
    bi = algo.best_individual()
    print "*" * 10
    print bi.dict_value()
    return bi.score