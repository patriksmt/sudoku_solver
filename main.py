from module import SudukoBoard
from colored import fore, back, style
import math

class Cell:
	def __init__(self, row, col):
		self.candidate_numbers = [1,2,3,4,5,6,7,8,9]
		self.fixed = False
		self.found = False
		self.value = '-'
		self.row = row
		self.col = col

	def get_address(self):
		return [self.row, self.col]

	def get_cluster(self):
		if self.row < 3:
			if self.col < 3:
				return 1
			if self.col >= 3 and self.col <= 5:
				return 2
			if self.col > 5:
				return 3

		if self.row <= 3 and self.row <= 5:
			if self.col < 3:
				return 4
			if self.col >= 3 and self.col <= 5:
				return 5
			if self.col > 5:
				return 6

		if self.row > 5:
			if self.col < 3:
				return 7
			if self.col >= 3 and self.col <= 5:
				return 8
			if self.col > 5:
				return 9

	def remove_candidate(self, possibility):
		"""
		Main removal function
		Returns 0 if the targeted cell is already found
		Returns -1 if the number was successfully removed from target cell
		Returns [1-9] if a number was removed and only a single number possiblity remains
		"""
		if self.found == True:
			return 0

		try:
			self.candidate_numbers.pop(self.candidate_numbers.index(int(possibility)))	
		except ValueError:
			pass

		if len(self.candidate_numbers) == 1:
			self.value = self.candidate_numbers[0]
			self.found = True
			return int(self.value)

		return -1

	def set_fixed(self, number):
		self.value = number
		self.fixed = True
		self.found = True
		self.candidate_numbers = [int(number)]

	def set_number(self, number):
		self.value = number
		self.candidate_numbers = [int(number)]
		self.found = True
		print('Found a new number')

	def get_candidates(self):
		return self.candidate_numbers

	def is_found(self):
		if self.found:
			return True

	def get_printable_candidates(self):
		printable_candidates = [1,2,3,4,5,6,7,8,9]
		for i in range(0,9):
			if (i + 1) not in self.candidate_numbers:
				printable_candidates[i] = '-'

		return printable_candidates




		



class Board:
	def __init__(self):
		self.board = []   
		for i in range (0, 9):  
		    row = []        
		    for j in range (0, 9): 
		        row.append(Cell(i, j))  
		    self.board.append(row)


	def check_if_single(self, row, col):
		if len(self.board[row][col].get_candidates) == 1:
			return True


	# def remove_candidate_row(self, number, row, ignore_list):
	# 	for i in range(0,9):
	# 		if i in ignore_list:
	# 			continue
	# 		else:	
	# 			if self.board[row][i].remove_candidate(number) == 1:
	# 				pass
	# 				#Call main tripple function


	# def remove_candidate_col(self, number, col, ignore_list):
	# 	for i in range(0,9):
	# 		if i in ignore_list:
	# 			continue
	# 		else:
	# 			if self.board[i][col].remove_candidate(number) == 1:
	# 				pass
	# 				#Call main tripple function

	# def remove_candidate_cluster(self, number, row, col, ignore_list):
	# 	row_cluster = math.floor(row / 3) * 3
	# 	col_cluster = math.floor(col / 3) * 3

	# 	for i in range(row_cluster, row_cluster + 3):
	# 		for j in range(col_cluster, col_cluster + 3):
	# 			if [i,j] in ignore_list:
	# 				continue
	# 			else:
	# 				if self.board[i][j].remove_candidate(number) == 1:
	# 					pass
	# 					#Call main tripple function


	def solve(self):
		#Loop over all cells on the board
		for row in range(0,9):
			for col in range(0,9):
				#Check if the the cell in question is found 
				if self.board[row][col].is_found():
					#If we know a fixed number, go ahread and eliminate that number from row, col, cluster
					self.basic_eliminations(self.board[row][col].value, row, col)



	def basic_eliminations(self, number, row, col):
		#Iterate over all cells in the row and column for the specific elimination
		for current_iterator in range(0,9):
			#If there were only 1 value left in the call the remove_candidate method will return with the number that was found
			#with that number we can ecursivley call this function to do basic eliminations again on that cell
			
			if self.board[row][current_iterator].remove_candidate(number) > 0:
				# The removal returned the number which is now the single remaining
				# Recursivly call this function to run another round of eliminations
				self.basic_eliminations(self.board[row][current_iterator].value, row, current_iterator)

			if self.board[current_iterator][col].remove_candidate(number) > 0:
				
				self.basic_eliminations(self.board[current_iterator][col].value, current_iterator, col)

		# This section is to determine a 3x3 cluster of numbers and eliminate candidates from that cluster
		row_cluster = math.floor(row / 3) * 3
		col_cluster = math.floor(col / 3) * 3

		for i in range(row_cluster, row_cluster + 3):
			for j in range(col_cluster, col_cluster + 3):
				if self.board[i][j].remove_candidate(number) > 0:
					self.basic_eliminations(self.board[i][j].value, i, j)
					


	def evaluate_cluster(self, cluster_row, cluster_col):
		overlap_set = [0,0,0,0,0,0,0,0,0]
		for i in range(cluster_row, cluster_row + 3):
			for j in range(cluster_col, cluster_col + 3):
				if self.board[i][j].value == '-':
					for n in self.board[i][j].candidate_numbers:
						overlap_set[n - 1] += 1

		magic_number = 0

		for index, item in enumerate(overlap_set):  
			if item == 1:
				print('A one was found in index number {}'.format(index))
				magic_number = index
				print(overlap_set)

				for i in range(cluster_row, cluster_row + 3):
					for j in range(cluster_col, cluster_col + 3):
						if self.board[i][j].value == '-':
							for n in self.board[i][j].candidate_numbers:
								if n == magic_number + 1:
									print(magic_number)
									print('hello')
									print(self.board[i][j].candidate_numbers)
									print('In row {}, col {}, we found a unique {}'.format(i,j,magic_number+1))
									self.board[i][j].set_number(magic_number+1)
						

	def evaluate_clusters(self):
		for i in range(0, 3):
			for j in range(0, 3):
				print('evaluating cluster starting in {}, {}'.format(i*3,j*3))
				self.evaluate_cluster(i * 3, j * 3)

	def naked_subset(self):
		for i in range(0,81):
			for j in range(i + 1, 81):

				base_row = math.floor(i / 9)
				base_col = i - (math.floor(i / 9)) * 9

				compare_row = math.floor(j / 9)
				compare_col = j - (math.floor(j / 9)) * 9

				if self.board[base_row][base_col].get_candidates() == self.board[compare_row][compare_col].get_candidates() and len(self.board[compare_row][compare_col].get_candidates()) == 2:
					# print('Found a match')
					# print(self.board[base_row][base_col].get_candidates())
					# print('Between: {} and {}, and {} and {}'.format(base_row, base_col, compare_row, compare_col))
					
					#Check if the two cells are in the same row, col, or box. If so, remove all other candidates
					if base_row == compare_row:
						for n in self.board[base_row][base_col].get_candidates():
							ignore_list = [base_col, compare_col]
							self.remove_row(n, base_row, ignore_list)

					if base_col == compare_col:
						for n in self.board[base_row][base_col].get_candidates():
							ignore_list = [base_row, compare_row]
							self.remove_col(n, base_col, ignore_list)

					if self.board[base_row][base_col].get_cluster() == self.board[compare_row][compare_col].get_cluster():
						for n in self.board[base_row][base_col].get_candidates():
							ignore_list = [[base_row, base_col], [compare_row, compare_col]]
							self.remove_cluster(n, base_row, base_col, ignore_list)


	def sum_sets(self):
		tree = {}
		
		for i in range(0,81):
			row = math.floor(i / 9)
			col = i - (math.floor(i / 9)) * 9

			if len(self.board[row][col].get_candidates()) == 1:
				continue

			item_list = ''
			for n in self.board[row][col].get_candidates():
				item_list = item_list + str(n)

			if item_list not in tree:
				tree[item_list] = 1
			else:	
				tree[item_list] += 1

		print(tree)

	def render_board(self):		
		for i in range(0,37):
			print(fore.RED + "-" + style.RESET, end='')
		print()

		for i in range(0,9):
			for j in range(0,9):
				if j % 3 == 0:
					print(fore.RED + '|' + style.RESET, end='')
				else:
					print('|', end='')
				if self.board[i][j].fixed == True:
					print(fore.BLUE, end='')
				print(' {} '.format(self.board[i][j].value), end='')
				print(style.RESET, end='')
			print(fore.RED + '|' + style.RESET)

			for k in range(0,37):
				if (i + 1) % 3 == 0:
					print(fore.RED + '-' + style.RESET, end='')
				else:
					print('-', end='')
			print()

	def render_possibility_space(self, row, col):
		a = self.board[int(row)][int(col)].get_printable_candidates()
		print('{} {} {}'.format(a[0],a[1],a[2]))
		print('{} {} {}'.format(a[3],a[4],a[5]))
		print('{} {} {}'.format(a[6],a[7],a[8]))


	def render_solution_space(self):
		for i in range(0,73):
			print(fore.RED + "-" + style.RESET, end='')
		print()
		for k in range(0,9):
			for j in range(0,3):
				print(fore.RED + '| ' + style.RESET, end='')	
				for i in range(0,9):
					if self.board[k][i].found == True:
						print(fore.GREEN, end='')
					if self.board[k][i].fixed == True:
						print(fore.BLUE, end='')
					print(self.board[k][i].get_printable_candidates()[j*3], end='')
					print(' ', end='')
					print(self.board[k][i].get_printable_candidates()[j*3+1], end='')
					print(' ', end='')
					print(self.board[k][i].get_printable_candidates()[j*3+2], end='')
					print(style.RESET, end='')
					if (i + 1) % 3 == 0:
						print(fore.RED + ' | ' + style.RESET, end='')
					else:
						print(' | ', end='')
				print()
			if (k + 1) % 3 == 0:
				for i in range(0,73):
					print(fore.RED + "-" + style.RESET, end='')
			else:
				for i in range(0,73):
					print("-", end='')
			print()

	def read_file(self):
		#file_name = input('File name: ')
		file_name = '2.txt'
		f = open(file_name, "r")

		row_num = 0
		col_num = 0

		for l in f:
			col_num = 0
			for n in l:
				if n != '-' and n != '\n':
					#print('Row: {}  Col: {} - inserting {}'.format(row_num, col_num, n))
					self.board[row_num][col_num].set_fixed(n)

				col_num += 1
			row_num += 1
		print('Read complete')



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
	if inst == 'e': #e - Evaluate
		b.evaluate_clusters()

	#RENDER FUNCTIONS
	if inst == 'r': #r - Render
		b.render_board()
	if inst == 'c': #c - render Candidates
		b.render_solution_space()
	if inst == 'li': #l - render local candidates
		row = input('Row: ')
		col = input('Column: ')
		b.render_possibility_space(row, col)
	if inst == 'ss':
		b.sum_sets()
	if inst == 'test':
		b.find_pairs()
	
	#MISC FUNCTIONS
	if inst == 'exit' or inst == 'quit':
		break

	if inst == 'n':
		b.naked_subset()
	
