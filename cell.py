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
