"""Unit Testing for Connect 4 ai
"""

import pytest
from ai import (calc_adjacent,
                calc_heuristic,
                find_moves,
                make_move,
                per_in_center)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 1
AI = 2

EMPTY = 0


def create_board(pieces = []):
    """ Create empty connect four board
    (0,0) is the top left corner
    
    Parameters:
        Pieces: list with structure [[row, column, player]]
    
    Returns:
        board (array): 2d array representing board state
    """

    board = [[0 for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)] #create empty board

    #fill in pieces
    for piece in pieces:
        board[piece[0]][piece[1]] = piece[2]
    return board

def create_all_but_one_board(player = AI):
    """ Create a board filled except for top left

    Player: int representing player
    """
    board = [[player for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]
    board[0][0] = 0
    return board

def create_full_board(player = AI):
    """
    Create a board filled except for top left

    Player: int representing player
    """
    return [[player for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]


find_moves_cases = [
    # moves to make, result
    ([0 for i in range(ROW_COUNT)], [1,2,3,4,5,6]),
    ([1 for i in range(ROW_COUNT)], [0,2,3,4,5,6]),
    ([],[i for i in range(COLUMN_COUNT)]),
    ([1 for i in range(ROW_COUNT)] + [0 for i in range(ROW_COUNT)], [2,3,4,5,6]),
]

@pytest.mark.parametrize("moves, result", find_moves_cases)
def test_find_moves(moves, result):
    board = create_board()
    for move in moves:
        board = make_move(board, move, AI)
    assert (find_moves(board)) == result 

def test_find_moves_full_board():
    board = create_full_board()
    assert (find_moves(board)) == [] 


make_move_cases = [
    # board, move to make, result
    (create_all_but_one_board(), 0, create_full_board()),
    (create_board(), 0, create_board([[ROW_COUNT-1,0,AI]])),
    (create_board(), COLUMN_COUNT-1, create_board([[ROW_COUNT-1,COLUMN_COUNT-1,AI]])),
    (create_board([[ROW_COUNT-1,0,AI]]), 0, create_board([[ROW_COUNT-1,0,AI],[ROW_COUNT-2,0,AI]])),
    (create_board([[ROW_COUNT-1,0,AI],[ROW_COUNT-2,0,AI]]), 0, create_board([[ROW_COUNT-1,0,AI],[ROW_COUNT-2,0,AI],[ROW_COUNT-3,0,AI]]))

]

@pytest.mark.parametrize("board, move, result", make_move_cases)
def test_make_move(board, move, result):
    assert make_move(board, move, AI) == result

def test_make_move_full_board():
    with pytest.raises(ValueError):
        make_move(create_full_board(), 0, AI)


calc_adjacent_cases = [
    # board, move to make, result
    (create_board(), AI, 2, 0),
    (create_board(), AI, 3, 0),
    (create_board(), AI, 4, 0),
    (create_board([[0,0,AI],[0,1,AI]]), AI, 2, 1),
    (create_board([[0,0,AI],[0,1,AI]]), AI, 3, 0),
    (create_board([[0,0,AI],[0,1,AI],[0,2,AI],[0,3,AI]]), AI, 2, 3),
    (create_board([[0,0,AI],[0,1,AI],[0,2,AI],[0,3,AI]]), AI, 3, 2),
    (create_board([[0,0,AI],[0,1,AI],[0,2,AI],[0,3,AI]]), AI, 4, 1),
    (create_board([[0,0,AI],[0,1,PLAYER],[0,2,AI],[0,3,AI]]), AI, 2, 1),
    (create_board([[0,0,AI],[0,1,PLAYER],[0,2,AI],[0,3,AI]]), AI, 3, 0),
    (create_board([[0,0,AI],[0,1,PLAYER],[0,2,AI],[0,3,AI]]), AI, 4, 0),

]

@pytest.mark.parametrize("board, player, number, result", calc_adjacent_cases)
def test_calc_adjacent(board, player, number, result):
    assert calc_adjacent(board,player,number) == result


per_in_center_cases = [
    (create_board([[ROW_COUNT-1,COLUMN_COUNT-3,AI]]), 1/9),
    (create_board([[ROW_COUNT-3,2,AI],[ROW_COUNT-1,2,AI]]), 2/9),
    (create_board([[ROW_COUNT-3,2,PLAYER],[ROW_COUNT-1,2,PLAYER]]), 0),
    (create_board([[ROW_COUNT-3,2,AI],[ROW_COUNT-1,2,AI],[ROW_COUNT-4,1,AI]]), 2/9),    
    (create_board(),0),
    (create_full_board(), 1)
]
@pytest.mark.parametrize("board, result", per_in_center_cases)
def test_per_in_center(board, result):
    assert per_in_center(board) == result

