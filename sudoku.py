from graph_utils import *
from sys import setrecursionlimit

setrecursionlimit(100)
read_puzzle()
for solution in color_puzzle(None, False):
    print("Solved Sudoku: ")
    print_solution(solution)
    print()
