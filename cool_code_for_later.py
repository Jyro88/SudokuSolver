import numpy as np
import matplotlib.pyplot as plt
import time
from concurrent.futures import ThreadPoolExecutor

# Helper functions and solver with minimum remaining values heuristic
def is_valid(board, row, col, num):
    if num in board[row, :] or num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True

def find_empty_with_min_options(board):
    min_options = 10
    min_cell = None
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                options = sum(is_valid(board, i, j, num) for num in range(1, 10))
                if 0 < options < min_options:
                    min_options = options
                    min_cell = (i, j)
    return min_cell

def solve_sudoku_visual(board, ax, delay=0.1):
    cell = find_empty_with_min_options(board)
    if not cell:
        return True  # Puzzle solved

    row, col = cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row, col] = num
            update_plot(board, ax, delay)
            if solve_sudoku_visual(board, ax, delay):
                return True
            board[row, col] = 0
            update_plot(board, ax, delay)

    return False

def update_plot(board, ax, delay):
    ax.clear()
    ax.matshow(np.ones_like(board) * -1, cmap='Pastel2', vmin=-1, vmax=9)
    for (i, j), val in np.ndenumerate(board):
        ax.text(j, i, str(val) if val != 0 else '', ha='center', va='center', fontsize=15)
    plt.pause(delay)

# Set up the Sudoku board and visualization
sudoku_puzzle = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

# Run the solver with visualization
fig, ax = plt.subplots()
plt.ion()
solve_sudoku_visual(sudoku_puzzle, ax, delay=0.05)
plt.ioff()
plt.show()
