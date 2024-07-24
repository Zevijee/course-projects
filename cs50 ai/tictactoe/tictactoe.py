"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # sets the amount of x's and o's to 0 initially
    x = 0
    o = 0

    # loops through the board and checks how many x's and o's there are
    for row in board:
        for place in row:
            if place == X:
                x = x + 1
            elif place == O:
                o = o + 1
    # returns x if o and x are equal meaning that o just went after x so now it is x's turn to go also if they are not equal then its o's turn to go
    if x == o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # create a empty set called moves to display all possible actions
    moves = set()

    # loop through each row and its index
    for i, row in enumerate(board):
        # loop through each cell in the row and its index
        for j, place in enumerate(row):
            # check if the cell is empty and add it to the set of possible moves if it is
            if place == EMPTY:
                move = (i, j)
                moves.add(move)

    # return moves
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # get the player and the action the player wants to do
    p = player(board)
    i, j = action

    # create a deepcopy of the board so the board isnt actually changed
    new_board = copy.deepcopy(board)

    # update the new board with the players move
    if i in range(3) and j in range(3) and new_board[i][j] == EMPTY:
        new_board[i][j] = p
    else:
        raise Exception('Invalid action')

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # checks rows across for wins
    for row in board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O

    # checks columns down for wins
    for col in range(len(board[0])): # loops over each column by using the length of the first row of the board
        current_col = [] # this list will hold the values of the current column being proccessed
        for place in range(len(board)): # loops over each row for the current column
           current_col.append(board[place][col]) # appends the cell value ate the current row and column to the list
        # now current_col holds all the cell values in the current coloumn

        # checks if all the cells in current_col have the same values and returns a winner or none based on the outcome
        if all(cell == X for cell in current_col):
            return X
        elif all(cell == O for cell in current_col):
            return O

    # checks diagonal win down to the right
    current_col = []
    for i in range(len(board)): # loops through the board to see if there is a diagonal win
        current_col.append(board[i][i]) # adds the corrosponding diagonal cell going to the right

    # checks if all the cells in current_col have the same values and returns a winner or none based on the outcome

    if all(cell == X for cell in current_col):
        return X
    elif all(cell == O for cell in current_col):
        return O

    # checks diagonal win down to the left
    current_col = []
    for i in range(len(board)): # adds the diagonal down to the left cells
        current_col.append(board[i][len(board) -i -1])

    # checks if all the cells in current_col have the same values and returns a winner or none based on the outcome

    if all(cell == X for cell in current_col):
        return X
    elif all(cell == O for cell in current_col):
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check for a win
    win = winner(board)
    if win is not None:
        return True

    # check for any empty squares if there is one then its not a tie
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # if no empty cells are found and theres no winner its a tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    W = winner(board) # gets the winner or if its a tie

    # returns the appropriate number based on the W value
    if W == X:
        return 1
    elif W == O:
        return -1
    elif W == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # if its Xes turn we want to max
    if player(board) == X:

        # set the max_utility to the lowest possible so we can go up from there
        max_utility = -math.inf
        best_move = None

        # loop through all the possible actions on the board
        for action in actions(board):

            # check the lowest utility possible for the result of the current board and the action we are on
            new_value = Min(result(board, action))

            # check if we found a higher automatic utility of the current board and do that move if we did
            if new_value > max_utility:
                max_utility = new_value
                best_move = action

        # return the best move we found
        return best_move

    # do the opposite the Xes turn if its O's turn
    else:
        max_utility = math.inf
        best_move = None

        for action in actions(board):
            new_value = Max(result(board, action))
            if new_value < max_utility:
                max_utility = new_value
                best_move = action
        return best_move

# checks for the max utility possible given a state of a board of tictactoe
def Max(board):

    # if the game is over return the utility of the game
    if terminal(board):
        return utility(board)

    # set the max_utility to the lowest possible so we can go up from there
    max_utility = -math.inf

    # loop through all the possible actions on the board given the current state
    for action in actions(board):
        # finds the lowest utility automaticly possible given a state
        new_value = Min(result(board, action))
        max_utility = max(new_value, max_utility)

    # returns the max_utility found for the best course of action taken by both players given the current state
    return max_utility

# does the direct opposite of the Max funtion
def Min(board):
    if terminal(board):
        return utility(board)

    max_utility = math.inf

    for action in actions(board):
        new_value = Max(result(board, action))
        max_utility = min(new_value, max_utility)

    return max_utility


