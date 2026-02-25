"""
Tic Tac Toe Player
"""

import math
import copy

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
    # Checking if it's a terminal state
    if terminal(board) == True:
        return None
    
    # First move is always from player X
    if board == [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]:
        return X
    
    used_cells = 0   # Counts the amount of cells that have already been used
    for row in board:
        for cell in row:
            if cell == X or cell == O:
                used_cells += 1

    if (used_cells % 2) != 0:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Checking if it's a terminal state
    if terminal(board) == True:
        return None
    
    actions_set = []    # List of every possible action

    i = 0  # Row counter
    for row in board:
        j = 0  # Cell counter
        for cell in row:
            if cell == EMPTY:
                actions_set.append((i, j))
            j += 1

            if j > 2:
                i += 1

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)

    i_action = action[0]    # Row of the action
    j_action = action[1]    # Cell of the action
    
    if (result_board[i_action][j_action] != EMPTY) or (i_action > 2) or (j_action > 2):
        raise Exception("Invalid action")
    
    result_board[i_action][j_action] = player(board)
    
    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking if X won the game
    if (board[0][0] == X and board[0][1] == X and board[0][2] == X) or (board[1][0] == X and board[1][1] == X and board[1][2] == X) or (board[2][0] == X and board[2][1] == X and board[2][2] == X) or (board[0][0] == X and board[1][1] == X and board[2][2] == X) or (board[0][2] == X and board[1][1] == X and board[2][0] == X) or (board[0][0] == X and board[1][0] == X and board[2][0] == X) or (board[0][1] == X and board[1][1] == X and board[2][1] == X) or (board[0][2] == X and board[1][2] == X and board[2][2] == X):
        return X
    # Checking if O won the game
    elif (board[0][0] == O and board[0][1] == O and board[0][2] == O) or (board[1][0] == O and board[1][1] == O and board[1][2] == O) or (board[2][0] == O and board[2][1] == O and board[2][2] == O) or (board[0][0] == O and board[1][1] == O and board[2][2] == O) or (board[0][2] == O and board[1][1] == O and board[2][0] == O) or (board[0][0] == O and board[1][0] == O and board[2][0] == O) or (board[0][1] == O and board[1][1] == O and board[2][1] == O) or (board[0][2] == O and board[1][2] == O and board[2][2] == O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Checking if someone won the game
    if winner(board) != None:
        return True
    
    # Checking if there is any empty cell
    for row in board:
        if EMPTY in row:
            return False
    
    # If no one won the game and there is no empty cell, it's a draw
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == False:
        raise Exception("Game is not over yet")
    
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

# TODO
# Still not playing optmally
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Checking it it's a terminal state
    if terminal(board) == True:
        return None
    
    # Checking whose turn is it
    if player(board) == X:
        score, optimal_action = max_loop(board, -1000, None) # The arguments are: a board, a default utility number and an action
    elif player(board) == O:
        score, optimal_action = mini_loop(board, 1000, None) # The arguments are: a board, a default utility number and an action

    return optimal_action

def max_loop(board, score, chosen_action):
    """
    Returns the utility of the decision and the optimal action of the X player
    """
    possibilities = actions(board)

    if possibilities == None:
        return utility(board), chosen_action

    for action in possibilities:
        try:
            result_board = result(board, action)
        except:
            continue
        final_score, optimal_action = mini_loop(result_board, score, action)
        if final_score >= score:
            score = final_score
            chosen_action = optimal_action

    return (score, chosen_action)
        
def mini_loop(board, score, chosen_action):
    """
    Returns the utility of the decision and the optimal action of the O player
    """
    possibilities = actions(board)

    # If it's a terminal state, calculates it's utility
    if possibilities == None:
        return utility(board), chosen_action

    for action in possibilities:
        try:
            result_board = result(board, action)
        except:
            continue
        final_score, optimal_action = max_loop(result_board, score, action)
        if final_score <= score:
            score = final_score
            chosen_action = optimal_action

    return (score, chosen_action)
