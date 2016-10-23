#class chessBoard:
 #       def __init__(self):
 #       def creat_board(self):
 #moves:
 # 1: northwest 2: north 3: northeast
 # 4: southwest 5: south 6: southeast
#initialize board
import sys
class agent:
    def __init__(self, algo, strat, type):
        self.position = 0
        self.status = 0
        self.algo = algo
        self.strat = strat
        self.type = type

class board:
    def __init__(self):
        self.board = self. creat_board()

    def creat_board(self):
        board = []
        for y in range(8):
            board_y = []
            for x in range(8):
                board_y.append('.')
            board.append(board_y)

        for x in range(8):
            board[0][x] = 'a'
            board[1][x] = 'a'
            board[6][x] = 'b'
            board[7][x] = 'b'
        return board        ##yx index


def minimax_Desicion (board, agent, pos, depth):
    moves = get_possible_moves(board, agent, pos)
    maxvalue = -sys.maxsize - 1
    bestmove = 0
    for move in moves:
        result_board = result(board, move, agent, pos)
        depth = depth -1
        temp = min_value(result_board, agent, pos, depth)
        if temp > maxvalue:
            maxvalue = temp
            bestmove = move
    return bestmove


def min_value(board, agent, pos, depth):
    if agent.type == 'a' and pos/8 == 7 or depth == 0:            # a at terminal state
        return get_value(board, agent, pos)
    elif agent.type == 'b' and pos/8 == 0 or depth == 0:
        return get_value(board, agent, pos)
    value = sys.maxsize
    moves = get_possible_moves(board, agent, pos)
    for move in moves:
        result_board = result(board, move, agent, pos)
        depth = depth - 1
        temp = max_value(result_board, agent, pos, depth)
        if temp < value:
            value = temp
    return value

def max_value(board, agent, pos, depth):
    if agent.type == 'a' and pos/8 == 7 or depth == 0:            # a at terminal state
        return get_value(board, agent, pos)
    elif agent.type == 'b' and pos/8 == 0 or depth == 0:
        return get_value(board, agent, pos)
    value = -sys.maxsize - 1
    moves = get_possible_moves(board, agent, pos)
    for move in moves:
        result_board = result(board, move, agent, pos)
        depth = depth -1
        temp = min_value(result_board, agent, pos, depth)
        if temp > value:
            value = temp
    return value

def result(board, move, agent, pos):
    new_board = board
    x_index = pos % 8
    y_index = pos / 8
    new_board[y_index][x_index] = '.'
    if move == 1:
        new_board[y_index - 1][x_index-1] = agent.type
    elif move == 2:
        new_board[y_index - 1][x_index] = agent.type
    elif move == 3:
        new_board[y_index - 1][x_index + 1] = agent.type
    elif move == 4:
        new_board[y_index + 1][x_index - 1] = agent.type
    elif move == 5:
        new_board[y_index + 1][x_index] = agent.type
    elif move == 6:
        new_board[y_index + 1][x_index + 1] = agent.type

    return new_board


def get_possible_moves(board, agent, pos):
    x_index = pos % 8
    y_index = pos / 8
    moves = []
    if agent.type == 'a':       # down player1 a
        if x_index != 0 and y_index != 7 and board[y_index][x_index] != 'a':
            moves.append(4)
        if y_index != 7:
            moves.append(5)
        if x_index != 7 and y_index != 7 and board[y_index][x_index] != 'a':
            moves.append(6)
    else:                   # up player 2 b
        if x_index != 0 and y_index != 0 and board[y_index][x_index] != 'b':
            moves.append(1)
        if y_index != 7:
            moves.append(2)
        if x_index != 7 and y_index != 0 and board[y_index][x_index] != 'b':
            moves.append(3)
    return moves

def get_value(board, agent, pos):
    val = 0
    val = val + piece_count(board, agent)
    val = val + piece_location(board, agent)
    val = val + safe_piece(board, agent)

    if agent.strat == 'off':    # offensive
        val = val + 2 * captured_piece(board, agent)
        val = val + enemy_peice(board, agent)
    else:
        val = val + captured_piece(board, agent)
        val = val + 2 * enemy_peice(board, agent)

    return val


def piece_count(board, agent):
    count = 0
    for x in range(8):
        for y in range(8):
            if board[y][x] == agent.type:
                count = count + 1
    count = count * 10
    return count

def piece_location(board, agent):
    value_map = [ 5, 15, 15,  5,  5, 15, 15,  5,
                 2,  3,  3,  3,  3,  3,  3,  2,
                 4,  6,  6,  6,  6,  6,  6,  4,
                 7, 10, 10, 10, 10, 10, 10,  7,
                11, 15, 15, 15, 15, 15, 15, 11,
                16, 21, 21, 21, 21, 21, 21, 16,
                20, 28, 28, 28, 28, 28, 28, 20,
                36, 36, 36, 36, 36, 36, 36, 36
                ]
    if agent.type == 'a':
        value_map.reverse()
    value = 0
    for x in range(8):
        for y in range(8):
            if board[y][x] == agent.type:
                value = value + value_map[x + y*8]
    return value

def safe_piece(board, agent):
    val_map = [ 5, 15, 15,  5,  5, 15, 15,  5,
                 2,  3,  3,  3,  3,  3,  3,  2,
                 4,  6,  6,  6,  6,  6,  6,  4,
                 7, 10, 10, 10, 10, 10, 10,  7,
                11, 15, 15, 15, 15, 15, 15, 11,
                16, 21, 21, 21, 21, 21, 21, 16,
                20, 28, 28, 28, 28, 28, 28, 20,
                36, 36, 36, 36, 36, 36, 36, 36
                ]
    if agent.type == 'a':
        enemy = 'b'
    else:
        enemy = 'a'
    val = 0
    for x in range(8):
        for y in range(8):
            if board[y][x] == agent.type:
                if agent.type == 'a':
                    if y == 7:
                        val = val + val_map[x+y*8] * 1.5
                    elif x == 0 and board[y+1][x+1] != enemy:
                        val = val + val_map[x+y*8] * 1.5
                    elif x == 7 and board[y+1][x-1] != enemy:
                        val = val + val_map[x + y * 8] * 1.5
                    elif board[y + 1][x + 1] != enemy and board[y + 1][x - 1] != enemy:
                        val = val + val_map[x + y * 8] * 1.5
                else:
                    if y == 0:
                        val = val + val_map[x+y*8] * 1.5
                    elif x == 0 and board[y-1][x+1] != enemy:
                        val = val + val_map[x+y*8] * 1.5
                    elif x == 7 and board[y-1][x-1] != enemy:
                        val = val + val_map[x + y * 8] * 1.5
                    elif board[y - 1][x + 1] != enemy and board[y - 1][x - 1] != enemy:
                        val = val + val_map[x + y * 8] * 1.5
    return val

def captured_piece(board, agent):
    count = 0
    if agent.type == 'a':
        enemy = 'b'
    else:
        enemy = 'a'
    for x in range(8):
        for y in range(8):
            if board[y][x] == enemy:
                count = count + 1
    count = count * 10
    return count

def enemy_piece(board, agent):
    val_map = [ 5, 15, 15,  5,  5, 15, 15,  5,
                 2,  3,  3,  3,  3,  3,  3,  2,
                 4,  6,  6,  6,  6,  6,  6,  4,
                 7, 10, 10, 10, 10, 10, 10,  7,
                11, 15, 15, 15, 15, 15, 15, 11,
                16, 21, 21, 21, 21, 21, 21, 16,
                20, 28, 28, 28, 28, 28, 28, 20,
                36, 36, 36, 36, 36, 36, 36, 36
                ]
    if agent.type == 'a':
        val_map.reverse()
        enemy = 'b'
    else:
        enemy = 'a'
    val = 0
    for x in range(8):
        for y in range(8):
            if board[y][x] == enemy:
                val = val + val_map[x + y * 8]

    return val




def agent_move(board):
    agent1 = agent('mm', 'off','a')
    agent2 = agent('mm', 'off','b')
    ##agent1 move and set value
    value = 0
    for pos in range(63):
        if board(pos) == "a":
            temp_board = board
            value = minimax_Desicion(temp_board,agent1, pos, 3)
