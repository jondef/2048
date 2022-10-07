# logic.py to be
# imported in the 2048.py file

import random
import numpy as np


def start_game():
    """
    This function will initialize the grid at the start of the game.
    It will create a 4x4 matrix with all the elements as 0.
    Then it will add a 2 in the grid at random position.
    The grid will be returned.
    :return: np.array
    """
    # create the board
    mat = np.array([[0] * 4] * 4)

    # print controls
    print("Commands are as follows: ")
    print("'W' or 'w' : Move Up")
    print("'S' or 's' : Move Down")
    print("'A' or 'a' : Move Left")
    print("'D' or 'd' : Move Right")

    add_new_2(mat)
    return mat


def add_new_2(mat):
    """
    This function will add a new 2 in the grid at a random empty position.
    :param mat: np.array
    :return: None
    """
    # choose a random index for row and column.
    r = random.randint(0, 3)
    c = random.randint(0, 3)

    # while loop to iterate until an empty cell is found.
    while mat[r][c] != 0:
        r = random.randint(0, 3)
        c = random.randint(0, 3)

    mat[r][c] = 2


def is_game_finished(mat):
    """
    This function will return the current state of the game.
    0 if the game is not over
    1 if the game is over and the player has won
    -1 if the game is over and the player has lost
    :param mat: np.array
    :return: int
    """
    # if any cell contains 2048 we have won
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == 2048):
                return 1

    # if we are still left with
    # at least one empty cell
    # game is not yet over
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == 0):
                return 0

    # or if no cell is empty now
    # but if after any move left, right,
    # up or down, if any two cells
    # gets merged and create an empty
    # cell then also game is not yet over
    for i in range(3):
        for j in range(3):
            if (mat[i][j] == mat[i + 1][j] or mat[i][j] == mat[i][j + 1]):
                return 0

    for j in range(3):
        if (mat[3][j] == mat[3][j + 1]):
            return 0

    for i in range(3):
        if (mat[i][3] == mat[i + 1][3]):
            return 0

    # else we have lost the game
    return -1


# all the functions defined below
# are for left swap initially.

# function to compress the grid
# after every step before and
# after merging cells.
def compress(mat):
    # bool variable to determine
    # any change happened or not
    changed = False

    # empty grid
    new_mat = []

    # with all cells empty
    for i in range(4):
        new_mat.append([0] * 4)

    # here we will shift entries
    # of each cell to it's extreme
    # left row by row
    # loop to traverse rows
    for i in range(4):
        pos = 0

        # loop to traverse each column
        # in respective row
        for j in range(4):
            if (mat[i][j] != 0):

                # if cell is non empty then
                # we will shift it's number to
                # previous empty cell in that row
                # denoted by pos variable
                new_mat[i][pos] = mat[i][j]

                if (j != pos):
                    changed = True
                pos += 1

    # returning new compressed matrix
    # and the flag variable.
    return new_mat, changed


# function to merge the cells
# in matrix after compressing
def merge(mat):
    changed = False

    for i in range(4):
        for j in range(3):

            # if current cell has same value as
            # next cell in the row and they
            # are non empty then
            if (mat[i][j] == mat[i][j + 1] and mat[i][j] != 0):
                # double current cell value and
                # empty the next cell
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0

                # make bool variable True indicating
                # the new grid after merging is
                # different.
                changed = True

    return mat, changed


# function to reverse the matrix
# means reversing the content of
# each row (reversing the sequence)
def reverse(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][3 - j])
    return new_mat


# function to get the transpose
# of matrix means interchanging
# rows and column
def transpose(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    return new_mat


class style():
    FG_WHITE = "\033[37m"
    FG_BLACK = "\033[30m"

    BG_GRAY = "\033[47m"
    BG_ORANGE = "\033[43m"
    BG_RED = "\033[41m"
    BG_YELLOW = "\033[103m"

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'


def print_mat(mat):
    for i in range(4):
        for j in range(4):
            # print with colors
            if (mat[i][j] == 2048):
                print(style.FG_WHITE + style.BG_YELLOW, end="")
            elif (mat[i][j] == 1024):
                print(style.FG_WHITE + style.BG_YELLOW, end="")
            elif (mat[i][j] == 512):
                print(style.FG_WHITE + style.BG_YELLOW, end="")
            elif (mat[i][j] == 256):
                print(style.FG_WHITE + style.BG_YELLOW, end="")
            elif (mat[i][j] == 128):
                print(style.FG_WHITE + style.BG_YELLOW, end="")
            elif (mat[i][j] == 64):
                print(style.FG_WHITE + style.BG_RED, end="")
            elif (mat[i][j] == 32):
                print(style.FG_WHITE + style.BG_RED, end="")
            elif (mat[i][j] == 16):
                print(style.FG_WHITE + style.BG_ORANGE, end="")
            elif (mat[i][j] == 8):
                print(style.FG_WHITE + style.BG_ORANGE, end="")
            elif (mat[i][j] == 4):
                print(style.FG_BLACK + style.BG_GRAY, end="")
            elif (mat[i][j] == 2):
                print(style.FG_BLACK + style.BG_GRAY, end="")
            elif (mat[i][j] == 0):
                print(style.BLUE, end="")

            print(mat[i][j], end="")  # print cell content

            print(style.RESET, end="\t")  # reset color
        print("", end="\n")  # print new line


# function to update the matrix
# if we move / swipe left
def move_left(grid):
    # first compress the grid
    new_grid, changed1 = compress(grid)

    # then merge the cells.
    new_grid, changed2 = merge(new_grid)

    changed = changed1 or changed2

    # again compress after merging.
    new_grid, temp = compress(new_grid)

    # return new matrix and bool changed
    # telling whether the grid is same
    # or different
    return new_grid, changed


# function to update the matrix
# if we move / swipe right
def move_right(grid):
    # to move right we just reverse
    # the matrix
    new_grid = reverse(grid)

    # then move left
    new_grid, changed = move_left(new_grid)

    # then again reverse matrix will
    # give us desired result
    new_grid = reverse(new_grid)
    return new_grid, changed


# function to update the matrix
# if we move / swipe up
def move_up(grid):
    # to move up we just take
    # transpose of matrix
    new_grid = transpose(grid)

    # then move left (calling all
    # included functions) then
    new_grid, changed = move_left(new_grid)

    # again take transpose will give
    # desired results
    new_grid = transpose(new_grid)
    return new_grid, changed


# function to update the matrix
# if we move / swipe down
def move_down(grid):
    # to move down we take transpose
    new_grid = transpose(grid)

    # move right and then again
    new_grid, changed = move_right(new_grid)

    # take transpose will give desired
    # results.
    new_grid = transpose(new_grid)
    return new_grid, changed

