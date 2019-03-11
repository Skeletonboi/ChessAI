from random import randint
from tree import *


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


def chess():
    board = ini()
    fin = False
    while (fin is False):
        a = b = c = d = 0
        printBoard(board)
        p1 = input("Player White: Indicate Piece Position\n")
        temp1 = GetPlayerPositions(board, 10)
        for i in temp1:
            if p1 == i:
                a = 1
        if a == 0:
            print "Invalid White Piece Choice"
            break
        cap1 = []
        m1 = input("Player White: Indicate Move Position\n")
        no_cap1 = GetPieceLegalMoves(board, p1, cap1)
        moves1 = no_cap1 + cap1
        for i in moves1:
            if m1 == i:
                b = 1
        if b == 0:
            print "Invalid White Move Position"
            break
        board = move(board, p1, m1)
        p2 = input("Player Black: Indicate Piece\n")
        temp2 = GetPlayerPositions(board, 20)
        for i in temp2:
            if p2 == i:
                c = 1
        if c == 0:
            print "Invalid Black Piece Choice"
            break
        m2 = input("Player Black: Indicate Move Position\n")
        cap2 = []
        no_cap2 = GetPieceLegalMoves(board, p2, cap2)
        moves2 = no_cap2 + cap2
        for i in moves2:
            if m2 == i:
                d = 1
        if d == 0:
            print "Invalid White Move Position"
            break
        board = move(board, p2, m2)
    return True


def PVErand():
    board = ini()
    fin = False
    while (fin is False):
        a = b = c = d = 0
        printBoard(board)
        p1 = input("Player White: Indicate Piece Position\n")
        temp1 = GetPlayerPositions(board, 10)
        for i in temp1:
            if p1 == i:
                a = 1
        if a == 0:
            print "Invalid White Piece Choice"
            break
        m1 = input("Player White: Indicate Move Position\n")
        cap_p = []
        no_cap_p = GetPieceLegalMoves(board, p1, cap_p)
        moves1 = no_cap_p + cap_p
        for i in moves1:
            if m1 == i:
                b = 1
        if b == 0:
            print "Invalid White Move Position"
            break
        board = move(board, p1, m1)
        # BEGIN RANDOM AI LOGIC
        cap_ai = []
        moves_ai = []
        final_moves = []
        allcurrentpos = GetPlayerPositions(board, 20)
        for i in allcurrentpos:
            no_cap_ai = (GetPieceLegalMoves(board, i, cap_ai))
            moves_ai = no_cap_ai + cap_ai
            for z in moves_ai:
                if isPositionUnderThreat(board, z) is False:
                    final_moves.append([z, i])
        r = randint(0, len(final_moves))
        m2 = final_moves[r][0]
        p2 = final_moves[r][1]
        board = move(board, p2, m2)
    return True


def eval_board(board, player):
    # Setting Pawn Position Weights
    w_pawn_weight = [0,  0,  0,  0,  0,  0,  0,  0, 5, 10, 10, -20, -20, 10, 10,  5, 5, -5, -10,  0,  0, -10, -5,  5, 0,  0,  0, 20, 20,  0,
                     0,  0, 5,  5, 10, 25, 25, 10,  5,  5, 10, 10, 20, 30, 30, 20, 10, 10, 50, 50, 50, 50, 50, 50, 50, 50, 0,  0,  0,  0,  0,  0,  0,  0]
    b_pawn_weight = w_pawn_weight[::-1]
    # Setting Knight Position Weights
    w_knight_weight = [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20,  0,  5,  5,  0, -20, -40, -30,  5, 10, 15, 15, 10,  5, -30, -30,  0, 15, 20, 20, 15,
                       0, -30, -30,  5, 15, 20, 20, 15,  5, -30, -30,  0, 10, 15, 15, 10,  0, -30, -40, -20,  0,  0,  0,  0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50]
    b_knight_weight = w_knight_weight[::-1]
    # Setting Bishop Position Weights
    w_bishop_weight = [-20, -10, -10, -10, -10, -10, -10, -20, -10,  5,  0,  0,  0,  0,  5, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10,  0, 10, 10, 10, 10,
                       0, -10, -10,  5,  5, 10, 10,  5,  5, -10, -10,  0,  5, 10, 10,  5,  0, -10, -10,  0,  0,  0,  0,  0,  0, -10, -20, -10, -10, -10, -10, -10, -10, -20]
    b_bishop_weight = w_bishop_weight[::-1]
    # Setting Rooks Position Weights
    w_rook_weight = [0,  0,  0,  5,  5,  0,  0,  0, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,
                     0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5, 5, 10, 10, 10, 10, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0]
    b_rook_weight = w_rook_weight[::-1]
    # Setting Queen Positions Weights
    w_queen_weight = [-20, -10, -10, -5, -5, -10, -10, -20, -10,  0,  5,  0,  0,  0,  0, -10, -10,  5,  5,  5,  5,  5,  0, -10, 0,  0,  5,  5,  5,  5,
                      0, -5, -5,  0,  5,  5,  5,  5,  0, -5, -10,  0,  5,  5,  5,  5,  0, -10, -10,  0,  0,  0,  0,  0,  0, -10, -20, -10, -10, -5, -5, -10, -10, -20]
    b_queen_weight = w_queen_weight[::-1]
    # Setting King Position Weights
    w_king_weight = [20, 30, 10,  0,  0, 10, 30, 20, 20, 20,  0,  0,  0,  0, 20, 20, -10, -20, -20, -20, -20, -20, -20, -10, -20, -30, -30, -40, -40, -30, -30, -20, -
                     30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30]
    b_king_weight = w_king_weight[::-1]
    # EVALUATION
    w_pos = []
    b_pos = []
    w_score = 0
    b_score = 0
    for i in range(0, 64):
        if board[i] >= 10 and board[i] < 16:
            w_pos.append([i, board[i]])
        elif board[i] >= 20 and board[i] < 25:
            b_pos.append([i, board[i]])
    for i in w_pos:
        if i[1] == 10:
            w_score += w_pawn_weight[i[0]]
        elif i[1] == 11:
            w_score += w_knight_weight[i[0]]
        elif i[1] == 12:
            w_score += w_bishop_weight[i[0]]
        elif i[1] == 13:
            w_score += w_rook_weight[i[0]]
        elif i[1] == 14:
            w_score += w_queen_weight[i[0]]
        elif i[1] == 15:
            w_score += w_king_weight[i[0]]
    for q in b_pos:
        if q[1] == 20:
            b_score += b_pawn_weight[q[0]]
        elif q[1] == 21:
            b_score += b_knight_weight[q[0]]
        elif q[1] == 22:
            b_score += b_bishop_weight[q[0]]
        elif q[1] == 23:
            b_score += b_rook_weight[q[0]]
        elif q[1] == 24:
            b_score += b_queen_weight[q[0]]
        elif q[1] == 25:
            b_score += b_king_weight[q[0]]
    if player == 10:
        return w_score - b_score
    elif player == 20:
        return b_score - w_score


def chessPlayer(board, player):
    if player == 10:
        enemy = 20
    elif player == 20:
        enemy = 10
    x = tree(board)
    cap_ai = []
    allcurrentpos = GetPlayerPositions(board, player)
    temp_moves = []
    for i in allcurrentpos:
        no_cap_ai = (GetPieceLegalMoves(board, i, cap_ai))
        temp_moves = no_cap_ai + cap_ai
        for j in temp_moves:
            temp_board = move(board, i, j)
            tree_val = [temp_board, i, j]
            temp_child = tree(tree_val)
            x.AddSuccessor(temp_child)
            # Second Layer
            e_pos = GetPlayerPositions(temp_board, enemy)
            e_nocap = []
            e_cap = []
            for k in e_pos:
                e_nocap = GetPieceLegalMoves(temp_board, k, e_cap)
                e_moves = e_nocap + e_cap
                for r in e_moves:
                    e_board = move(temp_board, k, r)
                    e_tree_val = [e_board, k, r]
                    e_child = tree(e_tree_val)
                    temp_child.AddSuccessor(e_child)
    d = x.depth()
    alpha = 0
    beta = 0
    candy = []
    score_list = evalTree(x, d, alpha, beta, True, player, candy)
    final_move = [score_list[1], score_list[2]]
    return [True, final_move, candy, x]


def evalTree(tree, depth, alpha, beta, ismaximizing, player, candidateMoves):
    if tree.depth() == 0:
        temp_score = eval_board(tree.store[0][0], player)
        return temp_score
    if ismaximizing is True:
        temp_max = -9999
        for i in tree.store[1]:
            score = evalTree(i, depth-1, alpha, beta, False, player, candidateMoves)
            candidateMoves.append([[i.store[0][1], i.store[0][2]], score])
            temp_max = max(temp_max, score)
        return [temp_max, i.store[0][1], i.store[0][2]]
    elif ismaximizing is False:
        temp_min = 9999
        for i in tree.store[1]:
            score = evalTree(i, depth-1, alpha, beta, True, player, candidateMoves)
            if score < temp_min:
                temp_min = score
        return temp_min
# RETURN_DATA


x = ini()
print chessPlayer(x, 10)
