import numpy as np
from boards import *


def build_candidates_board(main_board):
    """Function takes board to solve as input and returns board with candidates for each cell in form of a
    dictionary.
    Keys are coordinates, index of a cell. Tuples with two integers (y,x) ex.(2,4). y indicates row and x indicates
    column.
    Values are lists of integers that corresponding cell can take. By default this list is [1,2,3,4,5,6,7,8,9]"""
    indices = [index for index, x in np.ndenumerate(main_board)]
    candidates_all = list(np.arange(1, 10))
    candidates = {coord: candidates_all.copy() for coord in indices}
    return candidates


def set_boards_from_array(sudoku, candidates_board):
    """
    Function takes sudoku in form of a numpy 2d array and loops over all cells. If cell has a value then
    removes candidates from cells from row, column and block of that cell. Function returns main_board(sudoku) and
    modified candidates_board.
    """
    for index, val in np.ndenumerate(sudoku):
        if val != 0:
            candidates_board = eliminate_candidates(candidates_board, val, index)
        else:
            continue
    return sudoku, candidates_board


def create_slice(index):
    """Function takes cell coordinates (index) as argument (candidates_board key) and returns indexes of
    cells in row, column and block with that cell (except index of that cell)."""

    row, col, block = [], [], []
    for idx in range(9):
        if idx == index[1] and idx == index[0]:
            continue
        elif idx == index[1]:
            row.append((idx, index[1]))
        elif idx == index[0]:
            col.append((index[0], idx))
        else:
            row.append((idx, index[1]))
            col.append((index[0], idx))
    block_start = ((index[0]//3)*3, (index[1]//3)*3)
    for x in range(block_start[1], block_start[1] + 3):
        for y in range(block_start[0], block_start[0] + 3):
            if index == (y, x):
                continue
            else:
                block.append((y, x))
    return row, col, block


def eliminate_candidates(candidates_board, val, index):
    """Function takes candidates board, value of cell and coordinates of that cell. Then removes cell value from
    candidates from all cells from row, column and block of that cell. Fuction returns new candidates board."""
    row, col, block = create_slice(index)
    all_cells = list(set(row + col + block))
    candidates_board_new = candidates_board.copy()
    candidates_board_new[index] = [val]
    for cell in all_cells:
        if val in candidates_board_new[cell] and len(candidates_board_new[cell]) != 1:
            candidates_board_new[cell].remove(val)
    return candidates_board_new


def sole_candidate(main_board, candidates_board, index):
    """
    Function takes main_board, candidates_board and coordinates of cell. If cell has only one candidate then function
    write this value to main_board and eliminates candidates from other cells (row, column, block of that cell).
    Function returns new main_board and candidates_board.
    """

    main_board_new, candidates_board_new = main_board.copy(), candidates_board.copy()
    if len(candidates_board[index]) == 1:
        main_board_new[index[0]][index[1]] = candidates_board[index][0]
        candidates_board_new = eliminate_candidates(candidates_board, main_board_new[index[0]][index[1]], index)
    return main_board_new, candidates_board_new


def solve_loop(main_board, candidates_board):
    """
    Function takes main_board and candidates_board as arguments. Function iterates over all cells until all main
    boards cell have a value from 1 to 9. Function updates main_board and candidates_board. Function returns solved
    sudoku.
    """

    indices = [idx for idx, val in np.ndenumerate(main_board)]

    while (main_board == 0).sum() != 0:
        print((main_board == 0).sum())
        for index in indices:
            y, x = index[0], index[1]
            val = main_board[y][x]
            if val != 0:
                eliminate_candidates(candidates_board, val, index)
            else:
                main_board, candidates_board = sole_candidate(main_board, candidates_board, index)
    return main_board


if __name__ == '__main__':
    board = test_sudoku_easy
    candidates_board = build_candidates_board(board)
    boards = set_boards_from_array(board, candidates_board)
    sol = solve_loop(boards[0], boards[1])
    print(board)
    print('')
    print(sol)
