import os
base_path = os.path.dirname(__file__)
from sudokuboard import SudoBoard



filename = os.path.join(base_path, "sudoku.txt")
board = SudoBoard(filename)
    
    
def sudoku_fitness(solution):
    score = 0
    solution_values = solution.dict_value()
    filled_board = board.get_filled_board(solution_values)
    
    #
    for x in range(9):
        r = board.get_row(x, filled_board)
        items_row = len(set(r))
        score += 9 - items_row

    #
    for y in range(9):
        c = board.get_col(y, filled_board)
        items_col = len(set(c))
        score += 9 - items_col
        
    for x in range(3):
        for y in range(3):
            s = board.get_square(x*3, y*3, filled_board)
            items_sqa = len(set(s))
            score += (9 - items_sqa)
            
                
    """
    #each cell
    for x in range(9):
        for y in range(9):
            r = board.get_row(x, filled_board)
            c = board.get_col(y, filled_board)
            s = board.get_square(x, y, filled_board)
            
            #score += len(set(r)) + len(set(c)) +  len(set(s))
             
            ok_s = ok_r = ok_c = False
            
            if len(set(r)) == 9:
                ok_r = True
            if len(set(c)) == 9:
                ok_c = True
            if len(set(s)) == 9:
                ok_s = True
                
            num_ok = [ok_r, ok_c, ok_s]
            num_ok = [x for x in num_ok if x]
            
            score += len(num_ok)
            #bonus pont
            if len(num_ok) == 3:
                score += 30
    """
            
    return score 
            
    
from genepi.core.protogene import ProtoGene
from genepi.core.protogenome import ProtoGenome
from genepi.core.gene import DiscreteGene
from genepi.core.multiga import MultiGeneticAlgorithm
from genepi.core.ga import GeneticAlgorithm
from genepi.core.crossover import single_point_crossover
from genepi.core.selectors import roulette_select, select_from_top, simple_tournament_select
from genepi.core.stopcriteria import raw_score_stop



def test_6():   
    #not yet converging!
    return
    
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
    

    protogenome = ProtoGenome(protogenes, mutation_probability=0.01)
    
    algo = GeneticAlgorithm(protogenome, sudoku_fitness, 
        population_size = 200,
        #num_populations=1,
        #isolated_cycles=8,
        optimization_mode = 'min',
        num_parents = 2,
        #elitism = False,
        crossover_method = single_point_crossover,
        crossover_probability=.5,
        selection_method = simple_tournament_select,
        termination_criteria=[raw_score_stop], termination_criteria_options=[{'stop_score':0}])
    
    
    algo.evolve(debug=True)
    bi = algo.best_individual()
    print bi.dict_value()