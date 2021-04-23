import numpy as np
ROW_COUNT = 6
COLUMN_COUNT = 7
def calc_adjacent(board, player, num):
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

board = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 2, 2, 1, 1, 1, 1]]

print(np.flip(board, 0))
calc_adjacent(board, 1, 3)