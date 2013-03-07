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
            ok_s = ok_r = ok_c = False
            
            if len(set(r)) == 9:
                ok_r = True
                score += 1
            if len(set(c)) == 9:
                score += 1
                ok_c = True
            if len(set(s)) == 9:
                score += 1
                ok_s = True
                
            if ok_r and ok_c and ok_s:
                score +=3
    return score        
            
    
from genepi.core.protogene import ProtoGene
from genepi.core.protogenome import ProtoGenome
from genepi.core.gene import DiscreteGene
from genepi.core.ga import GeneticAlgorithm
from genepi.core.crossover import single_point_crossover
from genepi.core.selectors import roulette_select, select_from_top
from genepi.core.stopcriteria import raw_score_stop


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
        
        numbers_in_row = [x for x in board.get_row(row) if x is not None]
        numbers_in_col = [x for x in board.get_col(col) if x is not None]
        numbers_in_square  = [x for x in board.get_square(row, col) if x is not None]        

        alleles = [x for x in alleles if (x not in numbers_in_row)]
        alleles = [x for x in alleles if (x not in numbers_in_col)]
        alleles = [x for x in alleles if (x not in numbers_in_square)]
        
        protogenes.append(ProtoGene(DiscreteGene, name, alleles=alleles))
    

    protogenome = ProtoGenome(protogenes, mutation_probability=0.1)
    
    algo = GeneticAlgorithm(protogenome, sudoku_fitness, 
        population_size = 400,
        optimization_mode = 'max',
        num_parents = 4,
        crossover_method = single_point_crossover,
        crossover_probability=0.3,
        selection_method = select_from_top,
        termination_criteria=[raw_score_stop], termination_criteria_options=[{'stop_score':81*3*2}])
    
    
    algo.evolve(debug=True)
    bi = algo.best_individual()
    print bi.dict_value()