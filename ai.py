""" Hold driver functions for minimax ai

"""

import numpy as np
import pygame
import sys
import math
import copy
"""# pseudocode without alpha beta pruning
def minimax(boardType board, bool maximizer, int depth)
	# might make sense to check if someone has won first
	if depth == 0: #reached max recursion depth
		return heuristic(board), move 
	elif maximizer == True:# we want to maximize the score
		moves = find_moves(board) # max is 7
		new_boards = []
		for move in moves:
			# make deep copy of board w/ move played
			new_board = deep_copy(board.make_move(move))
			new_boards.append(new_board)
		# find max!
		return max(minimax(new_board, false, depth -1) for new_board in new_boards)
	else: #minimizer, aka we want to minimize the score
		moves = find_moves(board)
		new_boards = []
		for move in moves:
			# make deep copy of board w/ move played
			new_board = deep_copy(board.make_move(move))
			new_boards.append(new_board)
		# find min!
		return min(minimax(new_board, true, depth -1) for new_board in new_boards)

"""

def minimax(board, player, depth):#, prev_move):
    """player = 0: AI (maximizer)
        player = 1: oponenet (minimzer)
        prev_move: int representing last column played in
    """
    #what is move? how calculate? column?
    #TODO no possible moves? what return?

    #check if someone has won
    if calc_adjacent(board, 1, 4) > 0:
        #SUPER BAD--Lose 
        return -math.inf, -1
    if calc_adjacent(board, 0, 4) > 0:
        #SUPER GOOD--Win
        return math.inf, -1

    if depth == 0: #reached max recursion
        return heuristic(board), -1
    
    elif player == 0: #AI playing, maximizer
        poss_moves = find_moves(boards)
        #DO SOMETIHING IF POSS MOVES EMPTY
        results = []
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            results.append((minimax(copy.deepcopy(new_board), 1, depth-1)[0], move))
        
        return max(results)
    
    else: #human playing, minimzer
        poss_moves = find_moves(boards)
        #DO SOMETIHING IF POSS MOVES EMPTY
        results = []
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            results.append((minimax(copy.deepcopy(new_board), 0, depth-1)[0], move))
        
        return min(results)
        
def calc_heuristic(board):
    """will prob call calc_adjacent # in a row

    """
    return 0

def calc_adjacent(board, player, num):
    """num: how many we care about in a "row"
    need to deal with 2 in a row occurs in a 4 in a row, don't count sub-in-a-rows

    #return: # instances with num in a row for player
    """
    return 0

def find_moves(board):
    """returns list w/ columbs representing possible moves

    """
    return []

def make_move(board, move, player):
    """make a move on board 
    move: column
    player: human(1) or ai (0)
    return: board w/ move made
    """
    return board