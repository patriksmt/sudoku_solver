from module import SudukoBoard
from colored import fore, back, style
from board import Board
from cell import Cell
import math

b = Board()

#main instructions loop
while True:
	
	raw_inst = input('Instruction: ')
	inst = raw_inst[:4]

	#INPUT FUNCTIONS
	if inst == 'l': #l - Load
		b.read_file()

	#SOLVE FUNCTIONS
	if inst == 's': #s - Solve
		b.solve()
	if inst == 'u': #u - Unique
		b.find_unique_candidates()
	if inst == 'e': #e - Evaluate
		b.evaluate_clusters()

	#RENDER FUNCTIONS
	if inst == 'r': #r - Render
		b.render_board()
	if inst == 'c': #c - render Candidates
		b.render_solution_space()
	if inst == 'ss':
		b.sum_sets()
	if inst == 'test':
		b.find_pairs()
	
	#MISC FUNCTIONS
	if inst == 'exit' or inst == 'quit':
		break

	if inst == 'n':
		b.naked_subset()
	



"""
Execution order:
1. Basic and recursive eliminations. After this we have removed all candidate numbers from cells
which are in the same row, col, and cluster as the found number

2. Lonely candidate in row, col, and cluster. 
At this stage we can still have rows, cols, and clusters where a given candiate is only present in one cell,
but it still has other candidates in it which are also in other cells in the same row, col, cluster.
Here we evaluate in which rows, cols, and clusters this is happening and if a number if found we re-cursivly re-evaluate.
"""