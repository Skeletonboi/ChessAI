from random import randint


def ini():
    board = [0 for i in range(0, 64)]
    for i in range(0, 16):
        board[i] = board[i] + 10
    for i in range(48, 64):
        board[i] = board[i] + 20
    board[0] = board[7] = 13
    board[56] = board[63] = 23
    board[1] = board[6] = 11
    board[57] = board[62] = 21
    board[2] = board[5] = 12
    board[58] = board[61] = 22
    board[3] = board[3] + 5
    board[59] = board[59] + 5
    board[4] = board[4] + 4
    board[60] = board[60] + 4
    return board


def printBoard(b):
    for i in range(0, 8):
        print str(b[56-(i*8)])+"|"+str(b[57-(i*8)])+"|"+str(b[58-(i*8)])+"|"+str(b[59-(i*8)]) + \
            "|"+str(b[60-(i*8)])+"|"+str(b[61-(i*8)])+"|"+str(b[62-(i*8)])+"|"+str(b[63-(i*8)])
        print "-----------------------"
    return 0


def GetPlayerPositions(board, player):
    r = []
    for i in range(0, 64):
        if (((board[i]-player) >= 0) and ((board[i]-player) < 10)):
            r = r + [i]
    return r


def GetPieceLegalMoves(board, position, capture_list):
    pos = position
    if board[pos] == 0:
        print "Failed Attempt to Move Empty"
        return -1
    else:
        temp = board[pos]-10
        if temp >= 0 and temp < 10:
            player = 10
        elif temp >= 10 and temp < 20:
            player = 20
        else:
            print "Unrecognized Player"
            return False
    if player == 10:
        enemy = 20
    else:
        enemy = 10
    rval = []
    # actual comparison
    r = board[pos] % 10
    # pawn comparison
    if r == 0:
        if player == 10:  # white case
            if isUEdge(board, pos) != 1:
                if board[pos+8] == 0:
                    rval = rval + [pos+8]
            if isUEdge(board, pos) != 1 and isLEdge(board, pos) != 1:
                if board[pos+7] >= 20:
                    capture_list.append(pos+7)
            if isUEdge(board, pos) != 1 and isREdge(board, pos) != 1:
                if board[pos+9] >= 20:
                    capture_list.append(pos+9)
        elif player == 20:  # black case
            if isBEdge(board, pos) != 1:
                if board[pos-8] == 0:
                    rval = rval + [pos-8]
            if isREdge(board, pos) != 1 and isBEdge(board, pos) != 1:
                if board[pos-7]-enemy < 6 and board[pos-7]-enemy >= 0:
                    capture_list.append(pos-7)
            if isBEdge(board, pos) != 1 and isLEdge(board, pos) != 1:
                if board[pos-9]-enemy < 6 and board[pos-9]-enemy >= 0:
                    capture_list.append(pos-9)
    # bishop comparison
    elif r == 2:
        rval = BiUR(board, pos, rval, enemy, capture_list)
        rval = BiUL(board, pos, rval, enemy, capture_list)
        rval = BiLL(board, pos, rval, enemy, capture_list)
        rval = BiLR(board, pos, rval, enemy, capture_list)
    # rook comparison
    elif r == 3:
        rval = RoR(board, pos, rval, enemy, capture_list)
        rval = RoL(board, pos, rval, enemy, capture_list)
        rval = RoU(board, pos, rval, enemy, capture_list)
        rval = RoD(board, pos, rval, enemy, capture_list)
    # knight comparison
    elif r == 1:
        # all possible knight moves
        temp = [pos+17, pos-17, pos+15, pos-15, pos+10, pos-10, pos+6, pos-6]
        for i in temp:
            if i >= 0 and i <= 63:
                if (i == pos+17 or i == pos-15) and isLEdge(board, i) != 1:
                    if board[i] == 0:
                        rval = rval + [i]
                    elif board[i]-enemy >= 0 and board[i]-enemy < 6:
                        capture_list.append(i)
                elif (i == pos-17 or i == pos+15) and isREdge(board, i) != 1:
                    if board[i] == 0:
                        rval = rval + [i]
                    elif board[i]-enemy >= 0 and board[i]-enemy < 6:
                        capture_list.append(i)
                elif (i == pos+10 or i == pos-6) and isLEdge(board, i) != 1 and isLEdge(board, i-1) != 1:
                    if board[i] == 0:
                        rval = rval + [i]
                    elif board[i]-enemy >= 0 and board[i]-enemy < 6:
                        capture_list.append(i)
                elif (i == pos-10 or i == pos+6) and isREdge(board, i) != 1 and isREdge(board, i+1) != 1:
                    if board[i] == 0:
                        rval = rval + [i]
                    elif board[i]-enemy >= 0 and board[i]-enemy < 6:
                        capture_list.append(i)
    # queen comparison
    elif r == 4:
        # diag checks (bishop helpers)
        rval = BiUR(board, pos, rval, enemy, capture_list)
        rval = BiUL(board, pos, rval, enemy, capture_list)
        rval = BiLL(board, pos, rval, enemy, capture_list)
        rval = BiLR(board, pos, rval, enemy, capture_list)
        # linear checks (rook helpers)
        rval = RoR(board, pos, rval, enemy, capture_list)
        rval = RoL(board, pos, rval, enemy, capture_list)
        rval = RoU(board, pos, rval, enemy, capture_list)
        rval = RoD(board, pos, rval, enemy, capture_list)
    elif r == 5:
        trval = []
        tcapture_list = []
        # diag checks (bishop helpers)
        trval = BiUR(board, pos, trval, enemy, tcapture_list)
        trval = BiUL(board, pos, trval, enemy, tcapture_list)
        trval = BiLL(board, pos, trval, enemy, tcapture_list)
        trval = BiLR(board, pos, trval, enemy, tcapture_list)
        # linear checks (rook helpers)
        trval = RoR(board, pos, trval, enemy, tcapture_list)
        trval = RoL(board, pos, trval, enemy, tcapture_list)
        trval = RoU(board, pos, trval, enemy, tcapture_list)
        trval = RoD(board, pos, trval, enemy, tcapture_list)
        for i in trval:
            if i == pos-9 or i == pos-8 or i == pos-7 or i == pos-1 or i == pos+1 or i == pos+7 or i == pos+8 or i == pos+9:
                rval = rval + [i]
        for i in tcapture_list:
            if i == pos-9 or i == pos-8 or i == pos-7 or i == pos-1 or i == pos+1 or i == pos+7 or i == pos+8 or i == pos+9:
                capture_list.append(i)
    return rval


def RoR(board, pos, rval, e, capture_list):
    i = 1
    n1 = pos
    while (isREdge(board, n1) != 1):
        n1 = pos+i
        if board[n1] == 0:
            rval = rval + [n1]
        elif board[n1]-e >= 0 and board[n1]-e < 6:
            capture_list.append(n1)
            break
        else:
            break
        i = i + 1
    return rval


def RoL(board, pos, rval, e, capture_list):
    i = 1
    n2 = pos
    while (isLEdge(board, n2) != 1):
        n2 = pos-i
        if board[n2] == 0:
            rval = rval + [n2]
        elif board[n2]-e >= 0 and board[n2]-e < 6:
            capture_list.append(n2)
            break
        else:
            break
        i = i + 1
    return rval


def RoU(board, pos, rval, e, capture_list):
    i = 1
    n3 = pos
    while (isUEdge(board, n3) != 1):
        n3 = n3 + 8
        if board[n3] == 0:
            rval = rval + [n3]
        elif board[n3]-e >= 0 and board[n3]-e < 6:
            capture_list.append(n3)
            break
        else:
            break
        i = i + 1
    return rval


def RoD(board, pos, rval, e, capture_list):
    i = 1
    n4 = pos
    while (isBEdge(board, n4) != 1):
        n4 = n4 - 8
        if board[n4] == 0:
            rval = rval + [n4]
        elif board[n4]-e >= 0 and board[n4]-e < 6:
            capture_list.append(n4)
            break
        else:
            break
        i = i + 1
    return rval


def isBEdge(board, pos):
    rval = 0
    temp = [0, 1, 2, 3, 4, 5, 6, 7]
    for i in range(0, 8):
        if pos == temp[i]:
            rval = 1
    return rval


def isREdge(board, pos):
    rval = 0
    temp = [7, 15, 23, 31, 39, 47, 55, 63]
    for i in range(0, 8):
        if pos == temp[i]:
            rval = 1
    return rval


def isUEdge(board, pos):
    rval = 0
    temp = [63, 62, 61, 60, 59, 58, 57, 56]
    for i in range(0, 8):
        if pos == temp[i]:
            rval = 1
    return rval


def isLEdge(board, pos):
    rval = 0
    temp = [56, 48, 40, 32, 24, 16, 8, 0]
    for i in range(0, 8):
        if pos == temp[i]:
            rval = 1
    return rval


def BiUR(board, pos, rval, e, capture_list):
    i = 1
    n1 = pos
    while (isREdge(board, n1) != 1 and isUEdge(board, n1) != 1):
        n1 = pos+(9*i)
        if board[n1] == 0:
            rval = rval + [n1]
        elif board[n1]-e >= 0 and board[n1]-e < 6:
            capture_list.append(n1)
            break
        else:
            break
        i = i + 1
    return rval


def BiUL(board, pos, rval, e, capture_list):
    i = 1
    n2 = pos
    while (isUEdge(board, n2) != 1 and isLEdge(board, n2) != 1):
        n2 = pos+(7*i)
        if board[n2] == 0:
            rval = rval + [n2]
        elif board[n2]-e >= 0 and board[n2]-e < 6:
            capture_list.append(n2)
            break
        else:
            break
        i = i + 1
    return rval


def BiLL(board, pos, rval, e, capture_list):
    i = 1
    n3 = pos
    while (isLEdge(board, n3) != 1 and isBEdge(board, n3) != 1):
        n3 = pos+(-9*i)
        if board[n3] == 0:
            rval = rval + [n3]
        elif board[n3]-e >= 0 and board[n3]-e < 6:
            capture_list.append(n3)
            break
        else:
            break
        i = i + 1
    return rval


def BiLR(board, pos, rval, e, capture_list):
    i = 1
    n4 = pos
    while (isBEdge(board, n4) != 1 and isREdge(board, n4) != 1):
        n4 = pos+(-7*i)
        if board[n4] == 0:
            rval = rval + [n4]
        elif board[n4]-e >= 0 and board[n4]-e < 6:
            capture_list.append(n4)
            break
        else:
            break
        i = i + 1
    return rval


def isPositionUnderThreat(board, pos):
    if board[pos]-16 > 0:
        player = 20
        enemy = 10
    elif board[pos]-16 < 0 and board[pos]-16 > -7:
        player = 10
        enemy = 20
    else:
        "Empty Position cannot be under threat"
        return False
    for i in range(0, 64):
        cap = []
        if board[i]-enemy >= 0 and board[i]-enemy < 6:
            a = GetPieceLegalMoves(board, i, cap)
            for z in cap:
                if pos == z:
                    return True
    return False


def move(board, pos1, pos2):
    temp_board = board[:]
    tempo = temp_board[pos1]
    temp_board[pos1] = 0
    temp_board[pos2] = tempo
    return temp_board
