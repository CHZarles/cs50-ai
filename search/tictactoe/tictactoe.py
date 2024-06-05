"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


""" 
The player function should take a board state as input, and return which player’s turn it is (either X or O).
In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
"""


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0
    for row in board:
        for col in row:
            if col == EMPTY:
                continue
            elif col == X:
                x_num += 1
            elif col == O:
                o_num += 1
    if x_num > o_num:
        return O
    else:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_action = set()
    width = len(board)
    for i in range(width):
        for j in range(width):
            if board[i][j] == EMPTY:
                possible_action.add((i, j))
    return possible_action
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    import copy

    new_board = copy.deepcopy(board)
    current_player = player(board)
    i, j = action
    if board[i][j] != EMPTY or i < 0 or j < 0 or i >= len(board) or j >= len(board):
        raise RuntimeError("action is not vaild")

    new_board[i][j] = current_player
    return new_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    width = len(board)

    # check row
    for row in board:
        state = row[0]
        if state == EMPTY:
            continue
        if False not in (state == col for col in row):
            return state

    # check col
    for j in range(width):
        state = board[0][j]
        if state == EMPTY:
            continue
        if False not in (state == board[i][j] for i in range(width)):
            return state

    # check diagonally
    state = board[0][0]
    if state != EMPTY:
        if False not in (state == board[i][i] for i in range(width)):
            return state

    state = board[0][2]
    if state != EMPTY:
        if False not in (state == board[i][width - 1 - i] for i in range(width)):
            return state

    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    # check whether in process
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        # print("X win")
        return 1
    elif winner(board) == O:
        # print("O win")
        return -1
    else:
        # print("tie ")
        return 0

    raise NotImplementedError


def dfs(board, action) -> int:
    """
    min-max or max-min , depend on current player
    """

    new_board = result(board, action)
    if terminal(new_board):
        return utility(new_board)

    # get the worse choose
    current_player = player(board)
    opponent_actons = actions(new_board)
    if current_player == X:  # oppenent O, choose the worse one that opponent may cause
        func = min
        val = 2
        ret_value = -1  # used to reduse state
    else:
        func = max
        val = -2
        ret_value = 1  # used to reduse state

    for oppo_action in opponent_actons:
        res_val = dfs(new_board, oppo_action)
        val = func(res_val, val)
        if ret_value == val:
            break
    return val


def empty(board) -> bool:
    for row in board:
        for col in row:
            if col != EMPTY:
                return False
    return True


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # if empty board
    if empty(board):
        import random

        return (int(random.random() * 100) % 3, int(random.random() * 100) % 3)

    # check whether end
    if terminal(board):
        return None

    current_player = player(board)
    res_action = None
    val = -2 if current_player == X else 2

    # get current option actions
    current_actions = actions(board)
    # print("current_player: "  , current_player)
    for action in current_actions:
        tmp_val = dfs(board, action)
        if current_player == X:
            if tmp_val > val:
                val = tmp_val
                res_action = action
        else:
            if tmp_val < val:
                # print("update action: =====================>  " , action)
                val = tmp_val
                res_action = action
    # print("best val" , val)

    return res_action
    raise NotImplementedError
