"""
Testing for Connect 4 ai
"""

import pytest
from ai import (calc_adjacent,
                calc_heuristic,
                find_moves,
                make_move)

from connect4_pygame import (COLUMN_COUNT,
                             ROW_COUNT,
                             EMPTY,
                             PLAYER,
                             AI)


def create_board(pieces = []):
    """
    Create empty connect four board

    Pieces: list with structure [[row, column, player]]
    """
    board = [[0 for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]
    for row,column,player in pieces:
        board[row][column] = player
    return board

def create_all_but_one_board(player = AI):
    """
    Create a board filled except for top left

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
    ([],[0,1,2,3,4,5,6])
]

@pytest.mark.parametrize("moves, result", find_moves_cases)
def test_find_moves(moves, result):
    board = create_board()
    for move in moves:
        board = make_move(board, move, AI)
    assert (find_moves(board, AI)) == result 


make_move_cases = [
    # board, move to make, result
    (create_all_but_one_board(), 0, create_full_board()),
    (create_board(), 0, create_board([0,0,AI]))
]

@pytest.mark.parametrize("board, move, result", make_move_cases)
def test_make_move(board, move, result):
    assert make_move(board, move, AI) == result

def test_make_move_full_board(board, move, result):
    with pytest.raises(ValueError):
        make_move(create_full_board(), 0)


