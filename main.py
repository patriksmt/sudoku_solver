from module import SudukoBoard
from colored import fore, back, style
import math

class Cell:
	def __init__(self, row, col):
		self.remaining_numbers = [1,2,3,4,5,6,7,8,9]
		self.possibility_space = [1,2,3,4,5,6,7,8,9]
		self.fixed = False
		self.found = False
		self.value = '-'
		self.row = row
		self.col = col

	def get_possibilities(self):
		return len(self.remaining_numbers)

	def get_address(self):
		return [self.row, self.col]

	def remove_possibility(self, possibility):
		if self.fixed == True or self.found == True:
			return

		try:
			self.remaining_numbers.pop(self.remaining_numbers.index(int(possibility)))
			self.possibility_space[self.possibility_space.index(int(possibility))] = '-'
			
		except ValueError:
			pass

		if self.get_possibilities() == 1:
			#print(fore.GREEN + 'Only one possibility left. Inserting: {}'.format(self.remaining_numbers[0]) + style.RESET)
			self.value = self.remaining_numbers[0]
			self.found = True
			#trigger new removals

	def set_fixed(self, number):
		self.value = number
		self.fixed = True
		self.found = True
		for n in range(0,9):
			if n + 1 != int(number):
				self.possibility_space[n] = '-'

	def set_number(self, number):
		self.value = number
		self.remaining_numbers = [int(number)]
		self.found = True
		for n in range(0,9):
			if n + 1 != int(number):
				self.possibility_space[n] = '-'

		



class Board:
	def __init__(self):
		self.board = []   
		for i in range (0, 9):  
		    new = []        
		    for j in range (0, 9): 
		        new.append(Cell(i, j))  
		    self.board.append(new)

	def eliminate_row(self, number, row):
		for i in range(0,9):
			#print('(Row) Removing {} from row {}. Currently in col {}'.format(number, row, i))
			self.board[row][i].remove_possibility(number)


	def eliminate_col(self, number, col):
		for i in range(0,9):
			#print('(Col) Removing {} from col {}. Currently in row {}'.format(number, col, i))
			self.board[i][col].remove_possibility(number)

	def eliminate_cluster(self, number, row, col):
		row_cluster = math.floor(row / 3) * 3
		col_cluster = math.floor(col / 3) * 3

		for i in range(row_cluster, row_cluster + 3):
			for j in range(col_cluster, col_cluster + 3):
				#print('(Cluster) Removing {} from row {} and col {}'.format(number, i, j))
				self.board[i][j].remove_possibility(number)


	def evaluate_cluster(self, cluster_row, cluster_col):
		overlap_set = [0,0,0,0,0,0,0,0,0]
		for i in range(cluster_row, cluster_row + 3):
			for j in range(cluster_col, cluster_col + 3):
				if self.board[i][j].value == '-':
					for n in self.board[i][j].remaining_numbers:
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
							for n in self.board[i][j].remaining_numbers:
								if n == magic_number + 1:
									print(magic_number)
									print('hello')
									print(self.board[i][j].remaining_numbers)
									print('In row {}, col {}, we found a unique {}'.format(i,j,magic_number+1))
									self.board[i][j].set_number(magic_number+1)
						

	def evaluate_clusters(self):
		for i in range(0, 3):
			for j in range(0, 3):
				print('evaluating cluster starting in {}, {}'.format(i*3,j*3))
				self.evaluate_cluster(i * 3, j * 3)

	
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
		a = self.board[int(row)][int(col)].possibility_space
		print(fore.BLUE + 'Possibility space for row {} col {}'.format(row, col) + style.RESET)
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
					print(self.board[k][i].possibility_space[j*3], end='')
					print(' ', end='')
					print(self.board[k][i].possibility_space[j*3+1], end='')
					print(' ', end='')
					print(self.board[k][i].possibility_space[j*3+2], end='')
					print(fore.RED + ' | ' + style.RESET, end='')
				print()
			if (k-2) % 3 == 0:
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

	def solve(self):
		rotation = 0
		while rotation != 10:
			print(rotation)
			rotation += 1
			for i in range(0,9):
				for j in range(0,9):
					if self.board[i][j].value != '-':
						#print('Value {} in Row {} Col {}'.format(self.board[i][j].value, i,j))
						self.eliminate_row(self.board[i][j].value, i)
						self.eliminate_col(self.board[i][j].value, j)
						self.eliminate_cluster(self.board[i][j].value, i, j)
						#Need to get input if a new number was found. If so we need to rerun the eliminations




			


b = Board()

#main instructions loop
while True:
	
	raw_inst = input('Instruction: ')
	inst = raw_inst[:4]

	if inst == 'rend':
		b.render_board()
	if inst == 'sspa':
		row = input('Row: ')
		col = input('Column: ')
		b.render_possibility_space(row, col)
	if inst == 'read':
		b.read_file()
	if inst == 'exit' or inst == 'quit':
		break
	if inst == 'solv':
		b.solve()

	if inst == 'eval':
		b.evaluate_clusters()
	if inst == 'full':
		b.read_file()
		b.solve()
		b.evaluate_clusters()
	if inst == 'rspa':
		b.render_solution_space()
	





if __name__ == "__main__":
	a = SudukoBoard()
