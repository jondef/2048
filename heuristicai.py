from heapq import merge
import random
import game
import sys
import numpy as np
from searchai import board_weights

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def heuristicai_move(board, searches_per_move, search_length):
    first_moves = [UP, DOWN, LEFT, RIGHT]
    score = np.zeros(4)

    for first_index in range(4):
        first_move = first_moves[first_index]
        first_board, first_valid, first_score = first_move(board)

        if first_valid:
            first_board = merge(first_board)
            score[first_index] += first_score
        else:
            continue

        for later_moves in range(searches_per_move):
            move_number = 1
            search_board = np.copy(first_board)
            is_valid = True

            while is_valid and move_number < search_length:
                search_board, is_valid, score = random.choice(search_board)
                if is_valid:
                    search_board = merge(search_board)
                    score[first_index] += score
                    move_number += 1

    best_move_index = np.argmax(score)
    best_move = first_moves[best_move_index]
    final_board, position_valid, _ = best_move(board)
    return final_board, position_valid


def get_score_of_board_empty_tiles(board):
    """
    Calculates the score of a board based on the amount of empty tiles
    :param board: the board to calculate the score of
    :return: the score of the board
    """
    return np.count_nonzero(board == 0)

def get_score_of_board_sum_of_tiles(board):
    """
    Calculates the score of a board based on the sum of all tiles
    :param board: the board to calculate the score of
    :return: the score of the board
    """
    return np.sum(board * board_weights)

def find_best_move(board):
    bestmove = -1
    bestscore = -1

    # try every possible move, calculate the score for each move and return the move with the highest score
    for move in [UP, DOWN, LEFT, RIGHT]:
        newboard = execute_move(move, board)

        if board_equals(board, newboard):
            continue  # invalid move

        # calculate score for board
        score = get_score_of_board_sum_of_tiles(newboard) + 0.1 * get_score_of_board_empty_tiles(newboard)

        if bestmove == -1 or score > bestscore:
            bestmove = move
            bestscore = score

    return bestmove


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
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
    return (newboard == board).all()
