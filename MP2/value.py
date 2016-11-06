
def minimax(board, player):
    s = state(player, player.pawnName)
    pawnList = find_all_pawn(board, s.currTurn)
    bestMove = []
    bestVal = 0
    dir = player.goal
    for pawn in pawnList:
        # # Debug
        # if pawn == (7,7,'b'):
        #     print('Hi')

        move = [pawn, dir, 'l']
        if check_pawn_move(board, move):
            captured = take_action(board, move)
            # Change state for recursion
            s.depth = s.depth + 1
            s.currTurn = changeTurn(s.currTurn)
            # Call
            result = minValue(board, s)
            # Restore state
            s.depth = s.depth - 1
            s.currTurn = changeTurn(s.currTurn)
            if result > bestVal:
                bestVal = result
                bestMove = move
            retrieve_action(board, move, captured)
        move = [pawn, dir, 'f']
        if check_pawn_move(board, move):
            captured = take_action(board, move)
            # Change state for recursion
            s.depth = s.depth + 1
            s.currTurn = changeTurn(s.currTurn)
            # Call
            result = minValue(board, s)
            # Restore state
            s.depth = s.depth - 1
            s.currTurn = changeTurn(s.currTurn)
            if result > bestVal:
                bestVal = result
                bestMove = move
            retrieve_action(board, move, captured)
        move = [pawn, dir, 'r']
        if check_pawn_move(board, move):
            captured = take_action(board, move)
            # Change state for recursion
            s.depth = s.depth + 1
            s.currTurn = changeTurn(s.currTurn)
            # Call
            result = minValue(board, s)
            # Restore state
            s.depth = s.depth - 1
            s.currTurn = changeTurn(s.currTurn)
            if result > bestVal:
                bestVal = result
                bestMove = move
            retrieve_action(board, move, captured)
    return bestMove

# func: min_Value function.
# input: board, current board
#        state, containing the player who calls minimax/alpha-beta algorithm and player who moves now.
def minValue(board, state):
    if cutOff(state.depth):
        return utility(board, state)
    else:
        val = 9999  # Suppose 9999 = infinity
        # bestMove = []
        pawnList = find_all_pawn(board, state.currTurn)
        # Find current player's direction
        dir = ''
        if state.currTurn == state.player.pawnName:
            dir = state.player.goal
        else:
            if state.player.goal == 'U':
                dir = 'D'
            else:
                dir = 'U'
        # Check each pawn
        for pawn in pawnList:
            move = [pawn, dir, 'l']
            if check_pawn_move(board, move):
                captured = take_action(board, move)
                # Change state for recursion
                state.depth = state.depth + 1
                state.currTurn = changeTurn(state.currTurn)
                # Call
                result = maxValue(board, state)
                # Restore state
                state.depth = state.depth - 1
                state.currTurn = changeTurn(state.currTurn)
                if result < val:
                    val = result
                    # bestMove = move
                retrieve_action(board, move, captured)
            move = [pawn, dir, 'f']
            if check_pawn_move(board, move):
                captured = take_action(board, move)
                # Change state for recursion
                state.depth = state.depth + 1
                state.currTurn = changeTurn(state.currTurn)
                # Call
                result = maxValue(board, state)
                # Restore state
                state.depth = state.depth - 1
                state.currTurn = changeTurn(state.currTurn)
                if result < val:
                    val = result
                    # bestMove = move
                retrieve_action(board, move, captured)
            move = [pawn, dir, 'r']
            if check_pawn_move(board, move):
                captured = take_action(board, move)
                # Change state for recursion
                state.depth = state.depth + 1
                state.currTurn = changeTurn(state.currTurn)
                # Call
                result = maxValue(board, state)
                # Restore state
                state.depth = state.depth - 1
                state.currTurn = changeTurn(state.currTurn)
                if result < val:
                    val = result
                    # bestMove = move
                retrieve_action(board, move, captured)
        return val

# func: max_Value function.
# input: board, current board
#        state, containing the player who calls minimax/alpha-beta algorithm and player who moves now.
def maxValue(board, state):
    if cutOff(state.depth):
        return utility(board, state)
    else:
        val = -9999  # Suppose -9999 = -infinity
        # bestMove = []
        pawnList = find_all_pawn(board, state.currTurn)
        # Find current player's direction
        dir = ''
        if state.currTurn == state.player.pawnName:
            dir = state.player.goal
        else:
            if state.player.goal == 'U':
                dir = 'D'
            else:
                dir = 'U'
        # Check each pawn
        for pawn in pawnList:
            move = [pawn, dir, 'l']
            if check_pawn_move(board, move):
                captured = take_action(board, move)
                # Change state
                state.depth = state.depth + 1
                state.currTurn = changeTurn(state.currTurn)
                # Call
                result = minValue(board, state)
                # Restore state
                state.depth = state.depth - 1
                state.currTurn = changeTurn(state.currTurn)
                if result > val:
                    val = result
                    # bestMove = move
                retrieve_action(board, move, captured)
            move = [pawn, dir, 'f']
            if check_pawn_move(board, move):
                captured = take_action(board, move)
                # Change state
                state.depth = state.depth + 1
                state.currTurn = changeTurn(state.currTurn)
                # Call
                result = minValue(board, state)
                # Restore state
                state.depth = state.depth - 1
                state.currTurn = changeTurn(state.currTurn)
                if result > val:
                    val = result
                    # bestMove = move
                retrieve_action(board, move, captured)
            move = [pawn, dir, 'r']
            if check_pawn_move(board, move):
                captured = take_action(board, move)
                # Change state
                state.depth = state.depth + 1
                state.currTurn = changeTurn(state.currTurn)
                # Call
                result = minValue(board, state)
                # Restore state
                state.depth = state.depth - 1
                state.currTurn = changeTurn(state.currTurn)
                if result > val:
                    val = result
                    # bestMove = move
                retrieve_action(board, move, captured)
        return val