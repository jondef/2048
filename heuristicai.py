from heapq import merge
import random
import game
import sys
import numpy as np

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


def find_best_move(board):
    bestmove = -1

    # TODO:
    # Build a heuristic agent on your own that is much better than the random agent.
    # Your own agent don't have to beat the game.
    # bestmove = find_best_move_random_agent()
    bestmove = heuristicai_move(board, [1,4], 4)

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
