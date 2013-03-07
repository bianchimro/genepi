import os

class SudoBoard(object):

    num_rows = 9
    num_cols = 9
    data = dict()

    def __init__(self, filename):
        with open(filename, "rb") as f:
            content = f.read().replace("\r",'').replace("\n", '')        
        for pos, char in enumerate(content):
            row = pos/9
            col = pos % 9
            try:
                value = int(char)
            except:
                value = None
            if not value:
                value = None
            self.data[(row, col)] = value
        
        
    def get_row(self, row_idx, data=None):
        lookup = data or self.data
        numbers_in_row = [lookup[(row_idx, c)] for c in range(9)]
        return numbers_in_row
        
    def get_col(self, col_idx, data=None):
        lookup = data or self.data
        numbers_in_col = [lookup[(r, col_idx)] for r in range(9)]
        return numbers_in_col
        
    def get_square(self, row_idx, col_idx, data=None):
        lookup = data or self.data    
        square_start_row = (row_idx / 3) * 3
        square_start_col = (col_idx / 3) * 3
        square_end_row = square_start_row + 3
        square_end_col = square_start_col + 3
        numbers_in_square = []
        for i in range(square_start_row, square_end_row):
            for j in range(square_start_col, square_end_col):
                numbers_in_square.append(lookup[(i,j)])
        return numbers_in_square
        
    def get_filled_board(self, solution_values):
        filled_board = {}
        for row in range(9):
            for col in range(9):
                item = self.data[(row, col)]
                if item is None:
                    item = solution_values[str(row)+"_" + str(col)]
                filled_board[(row, col)] = item
        return filled_board


if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    filename = os.path.join(base_path, "sudoku.txt")
    board = SudoBoard(filename)
    print board.data
    print
    row = board.get_row(0)
    print row
    print
    col = board.get_col(0)
    print col
    print
    square = board.get_square(0,0)
    print square
    print
    square = board.get_square(1,1)
    print square
    print
    square = board.get_square(8,8)
    print square
