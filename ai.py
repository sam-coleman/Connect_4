""" Hold driver functions for minimax ai
"""

import numpy as np
import pygame
import sys
import math
import copy

from connect4_pygame import (
    ROW_COUNT,
    COLUMN_COUNT,
    AI,
    PLAYER,
    EMPTY
)

def minimax(board, player, depth, alpha, beta):#, prev_move):
    """player = 0: AI (maximizer)
        player = 1: opponent (minimzer)
        prev_move: int representing last column played in
    """
    #what is move? how calculate? column?
    #TODO no possible moves? what return?

    #check if someone has won
    if calc_adjacent(board, PLAYER, 4) > 0:
        #SUPER BAD--Lose
        return -math.inf, -1
    if calc_adjacent(board, AI, 4) > 0:
        #SUPER GOOD--Win
        return math.inf, -1

    if depth == 0: #reached max recursion
        return calc_heuristic(board), -1

    elif player == AI: #AI playing, maximizer
        poss_moves = find_moves(board,AI)
        results = []  
        #max_val = -math.inf      
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            result = ((minimax(copy.deepcopy(new_board), PLAYER, depth-1, alpha, beta)[0], move))
            # max_val = max(max_val, result[0])
            # alpha = max(alpha, result[0])
            # if depth < 3:
            #     if beta <= alpha:
            #         print("PRUNING")
            #         break
            #     else:
            #         print("NOT PRUNING")
            #print(f"result 0 is: {result[0]}")
            # val = max(max_val, result[0])
            # if val != result[0]:
            #     print("CRISIS")
            # alpha = max(val, alpha)
            # # if alpha >= beta:
            #     # print('alpha beta thing', alpha, beta, result)
            #     # break
            results.append(result)
        try: 
            # print(results)
            # if depth == 4:
                # print(results, max(results))
            return max(results)
        except:
            return 0,move
       
    else: #human playing, minimzer
        poss_moves = find_moves(board,PLAYER)
        results = []
        #min_val = math.inf
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            result = ((minimax(copy.deepcopy(new_board), AI, depth-1, alpha, beta)[0], move))
            #min_eval = min(min_val, result[0])
            # beta = min(beta, result[0])
            # if depth < 3:
            #     if beta <= alpha:
            #         print("PRUNING")
            #         break
            #     else:
            #         print("NOT PRUNING")
            # print(f"result 0 is: {result[0]}")
            # val = min(min_val,result[0])
            # if val != result[0]:
            #     print("CRISIS")
            # beta = min(val, beta)
            # # if beta <= alpha:
            #     # print('ab thing in minim', alpha, beta)
            #     # break 
            results.append(result)
        try:
            return min(results)
        except:
            return 0,move

def calc_heuristic(board):
    """Our heuristic function. Returns the sum of all weights attached to
    streaks (an integer).

    We are prioritizing not having the player win the most. After that, we prioritize
    the AI winning and an equal weight for the rest of the streaks.
    """
    # AI = 0, calculating the streaks the AI has
    our_fours = calc_adjacent(board, AI, 4)
    our_threes = calc_adjacent(board, AI, 3)
    our_twos = calc_adjacent(board, AI, 2)

    # player = 1, calculating the streaks that the player has
    enemy_fours = calc_adjacent(board, PLAYER, 4)
    enemy_threes = calc_adjacent(board, PLAYER, 3)
    enemy_twos = calc_adjacent(board, PLAYER, 2)

    #num_in_center = 

    if enemy_fours >= 1:
    	# avoid at ALL COST
    	rating = -math.inf
    else:
    	# For now, we are not going to prevent double-counting (might change later)
    	rating = (our_fours*(1000000) + our_threes*(1000) + our_twos*(10) + enemy_threes*(-1000) + enemy_twos*(-10))
    return rating

def calc_adjacent(board, player, num):
    """num: how many we care about in a "row"
    need to deal with 2 in a row occurs in a 4 in a row, don't count sub-in-a-rows

    #return: # instances with num in a row for player
    """
    total = 0

    #want to find 4 in a rows
    if num == 4:
	# Check horizontal locations
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                    total += 1

        # Check vertical locations
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                    total += 1

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                    total += 1

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                    total += 1

    elif num == 3:
        	# Check horizontal locations
        for c in range(COLUMN_COUNT-2):
            for r in range(ROW_COUNT):
                if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player:
                    total += 1

        # Check vertical locations
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-2):
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player:
                    total += 1

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-2):
            for r in range(ROW_COUNT-2):
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player:
                    total += 1

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-2):
            for r in range(2, ROW_COUNT):
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player:
                    total += 1

    else: #num == 2

        # Check horizontal locations
        for c in range(COLUMN_COUNT-1):
            for r in range(ROW_COUNT):
                if board[r][c] == player and board[r][c+1] == player:
                    total += 1

        # Check vertical locations
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-1):
                if board[r][c] == player and board[r+1][c] == player:
                    total += 1

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-1):
            for r in range(ROW_COUNT-1):
                if board[r][c] == player and board[r+1][c+1] == player:
                    total += 1

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-1):
            for r in range(1, ROW_COUNT):
                if board[r][c] == player and board[r-1][c+1] == player:
                    total += 1

    return total

def find_moves(board, player):
    """returns list w/ columns representing possible moves
    """
    # We will check if the column is filled (e.g. you can't add any more pieces to
    # that column)
    valid_moves = []

    for i in range(0, len(board[0])): # Looking at the first row
    	if board[0][i] == 0: #(np.flip(board, 0)
    		# we want to add 1 to indicate there's 1 less spot in this column
    		valid_moves.append(i)

    return valid_moves

def make_move(board, move, player):
    """make a move on board
    move: column
    player: human(1) or ai (2)
    return: board w/ move made
    """

    global ROW_COUNT

    valid_moves = find_moves(board, player)
    stuff_in_col = 0

    if move not in valid_moves:
        raise ValueError('Move %s is not valid. Valid moves: %s' % (move, valid_moves))

    for rows in board:
    	if rows[move] > 0:
    	      # we want to add 1 to indicate there's 1 less spot in this column
    	      stuff_in_col += 1

    # We subtract by 6 because we are starting from the bottom and going up
    index_for_col = ROW_COUNT - stuff_in_col - 1
    index_for_row = move

    board[index_for_col][index_for_row] = player

    return board
