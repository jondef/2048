import random
import sys

import numpy as np

import game

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

board_weights = np.array([[10, 8, 7, 6.5],
                          [.5, .7, 1, 3],
                          [-.5, -1.5, -1.8, -2],
                          [-3.8, -3.7, -3.5, -3]])


class Node:
    def __init__(self, board, parent=None, depth=2):
        self.parent = parent
        self.board = board

        self.tile_value_score = get_tile_value_score(board)
        self.empty_tile_score = get_empty_tiles_score(board)
        self.score = self.get_score()

        if depth != 0:  # only create children if we still have depth left
            self.left = Node(execute_move(LEFT, board), self, depth=depth - 1)
            self.right = Node(execute_move(RIGHT, board), self, depth=depth - 1)
            self.up = Node(execute_move(UP, board), self, depth=depth - 1)
            self.down = Node(execute_move(DOWN, board), self, depth=depth - 1)
            self.children = [self.left, self.right, self.up, self.down]
        else:
            self.left = None
            self.right = None
            self.up = None
            self.down = None
            self.children = []

    def get_score(self):
        score = 0
        current_node = self

        # go as close to the root node as possible
        while current_node.parent is not None:
            score += np.dot(([1, 100], stats(self.board)))
            current_node = current_node.parent

        return score

    def get_move(self):
        """
        Returns the move that was made to get to this node.
        :return: the move that was made to get to this node
        """
        current_node = self
        prev_node = None

        # go as close to the root node as possible
        while current_node.parent is not None:
            prev_node = current_node
            current_node = current_node.parent

        if current_node.left == prev_node:
            return LEFT
        elif current_node.right == prev_node:
            return RIGHT
        elif current_node.up == prev_node:
            return UP
        elif current_node.down == prev_node:
            return DOWN
        else:
            return -1

    def add_two_or_four(self, board):
        """
        Add a 2 or 4 to a random empty cell.
        """
        empty_cells = np.argwhere(board == 0)
        # if the board is full, break and penalize the score
        if len(empty_cells) == 0:
            self.score *= 0.5
            return board
        random_cell = random.choice(empty_cells)
        board[random_cell[0]][random_cell[1]] = np.random.choice([2, 4], 1, p=[0.9, 0.1])
        return board

    def getBestMove(self):
        """
        Navigates the tree and finds out which move is the best
        based on the score of the leafs.
        :return: the best move to make
        """
        # if node is not a parent node, break
        if self.parent is not None:
            return None

        # traverse the tree and add all leafs to a list
        leafs = self.get_leaf_nodes()
        best_leaf = leafs[0]

        # take the leaf with the highest score
        for leaf in leafs:
            if leaf.score > best_leaf.score:
                best_leaf = leaf

        # find the move that was made to get to the best leaf
        return best_leaf.get_move()

    def get_leaf_nodes(self):
        leafs = []
        def _get_leaf_nodes(node):
            if node is not None:
                if len(node.children) == 0:
                    leafs.append(node)
                for n in node.children:
                    _get_leaf_nodes(n)
        _get_leaf_nodes(self)
        return leafs

def find_best_move(board):
    """
    Comparison function based on number of empty tiles!
    Two look aheads and find where empty tiles the highest
    Forbidden direction only when absolutley needed!

    Additional idea -> when certain number of tiles already free, merge to maximize value!
    If board is half empty, no point in having more space -> focus on merging tiles

    :param board:
    :return: best move to make
    """
    root = Node(board, depth=2)  # build the tree with the possible moves
    return root.getBestMove()


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


def stats(board):
    free = get_empty_tiles_score(board)
    weighted_board_sum = np.sum(board * board_weights)
    return [weighted_board_sum, free**2]


def amount_of_empty_tiles(board):
    """
    Count the amount of empty tiles on the board.
    """
    return np.count_nonzero(board == 0)


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


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