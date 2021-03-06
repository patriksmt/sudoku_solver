from cell import Cell
from colored import fore, back, style
import math

class Board:
	def __init__(self):
		self.board = []   
		for i in range (0, 9):  
		    row = []        
		    for j in range (0, 9): 
		        row.append(Cell(i, j))  
		    self.board.append(row)

	def read_file(self):
		#file_name = input('File name: ')
		file_name = '3.txt'
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


	def solve(self):
		#Loop over all cells on the board
		for row in range(0, 9):
			for col in range(0, 9):
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
					

	def find_unique_candidates(self):
		# 1. Iterate over all 9 rows on the board to find rows with unique candidates
		overlap_array = [0,0,0,0,0,0,0,0,0]

		for investigated_row in range(0,9):
			for current_col in range(0, 9):
				if self.board[investigated_row][current_col].value == '-':
					for n in self.board[investigated_row][current_col].candidate_numbers:
						overlap_array[n - 1] += 1
			print([1,2,3,4,5,6,7,8,9])
			print(overlap_array)
			print()

			for index, item in enumerate(overlap_array):
				# Check if we have a position with a 1, meaning we found a unique value  
				if item == 1:
					print('A one was found in row {}. It was for number {}'.format(investigated_row, index + 1))
					print()
					print(self.find_address_of_unique_number("row", investigated_row, index + 1))
					
					self.board[investigated_row][self.find_address_of_unique_number("row", investigated_row, index + 1)].set_number(index + 1)
					#Here we must trigger new step 1 eliminations
					self.solve()
					#Recursivly run this function again given the new info
					self.find_unique_candidates()
			overlap_array = [0,0,0,0,0,0,0,0,0]


		# 2. Iterate over all 9 cols on the board to find cols with unique candidates

		for investigated_col in range(0, 9):
			for current_row in range(0, 9):
				if self.board[current_row][investigated_col].value == '-':
					for n in self.board[current_row][investigated_col].candidate_numbers:
						overlap_array[n - 1] += 1
			print([1,2,3,4,5,6,7,8,9])
			print(overlap_array)
			print()

			for index, item in enumerate(overlap_array):
				# Check if we have a position with a 1, meaning we found a unique value  
				if item == 1:
					print('A one was found in col {}. It was for number {}'.format(investigated_col, index + 1))
					print()
					print(self.find_address_of_unique_number("col", investigated_col, index + 1))
					
					self.board[self.find_address_of_unique_number("col", investigated_col, index + 1)][investigated_col].set_number(index + 1)
					#Here we must trigger new step 1 eliminations
					self.solve()
					#Recursivly run this function again given the new info
					self.find_unique_candidates()
			overlap_array = [0,0,0,0,0,0,0,0,0]

		# 3. Iterate over all 9 clusters on the board to find clusters with unique candidates

		print("Starting on Cluster evaluation")
		for cluster_row in range(0, 3):
			for cluster_col in range(0, 3):
				print('Evaluating cluster starting in {}, {}'.format(cluster_row*3,cluster_col*3))

				overlap_array = [0,0,0,0,0,0,0,0,0]
				for i in range(cluster_row * 3, (cluster_row * 3) + 3):
					for j in range(cluster_col * 3, (cluster_col * 3) + 3):
						if self.board[i][j].value == '-':
							for n in self.board[i][j].candidate_numbers:
								overlap_array[n - 1] += 1
				
				print([1,2,3,4,5,6,7,8,9])
				print(overlap_array)
				print()

				for index, item in enumerate(overlap_array):  
					if item == 1:
						print('A one was found in index number {}'.format(index))

				#MUST CALL find_address_of_unique_number HERE!!!


	def find_address_of_unique_number(self, variant, index, number):
		"""
		Variant: row, col, cluster
		Index: index of the variant, 0 based
		Number: Which number should be found
		"""
		if variant == "row":
			for i in range(0, 9):
				if number in self.board[index][i].candidate_numbers:
					return(i)
					# could send the address if more than one, for now only using this func
					# to search for a single cell

		if variant == "col":
			for i in range(0, 9):
				if number in self.board[i][index].candidate_numbers:
					return(i)

		if variant == "cluster":
			for i in range(index[0], index[0] + 3):
					for j in range(index[1], index[1] + 3):
						if self.board[i][j].value == '-':
							for n in self.board[i][j].candidate_numbers:
								if n == number:
									print(magic_number)
									print(self.board[i][j].candidate_numbers)
									print('In row {}, col {}, we found a unique {}'.format(i,j,magic_number+1))
									self.board[i][j].set_number(magic_number+1)



				
	"""
	Identify cells which have the same candidates
	Look at each row, col, and cluster. Take a fingerprint of each cell and count if there are multiple 
	instances of that finger print
	In Can make this work with tripels as well later to take fingerprints on subsets. 
	Create the fingerprint based on a hash table/dict. 
	"""
	def naked_subset(self):
		
		# Check each row
		for investigated_row in range(0, 9):
			# For each row, check each col in that row
			fingerprint_array = []
			for current_col in range(0, 9):
				if self.board[investigated_row][current_col].get_candidates():
					candidate_list = self.board[investigated_row][current_col].get_candidates()
					if candidate_list in fingerprint_array:
						print('Match found: {}, in row {}'.format(candidate_list, investigated_row + 1))
						if len(candidate_list) == 2:
							#Erase candidates from all other cells in the row
							print('Removing {}'.format(candidate_list))
							self.remove_candidates_from_row(investigated_row, candidate_list)
					else:
						fingerprint_array.append(candidate_list)

		# Check each col
		for investigated_col in range(0, 9):
			# For each row, check each col in that row
			fingerprint_array = []
			for current_row in range(0, 9):
				if self.board[current_row][investigated_col].get_candidates():
					candidate_list = self.board[current_row][investigated_col].get_candidates()
					if candidate_list in fingerprint_array:
						print('Match found: {}, in col {}'.format(candidate_list, investigated_col + 1))
						if len(candidate_list) == 2:
							#Erase candidates from all other cells in the row
							print('Removing {}'.format(candidate_list))
							self.remove_candidates_from_col(investigated_col, candidate_list)
					else:
						fingerprint_array.append(candidate_list)



		# for i in range(0,81):
		# 	for j in range(i + 1, 81):

		# 		base_row = math.floor(i / 9)
		# 		base_col = i - (math.floor(i / 9)) * 9

		# 		compare_row = math.floor(j / 9)
		# 		compare_col = j - (math.floor(j / 9)) * 9

		# 		if self.board[base_row][base_col].get_candidates() == self.board[compare_row][compare_col].get_candidates() and len(self.board[compare_row][compare_col].get_candidates()) == 2:
		# 			# print('Found a match')
		# 			# print(self.board[base_row][base_col].get_candidates())
		# 			# print('Between: {} and {}, and {} and {}'.format(base_row, base_col, compare_row, compare_col))
					
		# 			#Check if the two cells are in the same row, col, or box. If so, remove all other candidates
		# 			if base_row == compare_row:
		# 				for n in self.board[base_row][base_col].get_candidates():
		# 					ignore_list = [base_col, compare_col]
		# 					self.remove_row(n, base_row, ignore_list)

		# 			if base_col == compare_col:
		# 				for n in self.board[base_row][base_col].get_candidates():
		# 					ignore_list = [base_row, compare_row]
		# 					self.remove_col(n, base_col, ignore_list)

		# 			if self.board[base_row][base_col].get_cluster() == self.board[compare_row][compare_col].get_cluster():
		# 				for n in self.board[base_row][base_col].get_candidates():
		# 					ignore_list = [[base_row, base_col], [compare_row, compare_col]]
		# 					self.remove_cluster(n, base_row, base_col, ignore_list)

	def remove_candidates_from_row(self, row, candidate_list):
		for current_col in range(0, 9):
			if self.board[row][current_col].get_candidates() == candidate_list:
				print("This is the cell itself")
				continue
			for number in candidate_list:
				print("Removing candidate {}".format(number))
				self.board[row][current_col].remove_candidate(number)
	
	def remove_candidates_from_col(self, col, candidate_list):
		for current_row in range(0, 9):
			if self.board[current_row][col].get_candidates() == candidate_list:
				print("This is the cell itself")
				continue
			for number in candidate_list:
				print("Removing candidate {}".format(number))
				self.board[current_row][col].remove_candidate(number)

	def remove_candidates_from_cluster(self, cluster, candidate_list):
		pass

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


	"""
	RENDER FUNCTIONS
	Used to render board state to terminal. Can either render the basic board, showing the found numbers, or
	the full solution space, which lists the remaining candidate cells for every cell on the board.
	"""
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


