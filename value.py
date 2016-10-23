
# func: Find safe piece in the board
def safe_piece(board, pawnName, dir):
    bonus = 10
    pawnList = find_all_pawn(board, pawnName)
    val = 0
    enemy = ''
    if pawnName == 'w':
        enemy = 'b'
    else:
        enemy = 'w'
    for pawn in pawnList:
        x = pawn[0]; y = pawn[1]
        if dir == 'D':
            if y == 7:
                val = val + bonus
            elif x == 0 and board[y+1][x+1] != enemy:
                val = val + bonus
            elif x == 7 and board[y+1][x-1] != enemy:
                val = val +bonus
            elif board[y+1][x+1] != enemy and board[y+1][x-1] != enemy:
                val = val + bonus
        if dir == 'U':
            if y == 0:
                val = val + bonus
            elif x == 0 and board[y - 1][x + 1] != enemy:
                val = val + bonus
            elif x == 7 and board[y - 1][x - 1] != enemy:
                val = val + bonus
            elif board[y - 1][x + 1] != enemy and board[y - 1][x - 1] != enemy:
                val = val + bonus
    return val

# func: Evaluate how many opponent's piece in total has been captured.
def captured_piece(board, pawnName):
    bonus = 10
    val = 0
    enemy = ''
    if pawnName == 'w':
        enemy = 'b'
    else:
        enemy = 'w'
    val = bonus * len(find_all_pawn(board, enemy))
    return val

# func: Evaluate the location of enemy's pieces
def enemy_piece_location(board, pawnName, dir):
    valueArr = [5, 15, 15, 5, 5, 15, 15, 5,
                2, 3, 3, 3, 3, 3, 3, 2,
                4, 6, 6, 6, 6, 6, 6, 4,
                7, 10, 10, 10, 10, 10, 10, 7,
                11, 15, 15, 15, 15, 15, 15, 11,
                16, 21, 21, 21, 21, 21, 21, 16,
                20, 28, 28, 28, 28, 28, 28, 20,
                36, 36, 36, 36, 36, 36, 36, 36
                ]
    if dir == 'D':  # If we go down, enemy go up
        valueArr.reverse()
    enemy = ''
    if pawnName == 'w':
        enemy = 'b'
    else:
        enemy = 'w'
    val = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == enemy:
                val = val + valueArr[x + y*8]
    return val


if strategy == 'offensive':
    val = val + 2 * captured_piece(board, pawnName)
else:
    val = val + capture_piece(board, pawnName)
if strategy == 'defensive':
    val = val + 2 * enemy_piece_location(board, pawnName, state.player.goal)
else:
    val = val + enemy_piece_location(board, pawnName, state.player.goal)