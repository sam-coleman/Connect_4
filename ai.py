""" Hold driver functions for MiniMax AI
TODO: Update header comment
"""

import pygame
import sys
import math
import copy
import random

#import constants
from main import (
    ROW_COUNT,
    COLUMN_COUNT,
    AI,
    PLAYER,
    EMPTY
)

def minimax(board, player, depth, alpha, beta):
    """ Driver function for MiniMax algorithm

    Parameters:
        - board (array): 2d array representing board state
        - player (int): constant representing current player (PLAYER or AI)
        - depth (int): current depth, 0 represents max depth reached
        - alpha (float): best value maximizer player can gaurantee at current depth or above
        - beta (float): best value minimizer player can gaurantee at current depth or above
    
    Returns:
        - heuristic (float), move (int): Column representing best move to play and corresponding heuristic
    """
    #check if either player has won
    if calc_adjacent(board, AI, 4) > 0:
        #SUPER GOOD--Win
        return 1000000000 * (depth+1), -1
    if calc_adjacent(board, PLAYER, 4) > 0:
        #SUPER BAD--Lose
        return -100000000000 * (depth+1), -1

    poss_moves = find_moves(board) #find possible moves
    if depth == 0 or len(poss_moves) == 0: #reached max recursion or out of spaces
        return calc_heuristic(board), -1

    elif player == AI: #AI playing, maximizer
        results = []  
        #play through all possible next moves
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            #find heuristic of that move tree
            result = ((minimax(copy.deepcopy(new_board), PLAYER, depth-1, alpha, beta)[0], move)) #call recursively with move played
            results.append(result)
            #alpha beta pruning
            alpha = max(max(results)[0], alpha)
            if alpha > beta:
                break

        try: #play best move for maximizer
            max_heur = max([heur[0] for heur in results])
            max_results = [key for key in results if key[0] == max_heur]
            return random.choice(max_results)
        except:
            return 0,move

    else: #human playing, minimzer
        results = []
        #play through all possible next moves for player
        for move in poss_moves:
            new_board = copy.deepcopy(board)
            new_board = make_move(new_board, move, player)
            #find heuristic of that move tree
            result = ((minimax(copy.deepcopy(new_board), AI, depth-1, alpha, beta)[0], move))  #call recursively with move played
            results.append(result)
            beta = min(min(results)[0], beta)
            #alpha beta pruning
            if alpha > beta:
                break 
        try: #play best move for minimizer
            min_heur = min([heur[0] for heur in results])
            min_results = [key for key in results if key[0] == min_heur]
            return random.choice(min_results)
        except:
            return 0,move

def calc_heuristic(board):
    """ Calculate heuristic for a given board

    Paramters:
        - board (array): 2d array representing board state
    
    Returns:
        - rating (float): Heuristic value
    """
    #AI values
    our_threes = calc_adjacent(board, AI, 3)
    our_twos = calc_adjacent(board, AI, 2)
    our_middle_perc = per_in_center(board)
    
    #player values
    enemy_threes = calc_adjacent(board, PLAYER, 3)
    enemy_twos = calc_adjacent(board, PLAYER, 2)


    #Calculate heuristic, ignore double counting
    rating = (our_middle_perc * 1050 + our_threes*(1000) + our_twos*(20) + enemy_threes*(-1100) + enemy_twos*(-10))
    return rating

def per_in_center(board):
    """ Calculate percent in center 9 spots AI has (middle 3 columns from the bottom to third from bottom row)
    since these spots are more valuable

    Paramters:
        - board (array): 2d array representing board state
    
    Returns:
        - percent (float): Proportion of center spots occupied by AI
    """
    num_tokens = 0
    for c in range(2,COLUMN_COUNT-2):
        for r in range(ROW_COUNT-3, ROW_COUNT):
            if board[r][c] == AI:
                num_tokens += 1
    
    return num_tokens / 9


def calc_adjacent(board, player, num):
    """ Calculate number of adjacent tokens of a given length
    
    Parameters:
        - board (array): 2d array representing board state
        - player (int): constant representing current player (PLAYER or AI)
        - num (int: 2, 3, or 4): how many we care about in a "row"

    Returns:
        - Number of adjacent streaks of given length; ignoring double counting
    """
    total = 0

   
    if num == 4: #find 4 in a rows
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

    elif num == 3: #find 3 in a rows
        #full 3 in a rows without any breaks
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
        
        #3 in a rows with an empty spot in the middle
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

    else: #find 2 in a rows
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
    """Find all posisble next moves for a given board

    Parameter:
        -board (array): 2d array representing board state
    
    Returns:
        - (list of ints): columns representing possible moves
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
    """Make a move on board

    Parameters:
        - board (array): 2d array representing board state
        - move (int): move to make, indicated by column
        - player (int): constant representing current player (PLAYER or AI)
    
    Return:
        - board (array): board with move made
    """
    #ensure move is valid
    valid_moves = find_moves(board)
    if move not in valid_moves:
        raise ValueError('Move %s is not valid. Valid moves: %s' % (move, valid_moves))
    
    #determine row to place token
    stuff_in_col = 0
    for rows in board:
    	if rows[move] > 0:
    	      # we want to add 1 to indicate there's 1 less spot in this column
    	      stuff_in_col += 1

    # We subtract by 6 because we are starting from the bottom and going up
    index_for_col = ROW_COUNT - stuff_in_col - 1
    index_for_row = move

    #make move
    board[index_for_col][index_for_row] = player

    return board