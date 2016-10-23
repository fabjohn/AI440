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


def minimax_Desicion (board, agent, pos):
    moves = get_possible_moves(board, agent, pos)
    value = -sys.maxsize - 1
    for move in moves:
        result_board = result(board, move, agent, pos)
        value = min_value(result_board, agent, pos)



def min_value(board, agent, pos):



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



def agent_move(board):
    agent1 = agent("mm", "off",'a')
    agent2 = agent("mm", "off",'b')
    ##agent1 move and set value
    value = 0
    for pos in range(63):
        if board(pos) == "a":
            temp_board = board
            value = minimax_Desicion(temp_board,agent1, pos)
