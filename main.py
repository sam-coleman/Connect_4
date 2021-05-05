"""Credit for base Connect 4 implementation: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
"""

import numpy as np
import pygame
import sys
import math
import random
import timeit
import ai
import matplotlib.pyplot as plt

#define constants
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 1
AI = 2

EMPTY = 0

timing_results = []
move_number = 0

def create_board():
	board = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def test_plots(runtime_to_plot):
	# Data for plotting
	fig, ax = plt.subplots()
	moves_to_plot = []

	for i in range(0, len(timing_results)):
		moves_to_plot.append(i+1)
	# moves_to_plot = []
	# for i in range(0, len(timing_results)-1):
	# 	moves_to_plot.append(timing_results[i][0])
	#
	# runtime_to_plot = []
	# for i in range(0, len(timing_results)-1):
	# 	runtime_to_plot.append(timing_results[i][1])

	ax.plot(moves_to_plot, runtime_to_plot, label="")
	ax.scatter(moves_to_plot, runtime_to_plot, s=80, marker=">")

	ax.set(xlabel='Move Number', ylabel='Runtime (s)', title='Runtime of MiniMax Over Time')
	ax.grid()

	fig.savefig("connect4cks_runtime_plot.png")
	plt.show()
	plt.legend()



if __name__ == "__main__":
	board = create_board()
	game_over = False
	turn = PLAYER

	pygame.init()

	SQUARESIZE = 100

	width = COLUMN_COUNT * SQUARESIZE
	height = (ROW_COUNT+1) * SQUARESIZE

	size = (width, height)

	RADIUS = int(SQUARESIZE/2 - 5)

	screen = pygame.display.set_mode(size)
	draw_board(board)
	pygame.display.update()

	myfont = pygame.font.SysFont("monospace", 75)

	while True:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		if not game_over:

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				posx = event.pos[0]
				if turn == PLAYER:
					pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

			pygame.display.update()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

				# Ask human for input
				if turn == PLAYER:

					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))

					if is_valid_location(board, col):
						row = get_next_open_row(board, col)
						drop_piece(board, row, col, PLAYER)

						if winning_move(board, PLAYER):
							label = myfont.render("Human Wins!!", 1, RED)
							screen.blit(label, (40,10))
							game_over = True
							outputfile=open('connect4cks_output.txt','w')
							i = 0
							for item in timing_results:
								outputfile.writelines('(' + str(i) + ',' + str(item) + ')')
							outputfile.close()
							test_plots(timing_results)

						elif 0 not in board[ROW_COUNT-1]:
							label = myfont.render("It's a tie!", 1, ORANGE)
							screen.blit(label, (40,10))
							game_over = True
							outputfile=open('connect4cks_output.txt','w')
							i = 0
							for item in timing_results:
								outputfile.writelines('(' + str(i) + ',' + str(item) + ')')
							outputfile.close()
							test_plots(timing_results)

						turn = AI
						draw_board(board)


			# Ask AI for input
			if turn == AI and not game_over:
				#determine column to play in (using minimax algorithm)
				# TIMING!

				start = timeit.default_timer()
				heur, col = ai.minimax(np.flip(board, 0), AI, 4, -math.inf, math.inf) #move is the column
				stop = timeit.default_timer()
				move_number += 1
				timing_results.append(stop - start)
				print('-------Runtime: %s----------\n' % (stop - start))
				# end timing

				if is_valid_location(board, col):
					pygame.time.wait(500)
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, AI)

				if winning_move(board, AI):
					label = myfont.render("AI wins!!", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True
					outputfile=open('connect4cks_output.txt','w')
					i = 0
					for item in timing_results:
						i += 1
						outputfile.writelines('(' + str(i) + ',' + str(item) + ')')
					outputfile.close()
					test_plots(timing_results)

				elif 0 not in board[ROW_COUNT-1]:
						label = myfont.render("It's a tie!", 1, ORANGE)
						screen.blit(label, (40,10))
						game_over = True
						outputfile=open('connect4cks_output.txt','w')
						i = 0
						for item in timing_results:
							outputfile.writelines('(' + str(i) + ',' + str(item) + ')')
						outputfile.close()
						test_plots(timing_results)

				draw_board(board)
				turn = PLAYER
