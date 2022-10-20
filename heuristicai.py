import random

import numpy as np

import game
import sys

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
FORBIDDEN_MOVE = random.choice([RIGHT])

class Node:
    def __init__(self, board, parent=None, depth=2):
        self.parent = parent
        self.board = board

        if depth != 0:  # only create children if we still have depth left
            self.left = Node(execute_move(LEFT, board), self, depth=depth - 1)
            self.right = Node(execute_move(RIGHT, board), self, depth=depth - 1)
            self.up = Node(execute_move(UP, board), self, depth=depth - 1)
            self.down = Node(execute_move(DOWN, board), self, depth=depth - 1)
        else:
            self.left = None
            self.right = None
            self.up = None
            self.down = None

        self.tile_value_score = get_tile_value_score(board)
        self.empty_tile_score = get_empty_tiles_score(board)

def find_best_move(board):
    """
#Comparison function based on number of empty tiles!
#Two look aheads and find where empty tiles highest
#Forbidden direction only when absolutley needed!

#Additional idea -> when certain number of tiles already free, merge to maximize value!
# if board is half empty, no point in having more space -> focus on merging tiles

    :param board:
    :return: best move to make
    """
    bestmove = -1    
    root = Node(board, depth=2)  # build the tree with the possible moves



    if bestmove == -1:
        bestmove = find_best_move_random_agent()
    return bestmove

def get_tile_value_score(board):
    """
    Return the score of the board based on the value of the tiles.
    """
    return np.sum(board ** 2)

def get_empty_tiles_score(board):
    """
    Return the score of the board based on the amount of empty tiles in percentage.
    """
    return np.count_nonzero(board == 0)

def bring_two_same_tiles_together(board):
    """
    Bring two tiles with the same value together.
    Return the move that brings the tiles together.
    """
    # check if there are two tiles with the same value on the board
    # if there are, bring them together
    # if there are no tiles with the same value, return -1

    # check if there are two tiles with the same value on the board
    # if there are, bring them together
    # if there are no tiles with the same value, return -1
    for i in range(3):
        for j in range(3):
            if i == 3 and j == 3:
                return -1
            if board[i][j] == board[i][j+1]:
                return RIGHT
            if board[i][j] == board[i+1][j]:
                return DOWN

    return -1

def merging_tiles_heuristic(board):
    """
    Makes a move based on if two tiles get merged.
    :return: The move with the highest score or -1 if no move merges tiles together
    """
    current_empty_tiles = amount_of_empty_tiles(board)

    if current_empty_tiles == 14: # if start of the game, just make a random move
        return find_best_move_random_agent()

    # if moving up increases the amount of empty tiles
    if amount_of_empty_tiles(execute_move(UP, board)) > current_empty_tiles:
        return UP
    # if moving left increases the amount of empty tiles
    if amount_of_empty_tiles(execute_move(LEFT, board)) > current_empty_tiles:
        return LEFT
    # if moving down increases the amount of empty tiles
    if amount_of_empty_tiles(execute_move(DOWN, board)) > current_empty_tiles:
        return DOWN

    # if moving right increases the amount of empty tiles
    # if amount_of_empty_tiles(execute_move(RIGHT, board)) > current_empty_tiles:
    #     return RIGHT

    return -1

def amount_of_empty_tiles(board):
    """
    Count the amount of empty tiles on the board.
    """
    return np.count_nonzero(board == 0)

def random_forbidden_move_agent():
    """
    Forbid a move in a random direction.
    """
    return random.choice([i for i in range(4) if i != FORBIDDEN_MOVE])

def find_best_move_random_agent():
    return random.choice([UP,DOWN,LEFT,RIGHT])


def execute_move(move, board):
    """
    move and return the grid without a new random tile 
    It won't affect the state of the game in the browser.
    :returns: board after move
    """
    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()