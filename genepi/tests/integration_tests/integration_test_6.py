import os
base_path = os.path.dirname(__file__)
from sudokuboard import SudoBoard



filename = os.path.join(base_path, "sudoku.txt")
board = SudoBoard(filename)
    
    
def sudoku_fitness(solution):
    score = 0
    solution_values = solution.dict_value()
    filled_board = board.get_filled_board(solution_values)
    
    #each cell
    for x in range(9):
        for y in range(9):
            r = board.get_row(x, filled_board)
            c = board.get_col(y, filled_board)
            s = board.get_square(x, y, filled_board)
            
            score += len(set(r)) + len(set(c)) +  len(set(s))
             
            ok_s = ok_r = ok_c = False
            
            if len(set(r)) == 9:
                ok_r = True
                #score += 1
            if len(set(c)) == 9:
                #score += 1
                ok_c = True
            if len(set(s)) == 9:
                #score += 1
                ok_s = True
                
            num_ok = [ok_r, ok_c, ok_s]
            num_ok = [x for x in num_ok if x]
            score += len(num_ok) * 9
            
    return score        
            
    
from genepi.core.protogene import ProtoGene
from genepi.core.protogenome import ProtoGenome
from genepi.core.gene import DiscreteGene
from genepi.core.ga import GeneticAlgorithm
from genepi.core.crossover import single_point_crossover
from genepi.core.selectors import roulette_select, select_from_top, half_from_top
from genepi.core.stopcriteria import raw_score_stop

def mutation_wrapper_method(population, genome, **options):
    idle_cycles = options['last_stats']['idle_cycles']
    """
    if idle_cycles > 50:
        mutation_probability = genome.mutation_probability * 2
    else:
        mutation_probability = genome.mutation_probability
    """
    mutation_probability = genome.mutation_probability * (1 - idle_cycles * 0.001)
    #print "m", mutation_probability, options['last_stats']['idle_cycles']
    #print mutation_probability
    mutation_probability = max(mutation_probability, 0)
    g = genome.mutate(probability=mutation_probability)
    return g

def crossover_wrapper_method(genome_a, genome_b, **options):
    ga_engine = options['ga_engine']
    fact = options['last_stats']['idle_cycles'] * 0.01
    options['crossover_probability'] = ga_engine.crossover_probability * ( 1 - fact )
    out = ga_engine.population.apply_crossover([genome_a, genome_b], **options)
    return out


def test_6():
    protogenes = []    
    for square in board.data.keys():
        row = square[0]
        col = square[1]
        value = board.data[(row, col)]
        if value:
            continue
            
        name = str(row) + "_" + str(col)
        alleles = range(1,10)
        
        numbers_in_row = [x for x in board.get_row(row) if x ]
        numbers_in_col = [x for x in board.get_col(col) if x ]
        numbers_in_square  = [x for x in board.get_square(row, col) if x]        

        alleles = [x for x in alleles if (x not in numbers_in_row)]
        alleles = [x for x in alleles if (x not in numbers_in_col)]
        alleles = [x for x in alleles if (x not in numbers_in_square)]
        
        protogenes.append(ProtoGene(DiscreteGene, name, alleles=alleles))
    

    protogenome = ProtoGenome(protogenes, mutation_probability=0.1)
    
    algo = GeneticAlgorithm(protogenome, sudoku_fitness, 
        population_size = 100,
        optimization_mode = 'max',
        num_parents = 2,
        #elitism = False,
        crossover_method = single_point_crossover,
        crossover_probability=0.3,
        mutation_wrapper_method = mutation_wrapper_method,
        #crossover_wrapper_method = crossover_wrapper_method,
        selection_method = roulette_select,
        termination_criteria=[raw_score_stop], termination_criteria_options=[{'stop_score':81 * 36 + 81*27}])
    
    
    algo.evolve(debug=True)
    bi = algo.best_individual()
    print bi.dict_value()