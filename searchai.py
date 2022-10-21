import sys

import numpy as np

import game

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

board_weights = np.array([[10, 8, 7, 6.5],
                          [.5, .7, 1, 3],
                          [-.5, -1.5, -1.8, -2],
                          [-3.8, -3.7, -3.5, -3]])

FREE_CELL_BIAS = 1.0


class Node:
    def __init__(self, board, parent=None, moveNode=None, moveToNode=None, depth=2):
        """
        :param board: the board of the game
        :param parent: parent node
        :param moveNode: a move node is a node that was created after a move was made,
        unlike nodes that are created by randomly placing a 2 or 4 on the board
        :param moveToNode: the move that was used to get to that node
        :param depth: remaining depth to build the tree
        """
        self.parent = parent
        self.board = board
        self.depth = depth
        self.moveToNode = moveToNode
        self.score = 0

        # only create main nodes if node is not a move node, or node is root node
        if (depth != 0 and not moveNode) or parent is None:
            self.children = [
                Node(execute_move(LEFT, board), self, moveNode=True, moveToNode=LEFT, depth=depth - 1),
                Node(execute_move(RIGHT, board), self, moveNode=True, moveToNode=RIGHT, depth=depth - 1),
                Node(execute_move(UP, board), self, moveNode=True, moveToNode=UP, depth=depth - 1),
                Node(execute_move(DOWN, board), self, moveNode=True, moveToNode=DOWN, depth=depth - 1)
            ]
        else:
            self.children = []

        # if node is a move node, calculate the score by using the children
        if parent is not None and moveNode:
            # if the move is invalid, set the score to 0 and break
            if board_equals(self.board, parent.board):
                self.score = 0
                return

            self.get_score_with_all_possible_moves()
        else:  # if the node is not a move node, calculate the score based on the board
            # if the non-move node has children, take the best score of the children that is a move node
            if len(self.children) > 0:
                self.score = max([child.score for child in self.children])
            else:  # if they don't have children, calculate the score based on the board
                self.score = Node.get_score_of_board(self.board)

    def get_score_with_all_possible_moves(self):
        """
        Calculates the score of the move node based on the probability and score of its children.
        :return: None
        """
        empty_cells = np.argwhere(self.board == 0)

        possible_boards = []
        for cell in empty_cells:
            # add a 2 to the empty cell
            new_board = self.board.copy()
            new_board[cell[0]][cell[1]] = 2
            probability = 0.9 / len(empty_cells)
            possible_boards.append([Node(new_board, self, depth=self.depth, moveNode=False), probability])
            # add a 4 to the empty cell
            new_board = self.board.copy()
            new_board[cell[0]][cell[1]] = 4
            probability = 0.1 / len(empty_cells)
            possible_boards.append([Node(new_board, self, depth=self.depth, moveNode=False), probability])

        # multiply the children's score with the probability of the board
        self.score = np.add.reduce([child[0].score * child[1] for child in possible_boards])
        self.children: list[Node] = list(map(lambda x: x[0], possible_boards))

    @staticmethod
    def get_score_of_board(board):
        """
        Calculates the score of a board.
        :param board: the board to calculate the score of
        :return: the score of the board
        """
        free_cells = get_empty_tiles_score(board)
        weighted_board_sum = np.sum(board * board_weights)
        return np.dot([1, FREE_CELL_BIAS], [weighted_board_sum, free_cells ** 2])

    def getBestMove(self):
        """
        :return: the best move to make based on the score
        """
        # if node is not a parent node, break
        if self.parent is not None:
            raise NotImplementedError("This method can only be called on the root node.")

        return [node for node in self.children if node.score == self.score][0].moveToNode


def find_best_move(board):
    """
    :param board: board
    :return: best move to make (int)
    """

    # adjust the tree depth based on the amount of empty tiles
    empty_tiles = get_empty_tiles_score(board)

    # adjust the scoring bias based on the amount of empty tiles
    global FREE_CELL_BIAS
    FREE_CELL_BIAS = 10 / (empty_tiles if empty_tiles > 0 else 1)

    root = Node(board, depth=1 if empty_tiles > 8 else (2 if empty_tiles > 2 else 3))  # build the tree with the possible moves
    return root.getBestMove()


def get_empty_tiles_score(board):
    """
    Return the number of empty tiles on the board
    """
    return np.count_nonzero(board == 0)


def execute_move(move, board):
    """
    move and return the grid without placing a new random tile
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
    return  (newboard == board).all()  
