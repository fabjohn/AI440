#class chessBoard:
 #       def __init__(self):
 #       def creat_board(self):
 #moves:
 # 1: northwest 2: north 3: northeast
 # 4: southwest 5: south 6: southeast
#initialize board
class agent:
    def __init__(self, algo, strat, up):
        self.position = 0
        self.status = 0
        self.algo = algo
        self.strat = strat
        self.up = 0

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




def get_possible_moves(board, agent, pos):
    x_index = pos % 8
    y_index = pos / 8
    moves = []
    if agent.up == 0:       # down player1 a
        if x_index != 0 and y_index != 7 and board[y_index][x_index] != 'a':
            moves.append(5)
        if y_index != 7:
            moves.append(6)
        if x_index != 7 and y_index != 7 and board[y_index][x_index] != 'a':
            moves.append(7)
    else:                   # up player 2 b
        if x_index != 0 and y_index != 0 and board[y_index][x_index] != 'b':
            moves.append(1)
        if y_index != 7:
            moves.append(2)
        if x_index != 7 and y_index != 0 and board[y_index][x_index] != 'b':
            moves.append(3)
    return moves



def agent_move(board):
    agent1 = agent("mm", "off",0)
    agent2 = agent("mm", "off",1)
    ##agent1 move and set value
    value = 0
    for pos in range(63):
        if board(pos) == "a":
            temp_board = board
            value = minimax_Desicion(temp_board,agent1, pos)
