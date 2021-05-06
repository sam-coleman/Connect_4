""" Hold driver functions for minimax ai
"""

import numpy as np
import pygame
import sys
import math
import copy
import random

from main import (
    ROW_COUNT,
    COLUMN_COUNT,
    AI,
    PLAYER,
    EMPTY
)

def minimax(board, player, depth, alpha, beta):
    """player = 0: AI (maximizer)
        player = 1: opponent (minimzer)
        prev_move: int representing last column played in
    """

    if calc_adjacent(board, AI, 4) > 0:
        #SUPER GOOD--Win
        return 1000000000 * (depth+1), -1#math.inf, -1
    #check if someone has won
    if calc_adjacent(board, PLAYER, 4) > 0:
        #SUPER BAD--Lose
        return -100000000000 * (depth+1), -1 #-math.inf, -1

    poss_moves = find_moves(board)
    if depth == 0 or len(poss_moves) == 0: #reached max recursion
        return calc_heuristic(board), -1

    elif player == AI: #AI playing, maximizer
        results = []  
        #calculate next move
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            #find heuristic of that move tree
            result = ((minimax(copy.deepcopy(new_board), PLAYER, depth-1, alpha, beta)[0], move))
            results.append(result)
            #alpha beta pruning
            alpha = max(max(results)[0], alpha)
            if alpha > beta:
                break

        try: 
            max_heur = max([heur[0] for heur in results])
            max_results = [key for key in results if key[0] == max_heur]
            return random.choice(max_results)
        except:
            return 0,move

    else: #human playing, minimzer
        #poss_moves = find_moves(board)
        results = []
        #calculate next move
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            #find heuristic of that move tree
            result = ((minimax(copy.deepcopy(new_board), AI, depth-1, alpha, beta)[0], move))
            results.append(result)
            beta = min(min(results)[0], beta)
            #alpha beta pruning
            if alpha > beta:
                break 
        try:
            min_heur = min([heur[0] for heur in results])
            min_results = [key for key in results if key[0] == min_heur]
            return random.choice(min_results)
        except:
            return 0,move

def calc_heuristic(board):
    """Our heuristic function. Returns the sum of all weights attached to
    streaks (an integer).

    We are prioritizing not having the player win the most. After that, we prioritize
    the AI winning and an equal weight for the rest of the streaks.
    """
    # AI = 0, calculating the streaks the AI has
    #our_fours = calc_adjacent(board, AI, 4)
    our_threes = calc_adjacent(board, AI, 3)
    our_twos = calc_adjacent(board, AI, 2)
    our_middle_perc = per_in_center(board)
    # player = 1, calculating the streaks that the player has
    #enemy_fours = calc_adjacent(board, PLAYER, 4)
    enemy_threes = calc_adjacent(board, PLAYER, 3)
    enemy_twos = calc_adjacent(board, PLAYER, 2)


    # For now, we are not going to prevent double-counting (might change later)
    rating = (our_middle_perc * 1050 + our_threes*(1000) + our_twos*(20) + enemy_threes*(-1100) + enemy_twos*(-10)) #our_fours*(1000000) +
    return rating

def per_in_center(board):
    num_tokens = 0
    for c in range(2,COLUMN_COUNT-2):
        for r in range(ROW_COUNT-3, ROW_COUNT):
            if board[r][c] == AI:
                num_tokens += 1
    
    return num_tokens / 9


def calc_adjacent(board, player, num):
    """num: how many we care about in a "row"
    need to deal with 2 in a row occurs in a 4 in a row, don't count sub-in-a-rows
    #return: # instances with num in a row for player
    """
    total = 0
    if player == PLAYER:
        other_player = AI
    else:
        other_player = PLAYER
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
        #ACTUAL 3 IN A ROWS, W/ NO BREAKS
        # Check horizontal locations
        for c in range(COLUMN_COUNT-2):
            for r in range(ROW_COUNT):
                if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player: #and c+3 < COLUMN_COUNT - 1: #and board[r][c+2] < COLUMN_COUNT:
                    total += 1

        # Check vertical locations
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-2):
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player: #and r+3 < ROW_COUNT - 1:
                    total += 1

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-2):
            for r in range(ROW_COUNT-2):
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player: #and r+3 < ROW_COUNT - 1 and c+3 < COLUMN_COUNT - 1:
                    total += 1

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-2):
            for r in range(2, ROW_COUNT):
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player: #and c+3 < COLUMN_COUNT - 1:
                    total += 1
        
        #3 IN A ROWS W/ AN EMPTY SQUARE IN THE MIDDLE
        #checks horizaontal locations
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == player and board[r][c+1] == 0 and board[r][c+2] == player and board[r][c+3] == player:
                    total += 1
                elif board[r][c] == player and board[r][c+1] == player and board[r][c+2] == 0 and board[r][c+3] == player:
                    total += 1

        # Check vertical locations
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == player and board[r+1][c] == 0 and board[r+2][c] == player and board[r+3][c] == player:
                    total += 1
                elif board[r][c] == player and board[r+1][c] == player and board[r+2][c] == 0 and board[r+3][c] == player:
                    total += 1

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == player and board[r+1][c+1] == 0 and board[r+2][c+2] == player and board[r+3][c+3] == player:
                    total += 1
                elif board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == 0 and board[r+3][c+3] == player:
                    total += 1

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == player and board[r-1][c+1] == 0 and board[r-2][c+2] == player and board[r-3][c+3] == player:
                    total += 1
                elif board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == 0 and board[r-3][c+3] == player:
                    total += 1

    else: #num == 2
        # ACTUAL 2 IN A ROWS, W/ NO BREAKS
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

def find_moves(board):
    """returns list w/ columns representing possible moves
    """
    # We will check if the column is filled (e.g. you can't add any more pieces to
    # that column)
    valid_moves = []

    for i in range(0, len(board[0])): # Looking at the first row
    	if board[0][i] == 0: 
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

    valid_moves = find_moves(board)
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