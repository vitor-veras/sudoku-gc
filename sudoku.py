from graph_utils import *
from sys import setrecursionlimit

setrecursionlimit(1000)
read_sudoku()
for solution in colorize_sudoku(None, False):
    print("Solved Sudoku: ")
    print_sudoku(solution)
    print()
