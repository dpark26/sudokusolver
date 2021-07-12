import pygame
import time
pygame.font.init()

class Board:
	board = [
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0]
	]

	def __init__(self, length, height):
		self.length = length
		self.height = height
		self.marked = None
		self.boxes = []
		for i in range(9):
			temp = []
			for j in range(9):
				temp.append(Box(i, j, length, height, self.board[i][j]))
			self.boxes.append(temp)

	def insert(self, value):
		row, col = self.marked
		self.boxes[row][col].set_value(value)
		self.board[row][col] = value
		self.marked = None

	def draw(self, window):
		space = self.length / 9
		for i in range(10):
			if i % 3 == 0 and i != 0:
				pygame.draw.line(window, (212, 232, 255), (0, i * space), (self.length, i * space), 5)
				pygame.draw.line(window, (212, 232, 255), (i * space, 0), (i * space, self.height), 5)
			else:
				pygame.draw.line(window, (212, 232, 255), (0, i * space), (self.length, i * space), 2)
				pygame.draw.line(window, (212, 232, 255), (i * space, 0), (i * space, self.height), 2)

		for i in range(9):
			for j in range(9):
				self.boxes[i][j].draw(window)

	def mark(self, row, col):
		for i in range(9):
			for j in range(9):
				self.boxes[i][j].marked = False
		self.boxes[row][col].marked = True
		self.marked = row,col

	def click(self, position):
		if position[0] < self.length and position[1] < self.height:
			space = self.length / 9
			x = int(position[0]/space)
			y = int(position[1]/space)
			return int(y), int(x)

	def unmark(self, row, col):
		self.marked = None
		self.boxes[row][col].marked = False

	def solve(self):
		empty = next_empty(self.board)
		if empty == None: return True

		(row,col) = empty
		for i in range(1, 10):
			if is_valid(self.board, (row,col), i):
				self.board[row][col] = i
				if run(self.board): return True
				self.board[row][col] = 0

		return False


class Box:
	def __init__(self, row, col, length, height, value):
		self.row = row
		self.col = col
		self.length = length
		self.height = height
		self.value = value
		self.marked = False

	def draw(self, window):
		font = pygame.font.SysFont("corbel", 30, bold=True, italic=True)
		space = self.length/9
		x = self.col * space
		y = self.row * space

		if self.value == 0:
			text = font.render("", 24, (230, 151, 55))
			xPos = x + space/2 - text.get_width()/2
			yPos = y + space/2 - text.get_height()/2
			window.blit(text, (xPos, yPos))
		else:
			text = font.render(str(self.value), 24, (230, 151, 55))
			xPos = x + space/2 - text.get_width()/2
			yPos = y + space/2 - text.get_height()/2
			window.blit(text, (xPos, yPos))

		if self.marked: pygame.draw.rect(window, (82, 7, 7), (x,y,space,space), 3)

	def set_value(self, value):
		self.value = value


def draw_window(window, board):
	window.fill((21, 39, 59))
	board.draw(window)


def restart(board):
	for i in range(9):
		for j in range(9):
			board.board[i][j] = 0


def main():

	# start menu
	start_screen = True
	window = pygame.display.set_mode((600, 500))
	pygame.display.set_caption("Sudoku Solver")
	window.fill((21, 39, 59))
	font = pygame.font.SysFont("corbel", 30, bold=True, italic=True)
	title_font = pygame.font.SysFont("corbel", 75, bold=True, italic=True)
	instruction_font = pygame.font.SysFont("corbel", 20)
	title_text = title_font.render("Sudoku Solver", 24, (230, 151, 55))
	instruction_text1 = instruction_font.render("Instructions: Once you click play, you will be taken to a 9x9 grid,", 24, (145, 145, 145))
	instruction_text2 = instruction_font.render("where you will click on a box to enter a number.", 24, (145, 145, 145))
	instruction_text3 = instruction_font.render("Once all the numbers have been inserted in the correct boxes,", 24, (145, 145, 145))
	instruction_text4 = instruction_font.render("you may press enter to instantly solve the sudoku!", 24, (145, 145, 145))
	instruction_text5 = instruction_font.render("An X will appear on the screen if the inputted board is invalid.", 24, (145, 145, 145))
	start_text = font.render("START", 24, (0, 0, 0))
	window.fill((94, 94, 94), (225, 375, 140, 75))
	pygame.draw.rect(window, (0, 0, 0), (225, 375, 140, 75), 3)
	window.blit(title_text, (70, 100))
	window.blit(instruction_text1, (50, 200))
	window.blit(instruction_text2, (105, 225))
	window.blit(instruction_text3, (53, 250))
	window.blit(instruction_text4, (95, 275))
	window.blit(instruction_text5, (55, 300))
	window.blit(start_text, (250, 400))
	while(start_screen):
		for i in pygame.event.get():
			if i.type == pygame.QUIT:
				start_screen = False
			if i.type == pygame.MOUSEBUTTONDOWN:
				position = pygame.mouse.get_pos()
				if position[0] > 226 and position[0] < 363 and position[1] > 376 and position[1] < 448:
					start_screen = False
		pygame.display.update()

	window = pygame.display.set_mode((500, 500))
	board = Board(500, 500)
	value = None
	run = True
	while(run):
		for i in pygame.event.get():
			if i.type == pygame.QUIT: run = False
			if i.type == pygame.KEYDOWN:
				if i.key == pygame.K_1: value = 1
				if i.key == pygame.K_2: value = 2
				if i.key == pygame.K_3: value = 3
				if i.key == pygame.K_4: value = 4 
				if i.key == pygame.K_5: value = 5
				if i.key == pygame.K_6: value = 6
				if i.key == pygame.K_7: value = 7
				if i.key == pygame.K_8: value = 8
				if i.key == pygame.K_9: value = 9
				if i.key == pygame.K_0 or i.key == pygame.K_BACKSPACE: value = 0
				if i.key == pygame.K_RETURN:
					if is_valid_board(board.board) and board.solve():
						end_screen = True
						window = pygame.display.set_mode((500, 600))
						board = Board(500, 500)
						draw_window(window, board)
						window.fill((94, 94, 94), (0, 500, 500, 600))
						pygame.draw.line(window, (0, 0, 0), (250, 500), (250, 600), 5)
						font = pygame.font.SysFont("corbel", 30, bold=True, italic=True)
						start_text = font.render("START", 24, (0, 0, 0))
						exit_text = font.render("EXIT", 24, (0, 0, 0))
						window.blit(start_text, (75, 530))
						window.blit(exit_text, (350, 530))
						pygame.draw.rect(window, (0, 0, 0), (0, 500, 500, 100), 3)
						while(end_screen):
							for i in pygame.event.get():
								if i.type == pygame.QUIT:
									run = False
									end_screen = False
								if i.type == pygame.MOUSEBUTTONDOWN:
									position = pygame.mouse.get_pos()
									if position[0] > 1 and position[0] < 249 and position[1] > 501 and position[1] < 599:
										restart(board)
										main()
										end_screen = False
										run = False
									if position[0] > 251 and position[0] < 499 and position[1] > 501 and position[1] < 599:
										run = False
										end_screen = False
							pygame.display.update()
					else:
						timer = 0
						font = pygame.font.SysFont("corbel", 500)
						text = font.render('X', 1, (255, 0, 0))
						window.blit(text, (116, 45))
						while(True):
							pygame.display.update()
							time.sleep(1)
							timer += 1
							if timer > 1:
								break

			if i.type == pygame.MOUSEBUTTONDOWN:
				position = pygame.mouse.get_pos()
				clicked = board.click(position)
				if clicked:
					board.mark(clicked[0], clicked[1])
					value = None
		if board.marked and value != None:
			board.insert(value)
			board.unmark(clicked[0], clicked[1])

		draw_window(window, board)
		pygame.display.update()


def is_valid_board(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] != 0:
				num = board[i][j]

				for k in range(j, len(board[i])):
					if j != k and board[i][k] == num: return False

				for k in range(i, len(board)):
					if i != k and board[k][j] == num: return False

				if i < 3 and j < 3: # first box
					for k in range(3):
						for l in range(3):
							if i != k and l != j and board[k][l] == num: return False
				elif i < 3 and j < 6: # second box
					for k in range(3):
						for l in range(3, 6):
							if i != k and l != j and board[k][l] == num: return False
				elif i < 3 and j < 9: # third box
					for k in range(3):
						for l in range(6, 9):
							if i != k and l != j and board[k][l] == num: return False
				elif i < 6 and j < 3:
					for k in range(3, 6):
						for l in range(3):
							if i != k and l != j and board[k][l] == num: return False
				elif i < 6 and j < 6:
					for k in range(3, 6):
						for l in range(3, 6):
							if i != k and l != j and board[k][l] == num: return False
				elif i < 6 and j < 9:
					for k in range(3, 6):
						for l in range(6, 9):
							if i != k and l != j and board[k][l] == num: return False
				elif i < 9 and j < 3:
					for k in range(6, 9):
						for l in range(3):
							if i != k and l != j and board[k][l] == num: return False
				elif i < 9 and j < 6:
					for k in range(6, 9):
						for l in range(3, 6):
							if i != k and l != j and board[k][l] == num: return False
				else:
					for k in range(6, 9):
						for l in range(6, 9):
							if i != k and l != j and board[k][l] == num: return False
	return True


def run(board):
	empty = next_empty(board)
	if empty == None: return True

	(row,col) = empty
	for i in range(1, 10):
		if is_valid(board, (row,col), i):
			board[row][col] = i
			if run(board): return True
			board[row][col] = 0

	return False


def is_valid(board, position, value):
	for i in range(9):
		if board[position[0]][i] == value and position[1] != i: return False

	for i in range(9):
		if board[i][position[1]] == value and position[0] != i: return False


	if position[0] < 3 and position[1] < 3: # first subbox
		for i in range(3):
			for j in range(3):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	elif position[0] < 3 and position[1] < 6: # second subbox
		for i in range(3):
			for j in range(3, 6):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	elif position[0] < 3 and position[1] < 9:
		for i in range(3):
			for j in range(6, 9):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	elif position[0] < 6 and position[1] < 3:
		for i in range(3, 6):
			for j in range(3):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	elif position[0] < 6 and position[1] < 6:
		for i in range(3, 6):
			for j in range(3, 6):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	elif position[0] < 6 and position[1] < 9:
		for i in range(3, 6):
			for j in range(6, 9):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	elif position[0] < 9 and position[1] < 3:
		for i in range(6, 9):
			for j in range(3):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	elif position[0] < 9 and position[1] < 6:
		for i in range(6, 9):
			for j in range(3, 6):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	else: 
		for i in range(6, 9):
			for j in range(6, 9):
				if position[0] != i and position[1] != j and board[i][j] == value: return False
	return True


def next_empty(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 0: return i,j


main()
pygame.quit()