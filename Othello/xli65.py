import time
import gameplay
import random
from copy import deepcopy

DEFAULT_LOOK_AHEAD = 5

INFINITE = 999999999
MINIMUM_VALUE = -INFINITE
MAXIMUM_VALUE = INFINITE
BOARD_SIZE = 8

BOARD_SCORE = 1

BLACK = "B"
WHITE = "W"
BONUS_SCORE = 20 # bonus score for stable chess
LIBERTY_SCORE = 8 # punish score for liberty

EVAL_SCORES = [ [99, -8, 8, 6, 6, 8, -8, 99],
                [-8, -24, -4, -3, -3, -4, -24, -8],
                [8, -4, 7, 4, 4, 7, -4, 8],
                [6, -3, 4, 0, 0, 4, -3, 6],
                [6, -3, 4, 0, 0, 4, -3, 6],
                [8, -4, 7, 4, 4, 7, -4, 8],
                [-8, -24, -4, -3, -3, -4, -24, -8],
                [99, -8, 8, 6, 6, 8, -8, 99]];

CORNER = [(0,0),(0,7),(7,0),(7,7)]
TOP_LEFT = [(0,1),(1,0),(1,1)]
TOP_RIGHT = [(0,6),(1,7),(1,6)]
BUTTOM_LEFT = [(6,0),(6,1),(7,1)]
BUTTOM_RIGHT = [(6,6),(6,7),(7,6)]

step = 0

tt1 = 0
tt2 = 0

class State:
    def __init__(self, board, color):
        self.board = board
        self.color = color

class Successor(State):
    def __init__(self, board, color, move):
        self.board = board
        self.color = color
        self.move = move

    # def value(self):
    #     evaluate_board(self.board,step,r)

def get_valid_moves(state):
    """check whether a move is valid for a player"""
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if gameplay.valid(state.board, state.color, (x,y)):
                moves.append((x, y))
    return moves

def do_move(state, move):
    """put a chess on the board, and do flip"""
    newBoard = deepcopy(state.board)
    gameplay.doMove(newBoard, state.color, move)
    opponentColor = gameplay.opponent(state.color)
    return Successor(newBoard, opponentColor, move)

def get_successors(state):
    """return all successor states"""
    successors = []
    moves = get_valid_moves(state)
    for move in moves:
        successor = do_move(state, move)
        successors.append(successor)
    return successors

def is_end_state(s):
    """chech whether get the end"""
    return gameplay.gameOver(s.board)

def is_on_board(x,y):
    """check whether a chess is on board"""
    return BOARD_SIZE - x > 0 and x >= 0 and BOARD_SIZE - y > 0 and y >= 0

def evaluate_point(x,y):
    """return the static move value"""
    return EVAL_SCORES[x][y]

def evaluate_board(board,step,r):
    """calculate the total point for a state, including chess
        count score, the stable, liberty, and the static value
        of a certain move"""
    white_count = 0
    black_count = 0
    white_score = 0
    black_score = 0
    if step <=46:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == '.':
                    continue
                liberty_count = 0

                for i_delta in [-1,0,1]:
                    for j_delta in [-1,0,1]:
                        if is_on_board(i + i_delta, j + j_delta) and board[i + i_delta][j + j_delta] == '.':
                            liberty_count = liberty_count + 1

                if board[i][j] == BLACK:
                    black_count = black_count + 1;
                    black_score = black_score + evaluate_point(i,j)
                    black_score = black_score - liberty_count * LIBERTY_SCORE if not r else black_score + liberty_count * LIBERTY_SCORE
                else:
                    white_count = white_count + 1;
                    white_score = white_score + evaluate_point(i,j)
                    white_score = white_score - liberty_count * LIBERTY_SCORE if not r else white_score + liberty_count * LIBERTY_SCORE

            if white_count == 0:
                return MAXIMUM_VALUE

            if black_count == 0:
                return MINIMUM_VALUE

            if white_count + black_count == BOARD_SIZE * BOARD_SIZE:
                if white_count > black_count:
                    return MINIMUM_VALUE
                elif black_count > white_count:
                    return MAXIMUM_VALUE

        black_bonus, white_bonus = evaluate_stable_bonus(board)

        return (black_score + black_bonus) - (white_score + white_bonus)
    else:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == BLACK:
                    black_count = black_count + 1;
                else:
                    white_count = white_count + 1;

            if white_count == 0:
                return MAXIMUM_VALUE

            if black_count == 0:
                return MINIMUM_VALUE

            if white_count + black_count == BOARD_SIZE * BOARD_SIZE:
                if white_count > black_count:
                    return MINIMUM_VALUE
                elif black_count > white_count:
                    return MAXIMUM_VALUE

        return black_count - white_count

def get_neighbors(i,j):
    """return all valid neighbors' moves"""
    neighbors = []
    for i_delta in [-1,0,1]:
        for j_delta in [-1,0,1]:
            if is_on_board(i + i_delta, j + j_delta):
                neighbors.append((i + i_delta, j + j_delta))
    return neighbors

def evaluate_stable_bonus(board):
    """Check whether a state is stable and give proper
        bonus according to the stabled chess count"""
    white_score = 0
    black_score = 0
    for (i,j) in CORNER:
        color_of_corner = board[i][j]
        if color_of_corner != '.':
            neighbors = get_neighbors(i,j) # the C and X positions
            for (i_neighbor, j_neighbor) in neighbors:
                if board[i][j] == BLACK and board[i_neighbor][j_neighbor] == BLACK:
                    black_score = black_score - evaluate_point(i_neighbor, j_neighbor)
                elif board[i][j] == WHITE and board[i_neighbor][j_neighbor] == WHITE:
                    white_score = white_score - evaluate_point(i_neighbor, j_neighbor)
            if i == 0 and j == 0: # left up corner
                shortest = BOARD_SIZE
                for delta in range(BOARD_SIZE):
                    for deltaj in range(shortest):
                        if board[delta][deltaj] != color_of_corner:
                            if deltaj < shortest:
                                shortest = deltaj - 1
                            elif deltaj == shortest:
                                shortest = shortest - 1
                            break
                        else:
                            if color_of_corner == BLACK:
                                black_score = black_score + BONUS_SCORE
                            elif color_of_corner == WHITE:
                                white_score = white_score + BONUS_SCORE

            if i == 0 and j == 7: # left bottom corner
                shortest = BOARD_SIZE
                for delta in range(BOARD_SIZE):
                    index = 0
                    for deltaj in reversed(range(BOARD_SIZE)):
                        if board[delta][7] != color_of_corner or index == shortest:
                            if index < shortest:
                                shortest = index - 1
                            elif index == shortest:
                                shortest = shortest-1
                            break
                        else:
                            index = index + 1
                            if color_of_corner == BLACK:
                                black_score = black_score + BONUS_SCORE
                            elif color_of_corner == WHITE:
                                white_score = white_score + BONUS_SCORE

            if i == 7 and j == 0: # right up corner
                shortest = BOARD_SIZE
                for delta in reversed(range(BOARD_SIZE)):
                    for deltaj in range(shortest):
                        if board[delta][deltaj] != color_of_corner:
                            if deltaj < shortest:
                                shortest = deltaj - 1
                            elif deltaj == shortest:
                                shortest = shortest - 1
                            break
                        else:
                            if color_of_corner == BLACK:
                                black_score = black_score + BONUS_SCORE
                            elif color_of_corner == WHITE:
                                white_score = white_score + BONUS_SCORE

            if i == 7 and j == 7: # right bottom corner
                shortest = BOARD_SIZE
                for delta in reversed(range(BOARD_SIZE)):
                    index = 0
                    for deltaj in reversed(range(BOARD_SIZE)):
                        if board[delta][7] != color_of_corner or index == shortest:
                            if index < shortest:
                                shortest = index - 1
                            elif index == shortest:
                                shortest = shortest-1
                            break
                        else:
                            index = index + 1
                            if color_of_corner == BLACK:
                                black_score = black_score + BONUS_SCORE
                            elif color_of_corner == WHITE:
                                white_score = white_score + BONUS_SCORE

    return (black_score, white_score)

def do_alpha_beta_search(state, remaining_time, reversed, remaining_count,step,r):
    """ alpha beta search. it will call two different sub-method
        to process alpha beta search in different case"""
    color = state.color
    tt1 = time.time()
    if(color == BLACK and reversed == False) or (color == WHITE and reversed == True):
        move, value = get_move_with_max_value(state, MINIMUM_VALUE, MAXIMUM_VALUE, remaining_time, remaining_count,step,r)
    else:
        move, value = get_move_with_min_value(state, MINIMUM_VALUE, MAXIMUM_VALUE, remaining_time, remaining_count,step,r)
    tt2 = time.time()
    print "Took: ", tt2 - tt1, " Value: ", value
    print ""
    return move

def get_move_with_max_value(state, alpha, beta, remaining_time, remaining_count,step, r,passed=0):
    """ do alpha-beta cut off,return the max value of all successors which are not cut off"""
    remaining_count = remaining_count - 1

    v = alpha
    successors = get_successors(state)
    best_move = None

    if len(successors) == 0:
        if passed == 1:
            v = evaluate_board(state.board,step,r)
        else:
            v = get_move_with_min_value(state, alpha, beta, remaining_time, remaining_count,step, 1)
        return ("pass", v)

    successors = sorted(successors, key=lambda succ: evaluate_board(succ.board,step,r), reverse=True)

    if remaining_count == 0:
        v = evaluate_board(successors[0].board,step,r)
        return (successors[0].move, v)

    best_move = successors[0].move
    for successor in successors:
        new_v = get_move_with_min_value(successor, alpha, beta, remaining_time, remaining_count,step,r,0)[1]

        if v < new_v:
            v = new_v
            best_move = successor.move
        if v >= beta:
            best_move = successor.move
            return (best_move, v)
        alpha = max(alpha, v)
    return (best_move, alpha)

def get_move_with_min_value(state, alpha, beta, remaining_time, remaining_count,step, r,passed=0):
    """do alpha beta cut off and return the min value of all successors which are not cut off"""
    remaining_count = remaining_count - 1

    v = beta
    successors = get_successors(state)
    best_move = None

    if len(successors) == 0:
        if passed == 1:
            v = evaluate_board(state.board,step,r)
        else:
            v = get_move_with_min_value(state, alpha, beta, remaining_time, remaining_count,step,r, 1)
        return ("pass", v)

    successors = sorted(successors, key=lambda succ: evaluate_board(succ.board,step,r))

    if remaining_count == 0:
        v = evaluate_board(successors[0].board,step,r)
        return (successors[0].move, v)

    best_move = successors[0].move
    for successor in successors:
        new_v = get_move_with_max_value(successor, alpha, beta, remaining_time, remaining_count,step,0)[1]
        if v > new_v:
            v = new_v
            best_move = successor.move
        if v <= alpha:
            best_move = successor.move
            return (best_move, v)
        beta = min(beta, v)
    return (best_move, beta)

def nextMoveR(board, color, remaining_time):
    return nextMove(board, color, remaining_time, True)

def nextMove(board, color, remaining_time, reversed = False):
    blank = 0
    look_ahead = DEFAULT_LOOK_AHEAD
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == '.':
                blank = blank + 1
    step = BOARD_SIZE * BOARD_SIZE - 4 - blank # 60 step total

    if step > 50:
        look_ahead = 64 - step
    else:
        look_ahead = 5
    state = State(board, color)

    if is_end_state(state):
        return "pass"

    result = do_alpha_beta_search(state, remaining_time, reversed, look_ahead,step,reversed)
    print "Step:", step, " Move:", result
    return result
