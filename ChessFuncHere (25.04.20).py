import numpy as np

#chboard = np.zeros((8, 8))
#chboard[6, 0], chboard[6, 1], chboard[6, 2], chboard[6, 3], chboard[6, 4], chboard[6, 5], chboard[6, 6], chboard[6, 7] = 1, 2, 3, 4, 5, 6, 7, 8
#chboard[7, 0], chboard[7, 1], chboard[7, 2], chboard[7, 3], chboard[7, 4], chboard[7, 5], chboard[7, 6], chboard[7, 7] = 15, 12, 13, 17, 18, 14, 11, 16
#chboard[1, 0], chboard[1, 1], chboard[1, 2], chboard[1, 3], chboard[1, 4], chboard[1, 5], chboard[1, 6], chboard[1, 7] = 21, 22, 23, 24, 25, 26, 27, 28
#chboard[0, 0], chboard[0, 1], chboard[0, 2], chboard[0, 3], chboard[0, 4], chboard[0, 5], chboard[0, 6], chboard[0, 7] = 35, 32, 34, 37, 38, 33, 31, 36
#print(chboard)


def uncaplist(chboard, turn):  # analyses the board for p1 pieces left, returns a list of p1 pieces left
    p1piecelist = list(range(1, 9)) + list(range(11, 19)) + list(range(101, 109)) + list(range(111, 119)) + list(
        range(121, 129)) + list(range(131, 139)) + [100]
    p2piecelist = list(range(21, 29)) + list(range(31, 39)) + list(range(201, 209)) + list(range(211, 219)) + list(
        range(221, 229)) + list(range(231, 239)) + [200]
    pieceremain = []
    if turn == 1:  # if player 1
        for rank in chboard:
            for file in rank:
                if file in p1piecelist:
                    pieceremain.append(file)
        return pieceremain
    if turn == 2:  # if player 2
        for rank in chboard:
            for file in rank:
                if file in p2piecelist:
                    pieceremain.append(file)
        return pieceremain


def piecelocator(chboard, pieceid):  # finds location of piece on the board, returns a list [rank,file]
    indexcount = 0
    for rank in chboard:
        for file in rank:
            if file == pieceid:
                y = indexcount // 8
                x = indexcount - ((indexcount // 8) * 8)
                return [y, x]
            indexcount += 1
    return [99, 99]  # piece do not exist


def piecetypelist(turn, piecetype):  # lists all possible pieceid for player's piecetype
    if turn == 1:
        if piecetype == 'pawn':
            return list(range(1, 9))
        elif piecetype == 'knight':
            return [11, 12] + list(range(101, 109))
        elif piecetype == 'bishop':
            return [13, 14] + list(range(111, 119))
        elif piecetype == 'rook':
            return [15, 16] + list(range(121, 129))
        elif piecetype == 'queen':
            return [17] + list(range(131, 139))
        elif piecetype == 'king':
            return [18]
        elif piecetype == 'all':
            return list(range(1, 9)) + list(range(11, 19)) + list(range(101, 109)) + list(range(111, 119)) + list(
                range(121, 129)) + list(range(131, 139)) + [100]
        else:
            return [999]  # error: invalid piecetype
    if turn == 2:
        if piecetype == 'pawn':
            return list(range(21, 29))
        elif piecetype == 'knight':
            return [31, 32] + list(range(201, 209))
        elif piecetype == 'bishop':
            return [33, 34] + list(range(211, 219))
        elif piecetype == 'rook':
            return [35, 36] + list(range(221, 229))
        elif piecetype == 'queen':
            return [37] + list(range(231, 239))
        elif piecetype == 'king':
            return [38]
        elif piecetype == 'all':
            return list(range(21, 29)) + list(range(31, 39)) + list(range(201, 209)) + list(range(211, 219)) + list(
                range(221, 229)) + list(range(231, 239)) + [200]
        else:
            return [999]  # error: invalid piecetype
    else:
        return [999]  # error: not turn 1 or 2


def pieceidentifier(pieceid):  # Identifies the piecetype from pieceid input
    if pieceid in piecetypelist(1, 'pawn'):
        return 10
    elif pieceid in piecetypelist(1, 'knight'):
        return 11
    elif pieceid in piecetypelist(1, 'bishop'):
        return 12
    elif pieceid in piecetypelist(1, 'rook'):
        return 13
    elif pieceid in piecetypelist(1, 'queen'):
        return 14
    elif pieceid in piecetypelist(1, 'king'):
        return 15
    elif pieceid in piecetypelist(2, 'pawn'):
        return 20
    elif pieceid in piecetypelist(2, 'knight'):
        return 21
    elif pieceid in piecetypelist(2, 'bishop'):
        return 22
    elif pieceid in piecetypelist(2, 'rook'):
        return 23
    elif pieceid in piecetypelist(2, 'queen'):
        return 24
    elif pieceid in piecetypelist(2, 'king'):
        return 25
    else:
        return 99  # invalid pieceid


def p2pawncheckmove(chboard, pieceid, rank, file, movehistlist):  # determine if P1pawn can move or capture or NONE, returns True/False
    pawnlist, pawnpos, pawn1list, pawn1mcount = list(range(21, 29)), piecelocator(chboard, pieceid), list(range(1, 9)), 0  # pawn1mcount = player 1 pawn move-counter
    if pieceid in pawnlist:
        if (0 <= rank <= 7) and (0 <= file <= 7):

            #### EN-PASSANT SCENARIO ####
            if len(movehistlist) != 0:
                p1epcaptured = movehistlist[len(movehistlist) - 1]  # Potential En-Passe Captured pawn moveset
                if p1epcaptured[0] in pawn1list:  # condition: Must be player 1 pawn ####
                    for moveset in movehistlist:
                        if moveset[0] == p1epcaptured[0]:
                            pawn1mcount += 1
                    if pawn1mcount == 1:  # condition: Must be first move of player 1 pawn ####
                        if p1epcaptured[2] == 4:  # condition: Must be two square movement (rank 6 to rank 4)  ####
                            pieceidpos = piecelocator(chboard, pieceid)
                            if ((pieceidpos[1] - p1epcaptured[3]) == 1) or ((pieceidpos[1] - p1epcaptured[3]) == -1):  # condition: player 1 pawn must be right beside player 2's pawn
                                if chboard[p1epcaptured[2] + 1][p1epcaptured[3]] == 0:  # condition: enpasse position must be unoccupied
                                    if ((p1epcaptured[2] + 1) == rank) and (p1epcaptured[3] == file):  # If rank & file input matches the allowed en-passe coordinates
                                        return [True, 'ep']

            if 0 > (pawnpos[0] + 1) > 7:  # Check if pawn can move forward
                return [False, 'n']  # Cannot move forward anymore, no point determining move or capture
            else:
                if pawnpos[0] == 1:
                    vertf = [[pawnpos[0] + 1, pawnpos[1]], [pawnpos[0] + 2, pawnpos[1]]]
                else:
                    vertf = [[pawnpos[0] + 1, pawnpos[1]], [99, 99]]

            if 0 > (pawnpos[1] - 1) > 7:  # Check if RDIAG is possible
                print('Error: Invalid move')
                rdiagf = None
            else:
                rdiagf = [[pawnpos[0] + 1, pawnpos[1] + 1]]

            if 0 > (pawnpos[1] + 1) > 7:
                print('Error: Invalid move')  # Check if LDIAG is possible
                ldiagf = None
            else:
                ldiagf = [[pawnpos[0] + 1, pawnpos[1] - 1]]

            for i in vertf:
                if i == [rank, file]:
                    if chboard[rank, file] == 0:  # MOVE, NEED 0 TO MOVE
                        return [True, 'n']
            for i in rdiagf:
                if i == [rank, file]:
                    if (chboard[rank, file] not in piecetypelist(2, 'all')) and (chboard[rank, file] != 0) :  # CAPTURE
                        return [True, 'n']
            for i in ldiagf:
                if i == [rank, file]:
                    if chboard[rank, file] not in piecetypelist(2, 'all') and (chboard[rank, file] != 0):  # CAPTURE
                        return [True, 'n']

            return [False, 'n']  # vertf,rdiagf,ldiagf do not exist
        else:
            return [False, 'n']  # rank/turn inout out of range
    else:
        return [False, 'n']  # pieceid not in pawnlist


def p1pawncheckmove(chboard, pieceid, rank, file, movehistlist):  # determine if P1pawn can move or capture or NONE, returns True/False
    pawnlist, pawnpos, pawn2list, pawn2mcount = list(range(1, 9)), piecelocator(chboard, pieceid), list(
        range(21, 29)), 0  # pawn2mcount = player 2 pawn move-counter
    if pieceid in pawnlist:
        if (0 <= rank <= 7) and (0 <= file <= 7):

            #### EN-PASSANT SCENARIO ####
            if len(movehistlist) != 0:
                p2epcaptured = movehistlist[len(movehistlist) - 1]  # Potential En-Passe Captured pawn moveset
                if p2epcaptured[0] in pawn2list:  # condition: Must be player 2 pawn ####
                    for moveset in movehistlist:
                        if moveset[0] == p2epcaptured[0]:
                            pawn2mcount += 1
                        if pawn2mcount == 1:  # condition: Must be first move of player 2 pawn ####
                            if p2epcaptured[2] == 3:  # condition: Must be two square movement (rank 1 to rank 3)  ####
                                pieceidpos = piecelocator(chboard, pieceid)
                                if ((pieceidpos[1] - p2epcaptured[3]) == 1) or ((pieceidpos[1] - p2epcaptured[
                                    3]) == -1):  # condition: player 1 pawn must be right beside player 2's pawn
                                    if chboard[p2epcaptured[2] - 1][p2epcaptured[3]] == 0:  # condition: enpasse position must be unoccupied
                                        if ((p2epcaptured[2] - 1) == rank) and (p2epcaptured[
                                                                                    3] == file):  # If rank & file input matches the allowed en-passe coordinates
                                            return [True, 'ep']

            #### MAIN PAWN MOVEMENT/CAPTURE FUNCTIONS ####                    
            if 0 > (pawnpos[0] - 1) > 7:  # Check if pawn can move forward
                return [False, 'n']  # Cannot move forward anymore, no point determining move or capture
            else:
                if pawnpos[0] == 6:
                    vertf = [[pawnpos[0] - 1, pawnpos[1]], [pawnpos[0] - 2, pawnpos[1]]]
                else:
                    vertf = [[pawnpos[0] - 1, pawnpos[1]], [99, 99]]

            if 0 > (pawnpos[1] - 1) > 7:  # Check if RDIAG is possible
                print('Error: Invalid move')
                rdiagf = None
            else:
                rdiagf = [[pawnpos[0] - 1, pawnpos[1] + 1]]

            if 0 > (pawnpos[1] + 1) > 7:
                print('Error: Invalid move')  # Check if LDIAG is possible
                ldiagf = None
            else:
                ldiagf = [[pawnpos[0] - 1, pawnpos[1] - 1]]

            for i in vertf:
                if i == [rank, file]:
                    if chboard[rank, file] == 0:  # MOVE  DONT HAVE TO BE 0 TO MOVE
                        return [True, 'n']
            for i in rdiagf:
                if i == [rank, file]:
                    if (chboard[rank, file] not in piecetypelist(1, 'all')) and (chboard[rank, file] != 0):  # MOVE
                        return [True, 'n']
            for i in ldiagf:
                if i == [rank, file]:
                    if (chboard[rank, file] not in piecetypelist(1, 'all')) and (chboard[rank, file] != 0):  # MOVE
                        return [True, 'n']

            return [False, 'n']  # vertf,rdiagf,ldiagf do not exist
        else:
            return [False, 'n']  # rank/turn inout out of range
    else:
        return [False, 'n']  # pieceid not in pawnlist


def pawncheckmove(chboard, turn, pieceid, rank, file, movehistlist):  # CORE PAWN MOVEMENT/CAPTURE FUNCTION, returns [True/False,ep/p/n]
    if turn == 1:
        if (p1pawncheckmove(chboard, pieceid, rank, file, movehistlist)[0]) and (
                p1pawncheckmove(chboard, pieceid, rank, file, movehistlist)[1] == 'ep'):  # EN-PASSANT!
            return [True, 'ep']
        elif p1pawncheckmove(chboard, pieceid, rank, file, movehistlist)[0]:
            if rank == 0:  # PROMOTION!
                return [True, 'p']
            else:  #
                return [True, 'n']
        else:
            return [p1pawncheckmove(chboard, pieceid, rank, file, movehistlist)[0], 'n']
    elif turn == 2:
        if (p2pawncheckmove(chboard, pieceid, rank, file, movehistlist)[0]) and (
                p2pawncheckmove(chboard, pieceid, rank, file, movehistlist)[1] == 'ep'):  # EN-PASSANT!
            return [True, 'ep']
        elif p2pawncheckmove(chboard, pieceid, rank, file, movehistlist)[0]:
            if rank == 7:  # PROMOTION!
                return [True, 'p']
            else:  #
                return [True, 'n']
        else:
            return [p2pawncheckmove(chboard, pieceid, rank, file, movehistlist)[0], 'n']


def pawnpromote(chboard, rank, file, pmtdpieceid):  # promotion of pawn piece to the piece of choice, Inputs old (pawn) and new piece ID, Outputs nothing
    chboard[rank, file] = pmtdpieceid
    return


def promotecheck(chboard, turn, pmtdpieceid):  # checks if pmtdpieceid of pawn is eligible to promote with ref. to board
    if turn == 1:
        if (pmtdpieceid in piecetypelist(1, 'all')) and (pmtdpieceid not in uncaplist(chboard, 1)):
            return True
        else:
            return False
    elif turn == 2:
        if (pmtdpieceid in piecetypelist(2, 'all')) and (pmtdpieceid not in uncaplist(chboard, 2)):
            return True
        else:
            return False
    else:
        return False


# ##### NOTE TO SELF ###### Run a pawncheckmove before applypawnmove to check if piece can promote, if so,
# ask player which piece to be promoted to

def applypawnmove(chboard, turn, pieceid, pmtdpieceid, rank, file, movehistlist):  # moves pawn piece on chboard to index [rank,file], if promoted, promote
    checkresult = pawncheckmove(chboard, turn, pieceid, rank, file, movehistlist)
    if checkresult[0] == True:  # pawnmove is valid, make pawn move
        if checkresult[1] == 'ep':  # pawn does en-passant
            if turn == 1:
                for r in range(0, 8):
                    for f in range(0, 8):
                        if pieceid == chboard[r, f]:
                            chboard[r, f] = 0  # remove pawn from old position
                chboard[rank, file] = pieceid  # put pawn in new position
                chboard[(rank + 1), file] = 0  # remove captured pawn
                return chboard
            elif turn == 2:
                for r in range(0, 8):
                    for f in range(0, 8):
                        if pieceid == chboard[r, f]:
                            chboard[r, f] = 0  # remove pawn from old position
                chboard[rank, file] = pieceid  # put pawn in new position
                chboard[(rank - 1), file] = 0  # remove captured pawn
                return chboard

        elif checkresult[1] == 'p':  # pawn must promote
            if promotecheck(chboard, turn, pmtdpieceid) == True:
                for r in range(0, 8):
                    for f in range(0, 8):
                        if pieceid == chboard[r, f]:
                            chboard[r, f] = 0  # remove pawn from old position
                chboard[rank, file] = pieceid  # put pawn in new position
                pawnpromote(chboard, rank, file, pmtdpieceid)  # promote pawn
                return chboard
            else:
                return chboard

        else:  # No promotion, just move/capture
            for r in range(0, 8):
                for f in range(0, 8):
                    if pieceid == chboard[r, f]:
                        chboard[r, f] = 0  # remove pawn from old position
            chboard[rank, file] = pieceid  # put pawn in new position
            return chboard
    else:
        return chboard  # Error: Move is invalid


def knightcheckmove(chboard, turn, pieceid, rank, file):  # Checks validity of rank & file of knight movement/capture
    p2knightlist, p1knightlist = list(range(31, 33)) + list(range(201, 209)), list(range(11, 13)) + list(
        range(101, 109))
    knightloc = piecelocator(chboard, pieceid)
    if (pieceid in p1knightlist) or (pieceid in p2knightlist):
        if (0 <= rank <= 7) and (0 <= file <= 7):  # within index of the board
            if abs(abs(rank) - abs(knightloc[0])) == 2:  # 2 RANKS, 1 FILE
                if abs(abs(file) - abs(knightloc[1])) == 1:
                    if turn == 1:  # P2 bishop captures P1 bishop
                        if pieceid in p1knightlist:
                            if chboard[rank, file] == 0:
                                return True
                            elif chboard[rank, file] in uncaplist(chboard, 2):
                                return True
                            else:
                                return False
                    elif turn == 2:  # P1 bistop capture P2 bishop
                        if pieceid in p2knightlist:
                            if chboard[rank, file] == 0:
                                return True
                            elif chboard[rank, file] in uncaplist(chboard, 1):
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False

            elif abs(abs(rank) - abs(knightloc[0])) == 1:  # 1 RANKS, 2 FILE
                if abs(abs(file) - abs(knightloc[1])) == 2:
                    if turn == 1:  # P2 bishop captures P1 bishop
                        if pieceid in p1knightlist:
                            if chboard[rank, file] == 0:
                                return True
                            elif chboard[rank, file] in uncaplist(chboard, 2):
                                return True
                            else:
                                return False
                    elif turn == 2:  # P1 bistop capture P2 bishop
                        if pieceid in p2knightlist:
                            if chboard[rank, file] == 0:
                                return True
                            elif chboard[rank, file] in uncaplist(chboard, 1):
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def applyknightmove(chboard, turn, pieceid, rank, file):  # Knight piece on chboard moves to / capture the index [rank,file]
    if knightcheckmove(chboard, turn, pieceid, rank, file):
        chboard[piecelocator(chboard, pieceid)[0], piecelocator(chboard, pieceid)[1]] = 0
        chboard[rank, file] = pieceid
        return chboard
    else:
        return chboard


def bishopcheckmove(chboard, turn, pieceid, rank, file):  # Checks validity of rank & file of bishop movement/capture
    p2bishoplist, p1bishoplist = list(range(33, 35)) + list(range(211, 219)), list(range(13, 15)) + list(
        range(111, 119))
    bishoploc, between, rindex, findex = piecelocator(chboard, pieceid), [], 0, 0
    if (pieceid in p1bishoplist) or (pieceid in p2bishoplist):  # condition: this function applies to only bishop pieces
        if (0 <= rank <= 7) and (0 <= file <= 7):  # condition: within index of the board
            if abs((bishoploc[0]) - rank) == abs(bishoploc[1] - file):  # condition: rank/file index diagonal

                # Create 'between' list containing positions in between current piece and selected rank/file
                if abs((bishoploc[0]) - rank) >= 1:  # if 'inbetween' has 1 or more positions

                    for inbetween in list(
                            range(abs((bishoploc[0]) - rank) - 1)):  # number of 'inbetween' positions is [n-1]
                        if (bishoploc[0] - rank) > 0:  # goes up (pos result)(+1) #
                            rindex -= 1
                        else:  # goes down (neg result)(-1) #
                            rindex += 1
                        between.append([(bishoploc[0]) + rindex])

                        if (bishoploc[1] - file) > 0:  # goes left (pos result)(+1) #
                            findex -= 1
                        else:  # goes right (neg result)(-1) #
                            findex += 1
                        between[inbetween].insert(1, (bishoploc[1]) + findex)

                    for bcoord in between:  # condition: cannot skip over a player's piece
                        if chboard[bcoord[0], bcoord[1]] != 0:
                            return False

                if turn == 1:  # condition: cannot capture friendly piece
                    if pieceid in p1bishoplist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return True
                        elif chboard[rank, file] in uncaplist(chboard, 2):  # opponent piece occupied on the board
                            return True
                        else:
                            return False  # Error: friendly piece
                    else:
                        return False  # Error: not p1 bishop piece
                elif turn == 2:
                    if pieceid in p2bishoplist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return True
                        elif chboard[rank, file] in uncaplist(chboard, 1):  # opponent piece occupied on the board
                            return True
                        else:
                            return False  # Error: friendly piece
                    else:
                        return False  # Error: not p2 bishop piece
                else:
                    return False  # Error: not turn 1 or 2
            else:
                return False  # Error: not diagonal
        else:
            return False  # Error: index out of range
    else:
        return False  # Error: pieceid not bishop piece


def applybishopmove(chboard, turn, pieceid, rank, file):  # Bishop piece on chboard moves to / capture the index [rank,file]
    if bishopcheckmove(chboard, turn, pieceid, rank, file):
        chboard[piecelocator(chboard, pieceid)[0], piecelocator(chboard, pieceid)[1]] = 0
        chboard[rank, file] = pieceid
        return chboard
    else:
        return chboard  # if move is not valid, returns unchanged chboard


def rookcheckmove(chboard, turn, pieceid, rank, file):  # Checks validity of rank & file of rook movement/capture
    p2rooklist, p1rooklist = list(range(35, 37)) + list(range(221, 229)), list(range(15, 17)) + list(range(121, 129))
    rookloc, between, rindex, findex = piecelocator(chboard, pieceid), [], 0, 0
    if (pieceid in p1rooklist) or (pieceid in p2rooklist):  # condition: this function applies to only rook pieces
        if (0 <= rank <= 7) and (0 <= file <= 7):  # condition: within index of the board
            if (((abs(rookloc[0] - rank)) != 0) and ((abs(rookloc[1] - file)) == 0)) or (
                    ((abs(rookloc[0] - rank)) == 0) and ((abs(rookloc[1] - file)) != 0)):

                # Create 'between' list containing positions in between current piece and selected rank/file
                if abs(rookloc[0] - rank) >= 1:  # if 'inbetween' has 1 or more positions
                    for inbetween in list(
                            range(abs((rookloc[0]) - rank) - 1)):  # number of 'inbetween' positions is [n-1]
                        if (rookloc[0] - rank) > 0:  # goes up (pos result)(+1) #
                            rindex -= 1
                        else:  # goes down (neg result)(-1) #
                            rindex += 1
                        between.append([(rookloc[0]) + rindex])
                        between[inbetween].insert(1, (rookloc[1]) + findex)

                elif abs(rookloc[1] - file) >= 1:  # if 'inbetween' has 1 or more positions
                    for inbetween in list(
                            range(abs((rookloc[1]) - file) - 1)):  # number of 'inbetween' positions is [n-1]
                        if (rookloc[1] - file) > 0:  # goes up (pos result)(+1) #
                            findex -= 1
                        else:  # goes down (neg result)(-1) #
                            findex += 1
                        between.append([(rookloc[0]) + rindex])
                        between[inbetween].insert(1, (rookloc[1]) + findex)
                for bcoord in between:  # condition: cannot skip over a player's piece
                    if chboard[bcoord[0], bcoord[1]] != 0:
                        return False  # Error: skip over player's piece

                if turn == 1:  # condition: cannot capture friendly piece
                    if pieceid in p1rooklist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return True
                        elif chboard[rank, file] in uncaplist(chboard, 2):  # opponent piece occupied on the board
                            return True
                        else:
                            return False  # Error: friendly piece
                    else:
                        return False  # Error: not p1 rook piece
                elif turn == 2:
                    if pieceid in p2rooklist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return True
                        elif chboard[rank, file] in uncaplist(chboard, 1):  # opponent piece occupied on the board
                            return True
                        else:
                            return False  # Error: friendly piece
                    else:
                        return False  # Error: not p2 rook piece
                else:
                    return False  # Error: not turn 1 or 2
            else:
                return False  # Error: not horizontal or vertical movement
        else:
            return False  # Error: index out of range
    else:
        return False  # Error: pieceid not rook piece


def applyrookmove(chboard, turn, pieceid, rank, file):  # Rook piece on chboard moves to / capture the index [rank,file]
    if rookcheckmove(chboard, turn, pieceid, rank, file):
        chboard[piecelocator(chboard, pieceid)[0], piecelocator(chboard, pieceid)[1]] = 0
        chboard[rank, file] = pieceid
        return chboard
    else:
        return chboard  # if move is not valid, returns unchanged chboard


def queencheckmove(chboard, turn, pieceid, rank, file):  # Checks validity of rank & file of queen movement/capture
    p2queenlist, p1queenlist = [37] + list(range(231, 239)), [17] + list(range(131, 139))
    queenloc, between, rindex, findex = piecelocator(chboard, pieceid), [], 0, 0
    if (pieceid in p1queenlist) or (pieceid in p2queenlist):  # condition: this function applies to only queen pieces
        if (0 <= rank <= 7) and (0 <= file <= 7):
            if (((abs(queenloc[0] - rank)) != 0) and ((abs(queenloc[1] - file)) == 0)) or (
                    ((abs(queenloc[0] - rank)) == 0) and ((abs(queenloc[1] - file)) != 0)) or (
                    abs((queenloc[0]) - rank) == abs(queenloc[1] - file)):  # Condition:
                # Vertical/Horizontal/Diagonal movement

                # Create 'between' list containing positions in between current piece and selected rank/file
                if (((abs(queenloc[0] - rank)) != 0) and ((abs(queenloc[1] - file)) == 0)) or (
                        ((abs(queenloc[0] - rank)) == 0) and (
                        (abs(queenloc[1] - file)) != 0)):  ## VERTICAL/HORIZONTAL MOVEMENT ##
                    if abs(queenloc[0] - rank) >= 1:  # if 'inbetween' has 1 or more positions
                        for inbetween in list(
                                range(abs((queenloc[0]) - rank) - 1)):  # number of 'inbetween' positions is [n-1]
                            if (queenloc[0] - rank) > 0:  # goes up (pos result)(+1) #
                                rindex -= 1
                            else:  # goes down (neg result)(-1) #
                                rindex += 1
                            between.append([(queenloc[0]) + rindex])
                            between[inbetween].insert(1, (queenloc[1]) + findex)

                    elif abs(queenloc[1] - file) >= 1:  # if 'inbetween' has 1 or more positions
                        for inbetween in list(
                                range(abs((queenloc[1]) - file) - 1)):  # number of 'inbetween' positions is [n-1]
                            if (queenloc[1] - file) > 0:  # goes up (pos result)(+1) #
                                findex -= 1
                            else:  # goes down (neg result)(-1) #
                                findex += 1
                            between.append([(queenloc[0]) + rindex])
                            between[inbetween].insert(1, (queenloc[1]) + findex)

                elif (abs((queenloc[0]) - rank) == abs(queenloc[1] - file)):  ## DIAGONAL MOVEMENT ##
                    for inbetween in list(range(abs((queenloc[0]) - rank) - 1)):  # number of 'inbetween' positions is [n-1]
                        if (queenloc[0] - rank) > 0:  # goes up (pos result)(+1) #
                            rindex -= 1
                        else:  # goes down (neg result)(-1) #
                            rindex += 1
                        between.append([(queenloc[0]) + rindex])

                        if (queenloc[1] - file) > 0:  # goes left (pos result)(+1) #
                            findex -= 1
                        else:  # goes right (neg result)(-1) #
                            findex += 1
                        between[inbetween].insert(1, (queenloc[1]) + findex)

                for bcoord in between:  # condition: cannot skip over a player's piece
                    if chboard[bcoord[0], bcoord[1]] != 0:
                        return False  # Error: skip over player's piece

                if turn == 1:  # condition: cannot capture friendly piece
                    if pieceid in p1queenlist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return True
                        elif chboard[rank, file] in uncaplist(chboard, 2):  # opponent piece occupied on the board
                            return True
                        else:
                            return False  # Error: friendly piece
                    else:
                        return False  # Error: not p1 rook piece
                elif turn == 2:
                    if pieceid in p2queenlist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return True
                        elif chboard[rank, file] in uncaplist(chboard, 1):  # opponent piece occupied on the board
                            return True
                        else:
                            return False  # Error: friendly piece
                    else:
                        return False  # Error: not p2 queen piece
                else:
                    return False  # Error: not turn 1 or 2
            else:
                return False  # Error: not horizontal or vertical movement
        else:
            return False  # Error: index out of range
    else:
        return False  # Error: pieceid not queen piece


def applyqueenmove(chboard, turn, pieceid, rank, file):  # Queen piece on chboard moves to / capture the index [rank,file]
    if queencheckmove(chboard, turn, pieceid, rank, file):
        chboard[piecelocator(chboard, pieceid)[0], piecelocator(chboard, pieceid)[1]] = 0
        chboard[rank, file] = pieceid
        return chboard
    else:
        return chboard  # if move is not valid, returns unchanged chboard


def kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist):  # PRECHECKS validity of rank & file of king movement/capture
    p2kinglist, p1kinglist = [38], [18]
    kingloc, between, rindex, findex = piecelocator(chboard, pieceid), [], 0, 0
    firstkmovecheck, firstrmovecheck, between = 0, 0, []
    if (pieceid in p1kinglist) or (pieceid in p2kinglist):  # condition: this function applies to only king pieces
        if (0 <= rank <= 7) and (0 <= file <= 7):

            #### MOVEMENT/CAPTURE ####        
            if ((abs(kingloc[0] - rank) == 1) and (abs(kingloc[1] - file) == 0)) or (abs(kingloc[0] - rank) == 0) and (
                    abs(kingloc[1] - file) == 1) or (abs((kingloc[0]) - rank) == abs((kingloc[1] - file)) and (
                    (abs((kingloc[0]) - rank) - 1) == 0)):  # Condition: move hori/vert/diag one square

                if turn == 1:  # condition: cannot capture friendly piece
                    if pieceid in p1kinglist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return [True, 'n']
                        elif chboard[rank, file] in uncaplist(chboard, 2):  # opponent piece occupied on the board
                            return [True, 'n']
                        else:
                            return [False, 'n']  # Error: friendly piece
                    else:
                        return [False, 'n']  # Error: not p1 rook piece

                elif turn == 2:
                    if pieceid in p2kinglist:
                        if chboard[rank, file] == 0:  # unoccupied position on the board
                            return [True, 'n']
                        elif chboard[rank, file] in uncaplist(chboard, 1):  # opponent piece occupied on the board
                            return [True, 'n']
                        else:
                            return [False, 'n']  # Error: friendly piece
                    else:
                        return [False, 'n']  # Error: not p2 rook piece
                else:
                    return [False, 'n']  # Error: not turn 1 or 2

            #### CASTLING ####
            if turn == 1:
                if rank != 7:  # turn 1 exists only in rank 7
                    return [False, 'n']
                for kmoves in movehistlist:  # check if king's first move
                    if (piecetypelist(1, 'king') in kmoves):
                        firstkmovecheck = 1
                        break
                if firstkmovecheck == 0:
                    if ([kingloc[0], kingloc[1] + 2] == [rank, file]):  # KING-SIDE Castle
                        for rmoves in movehistlist:  # check if king-side rook's first move
                            if 16 in rmoves:
                                return [False, 'n']

                        for ks1file in list(range(kingloc[1] + 1, kingloc[1] + 3)):
                            between.append([rank, ks1file])
                        for i in between:  # check for pieces in between
                            if chboard[i[0], i[1]] != 0:
                                return [False, 'n']
                        return [True, 'ksc']  # Castle true when between all zeros

                    elif ([kingloc[0], kingloc[1] - 2] == [rank, file]):  # QUEEN-SIDE Castle
                        for rmoves in movehistlist:  # check if king-side rook's first move
                            if 15 in rmoves:
                                return [False, 'n']

                        for qs1file in list(range(kingloc[1] - 3, kingloc[1])):
                            between.append([rank, qs1file])
                        for i in between:  # check for pieces in between
                            if chboard[i[0], i[1]] != 0:
                                return [False, 'n']
                        return [True, 'qsc']  # Castle true when between all zeros

            elif turn == 2:
                if rank != 0:  # turn 2 exists only in rank 0
                    return [False, 'n']
                for kmoves in movehistlist:  # check if king's first move
                    if (piecetypelist(2, 'king') in kmoves):
                        firstkmovecheck = 1
                        break
                if firstkmovecheck == 0:
                    if ([kingloc[0], kingloc[1] + 2] == [rank, file]):  # KING-SIDE Castle
                        for rmoves in movehistlist:  # check if king-side rook's first move
                            if 36 in rmoves:
                                return [False, 'n']

                        for ks2file in list(range(kingloc[1] + 1, kingloc[1] + 3)):
                            between.append([rank, ks2file])
                        for i in between:  # check for pieces in between
                            if chboard[i[0], i[1]] != 0:
                                return [False, 'n']
                        return [True, 'ksc']  # Castle true when between all zeros

                    elif ([kingloc[0], kingloc[1] - 2] == [rank, file]):  # QUEEN-SIDE Castle
                        for rmoves in movehistlist:  # check if king-side rook's first move
                            if 35 in rmoves:
                                return [False, 'n']

                        for qs2file in list(range(kingloc[1] - 3, kingloc[1])):
                            between.append([rank, qs2file])
                        for i in between:  # check for pieces in between
                            if chboard[i[0], i[1]] != 0:
                                return [False, 'n']
                        return [True, 'qsc']  # Castle true when between all zeros

            else:
                return [False, 'n']  # Error: not hori/vert/diag one square movement
        else:
            return [False, 'n']  # Error: index out of range
    else:
        return [False, 'n']  # Error: pieceid not king piece


def kingcheckmove(chboard, turn, pieceid, rank, file, movehistlist):  # CHECKS for 'check' & 'checkmate' conditions, determines validity of king movement/capture
    kschboard = cloneboard(chboard)  # kscboard stands for 'King Simulation CHess Board'
    kingloc = piecelocator(kschboard, pieceid)  # king piece's rank/file index
    p2pieces, p1pieces = uncaplist(kschboard, 2), uncaplist(kschboard, 1)
    castleside = 'o'

    if kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True,
                                                                              'n']:  # Condition: valid rank/file movement index
        kschboard[rank, file], kschboard[kingloc[0], kingloc[1]] = pieceid, 0  # move king piece on kschboard

        if turn == 1:  # Simulate P2 piece movement, see if can capture P1 King
            for piece in p2pieces:
                kschboard = cloneboard(chboard)
                kschboard[rank, file], kschboard[kingloc[0], kingloc[1]] = pieceid, 0

                if piece in piecetypelist(turn + 1, 'pawn'):  ## PAWN PIECE ##
                    applypawnmove(kschboard, 2, piece, 200, rank, file, movehistlist)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'knight'):  # KNIGHT PIECE #
                    applyknightmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'bishop'):  # BISHOP PIECE #
                    applybishopmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'rook'):  # ROOK PIECE #
                    applyrookmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'queen'):  # QUEEN PIECE #
                    applyqueenmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'king'):  # KING PIECE #
                    if kingprecheckmove(kschboard, turn + 1, piece, rank, file, movehistlist) == True:
                        kschboard[piecelocator(kschboard, piece)[0], piecelocator(kschboard, piece)[1]] = 0
                        kschboard[rank, file] = piece
                        if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                            return [False, 'n']
            return [True, 'n']  # no P2 piece can capture P1 King

        if turn == 2:  # Simulate P1 piece movement, see if can capture P2 King
            for piece in p1pieces:
                kschboard = cloneboard(chboard)
                kschboard[rank, file], kschboard[kingloc[0], kingloc[1]] = pieceid, 0

                if piece in piecetypelist(turn - 1, 'pawn'):  ## PAWN PIECE ##
                    applypawnmove(kschboard, 1, piece, 100, rank, file, movehistlist)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'knight'):  # KNIGHT PIECE #
                    applyknightmove(kschboard, 1, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'bishop'):  # BISHOP PIECE #
                    applybishopmove(kschboard, 1, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'rook'):  # ROOK PIECE #
                    applyrookmove(kschboard, 1, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'queen'):  # QUEEN PIECE #
                    applyqueenmove(kschboard, 1, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'king'):  # KING PIECE #
                    if kingprecheckmove(kschboard, turn - 1, piece, rank, file, movehistlist) == True:
                        kschboard[piecelocator(kschboard, piece)[0], piecelocator(kschboard, piece)[1]] = 0
                        kschboard[rank, file] = piece
                        if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                            return [False, 'n']
            return [True, 'n']  # no P2 piece can capture P1 King
        else:
            return False  # Error: not turn 1 or 2

    elif (kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True, 'ksc']) or (kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True,'qsc']):
        # Condition: valid rank/file movement index

        if turn == 1:  # P1 CASTLE
            for piece in p2pieces:
                if kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True,
                                                                                          'ksc']:  # P1 KING-SIDE CASTLE
                    kschboard, castleside = cloneboard(chboard), 'k'
                    kschboard[rank, file], kschboard[kingloc[0], kingloc[1]] = pieceid, 0
                    kschboard[piecelocator(kschboard, 16)[0], piecelocator(kschboard, 16)[1]], kschboard[
                        rank, file - 1] = 0, 16
                elif kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True,
                                                                                            'qsc']:  # P1 KING-SIDE CASTLE
                    kschboard, castleside = cloneboard(chboard), 'q'
                    kschboard[rank, file], kschboard[kingloc[0], kingloc[1]] = pieceid, 0
                    kschboard[piecelocator(kschboard, 15)[0], piecelocator(kschboard, 15)[1]], kschboard[
                        rank, file + 1] = 0, 15

                if piece in piecetypelist(turn + 1, 'pawn'):  ## PAWN PIECE ##
                    applypawnmove(kschboard, 2, piece, 200, rank, file, movehistlist)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'knight'):  # KNIGHT PIECE #
                    applyknightmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'bishop'):  # BISHOP PIECE #
                    applybishopmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'rook'):  # ROOK PIECE #
                    applyrookmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'queen'):  # QUEEN PIECE #
                    applyqueenmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn + 1, 'king'):  # KING PIECE #
                    if kingprecheckmove(kschboard, turn + 1, piece, rank, file, movehistlist) == True:
                        kschboard[piecelocator(kschboard, piece)[0], piecelocator(kschboard, piece)[1]] = 0
                        kschboard[rank, file] = piece
                        if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                            return [False, 'n']

            if castleside == 'k':
                return [True, 'k']  # Valid King-Side castle
            elif castleside == 'q':
                return [True, 'q']  # Valid Queen-Side castle

        elif turn == 2:  # P2 CASTLE
            for piece in p1pieces:
                if kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True,
                                                                                          'ksc']:  # P1 KING-SIDE CASTLE
                    kschboard, castleside = cloneboard(chboard), 'k'
                    kschboard[rank, file], kschboard[kingloc[0], kingloc[1]] = pieceid, 0
                    kschboard[piecelocator(kschboard, 36)[0], piecelocator(kschboard, 36)[1]], kschboard[
                        rank, file - 1] = 0, 36
                elif kingprecheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True,
                                                                                            'qsc']:  # P1 KING-SIDE CASTLE
                    kschboard, castleside = cloneboard(chboard), 'q'
                    kschboard[rank, file], kschboard[kingloc[0], kingloc[1]] = pieceid, 0
                    kschboard[piecelocator(kschboard, 35)[0], piecelocator(kschboard, 35)[1]], kschboard[
                        rank, file + 1] = 0, 35

                if piece in piecetypelist(turn - 1, 'pawn'):  ## PAWN PIECE ##
                    applypawnmove(kschboard, 2, piece, 200, rank, file, movehistlist)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'knight'):  # KNIGHT PIECE #
                    applyknightmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'bishop'):  # BISHOP PIECE #
                    applybishopmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'rook'):  # ROOK PIECE #
                    applyrookmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'queen'):  # QUEEN PIECE #
                    applyqueenmove(kschboard, 2, piece, rank, file)
                    if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                        return [False, 'n']
                elif piece in piecetypelist(turn - 1, 'king'):  # KING PIECE #
                    if kingprecheckmove(kschboard, turn - 1, piece, rank, file, movehistlist) == True:
                        kschboard[piecelocator(kschboard, piece)[0], piecelocator(kschboard, piece)[1]] = 0
                        kschboard[rank, file] = piece
                        if piecelocator(kschboard, pieceid) == [99, 99]:  # IF king is captured
                            return [False, 'n']

            if castleside == 'k':
                return [True, 'k']  # Valid King-Side castle
            elif castleside == 'q':
                return [True, 'q']  # Valid Queen-Side castle

        else:
            return [False, 'n']  # Error: not turn 1 or 2
    else:
        return [False, 'n']  # Error: kingprecheckmove failed


def applykingmove(chboard, turn, pieceid, rank, file, movehistlist):  # King piece on chboard moves to / capture the index [rank,file]
    kingloc = piecelocator(chboard, pieceid)
    if kingcheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True, 'n']:  # MOVEMENT/CAPTURE
        chboard[piecelocator(chboard, pieceid)[0], piecelocator(chboard, pieceid)[1]] = 0
        chboard[rank, file] = pieceid
        return chboard
    elif turn == 1:  # CASTLE
        if kingcheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True, 'k']:
            chboard[rank, file], chboard[kingloc[0], kingloc[1]] = pieceid, 0
            chboard[piecelocator(chboard, 16)[0], piecelocator(chboard, 16)[1]], chboard[rank, file - 1] = 0, 16
            return chboard
        elif kingcheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True, 'q']:
            chboard[rank, file], chboard[kingloc[0], kingloc[1]] = pieceid, 0
            chboard[piecelocator(chboard, 15)[0], piecelocator(chboard, 15)[1]], chboard[rank, file + 1] = 0, 15
            return chboard
        else:
            return chboard
    elif turn == 2:  # CASTLE
        if kingcheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True, 'k']:
            chboard[rank, file], chboard[kingloc[0], kingloc[1]] = pieceid, 0
            chboard[piecelocator(chboard, 36)[0], piecelocator(chboard, 36)[1]], chboard[rank, file - 1] = 0, 36
            return chboard
        elif kingcheckmove(chboard, turn, pieceid, rank, file, movehistlist) == [True, 'q']:
            chboard[rank, file], chboard[kingloc[0], kingloc[1]] = pieceid, 0
            chboard[piecelocator(chboard, 35)[0], piecelocator(chboard, 35)[1]], chboard[rank, file + 1] = 0, 35
            return chboard
        else:
            return chboard
    else:
        return chboard  # if move is not valid, returns unchanged chboard


def castlecheck(chboard, turn, movehistlist):  # checks if castling rights still available
    nocastle = []
    for moves in movehistlist:
        if turn == 1:
            if moves[0] == 18:
                return ['n', 'n']  # no castling rights due to king moving before
            elif moves[0] == 15:
                nocastle.append('q')
            elif moves[0] == 16:
                nocastle.append('k')
        elif turn == 2:
            if moves[0] == 38:
                return ['n', 'n']  # no castling rights due to king moving before
            elif moves[0] == 35:
                nocastle.append('q')
            elif moves[0] == 36:
                nocastle.append('k')
    if ('q' in nocastle) and ('k' in nocastle):
        return ['n', 'n']  # no castling rights
    elif 'q' in nocastle:
        return ['n', 'k']  # king-side castling rights
    elif 'k' in nocastle:
        return ['q', 'n']  # queen-side castling rights
    else:
        return ['q', 'k']  # both castling rights


def stalematecheck(chboard, turn):  # checks if game is a stalemate based on player's turn
    staleboard = cloneboard(chboard)
    p1pieces, p2pieces = uncaplist(staleboard, 1), uncaplist(staleboard, 2)

    if turn == 1:  # P1 TURN #
        for piece in p1pieces:
            if pieceidentifier(staleboard, piece) == 10:  ##### P1 pawn #####
                piecepos = piecelocator(staleboard, piece)
                for p1prank in list(
                        range(piecepos[0] + 1, piecepos[0] + 3)):  # rank goes up by 2, all files for +0 and +1 rank
                    for p1pfile in list(range(8)):
                        staleboard = cloneboard(chboard)
                        applypawnmove(staleboard, turn, piece, 100, p1prank, p1pfile)
                        for rank in list(range(8)):  # see if staleboard & chboard are the same
                            for file in list(range(8)):
                                if chboard(rank, file) != staleboard(rank, file):  # if pawn is movable, stalemate false
                                    return False
            elif pieceidentifier(staleboard, piece) == 11:  ##### P1 knight #####
                piecepos = piecelocator(staleboard, piece)
                for p1kncoord in [[piecepos[0] - 1, piecepos[1] - 2], [piecepos[0] - 1, piecepos[1] + 2],
                                  [piecepos[0] + 1, piecepos[1] - 2], [piecepos[0] + 1, piecepos[1] + 2],
                                  [piecepos[0] - 2, piecepos[1] - 1], [piecepos[0] - 2, piecepos[1] + 1],
                                  [piecepos[0] + 2, piecepos[1] - 1], [piecepos[0] + 2, piecepos[1] + 1]]:
                    staleboard = cloneboard(chboard)
                    applyknightmove(staleboard, turn, piece, p1kncoord[0], p1kncoord[1])
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if knight is movable, stalemate false
                                return False
            elif pieceidentifier(staleboard, piece) == 12:  ##### P1 bishop #####
                piecepos = piecelocator(staleboard, piece)
                p1bcoordlist = []
                for i in list(range(8)):
                    p1bcoordlist.append([piecepos[0] + i, piecepos[1] + i])
                    p1bcoordlist.append([piecepos[0] - i, piecepos[1] - i])
                    p1bcoordlist.append([piecepos[0] + i, piecepos[1] - i])
                    p1bcoordlist.append([piecepos[0] - i, piecepos[1] + i])
                for p1bcoord in p1bcoordlist:
                    staleboard = cloneboard(chboard)
                    applybishopmove(staleboard, turn, piece, p1bcoord[0], p1bcoord[1])
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if bishop is movable, stalemate false
                                return False
            elif pieceidentifier(staleboard, piece) == 13:  ##### P1 rook #####
                piecepos = piecelocator(staleboard, piece)
                p1rcoordlist = []
                for i in list(range(8)):
                    p1rcoordlist.append([piecepos[0] + i, piecepos[1]])
                    p1rcoordlist.append([piecepos[0] - i, piecepos[1]])
                    p1rcoordlist.append([piecepos[0], piecepos[1]] + i)
                    p1rcoordlist.append([piecepos[0], piecepos[1]] - i)
                for p1rcoord in p1rcoordlist:
                    staleboard = cloneboard(chboard)
                    applyrookmove(staleboard, turn, piece, p1bcoord[0], p1bcoord[1])
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if rook is movable, stalemate false
                                return False
            elif pieceidentifier(staleboard, piece) == 14:  ##### P1 queen #####
                piecepos = piecelocator(staleboard, piece)
                for p1qrank in list(range(8)):
                    for p1qfile in list(range(8)):
                        staleboard = cloneboard(chboard)
                        applyqueenmove(staleboard, turn, piece, p1qrank, p1qfile)
                        for rank in list(range(8)):
                            for file in list(range(8)):
                                if chboard(rank, file) != staleboard(rank, file):  # if queen is movable, stalemate false
                                    return False
            elif pieceidentifier(staleboard, piece) == 15:  ##### P1 king #####
                piecepos = piecelocator(staleboard, piece)
                p1kicoordlist = [[piecepos[0] + 1, piecepos[1]], [piecepos[0] - 1, piecepos[1]],
                                 [piecepos[0], piecepos[1] - 1], [piecepos[0], piecepos[1] + 1],
                                 [piecepos[0] + 1, piecepos[1] + 1], [piecepos[0] + 1, piecepos[1] - 1],
                                 [piecepos[0] - 1, piecepos[1] + 1], [piecepos[0] - 1, piecepos[1] - 1]]
                if castlecheck(staleboard, turn, movehistlist) != ['n', 'n']:  # if castling is possible, else nothing added to coordlist
                    for castlefile in list(range(8)):
                        p1kicoordlist.append([piecepos[0], piecepos[1] + castlefile])
                        p1kicoordlist.append([piecepos[0], piecepos[1] - castlefile])
                for p1kicoord in p1kicoordlist:
                    staleboard = cloneboard(chboard)
                    applykingmove(staleboard, turn, piece, p1kicoord[0], p1kicoord[1], movehistlist)
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if king is movable, stalemate false
                                return False
            else:
                continue  # Not P1 piece

        return True  # P1 cannot move any pieces, STALEMATE

    if turn == 2:  # P2 TURN #
        for piece in p2pieces:
            if pieceidentifier(staleboard, piece) == 20:  ##### P2 pawn #####
                piecepos = piecelocator(staleboard, piece)
                for p2prank in list(range(piecepos[0] - 1, piecepos[0] - 3)):  # rank goes down by 2, all files for +0 and +1 rank
                    for p2pfile in list(range(8)):
                        staleboard = cloneboard(chboard)
                        applypawnmove(staleboard, turn, piece, 200, p2prank, p2pfile)
                        for rank in list(range(8)):  # see if staleboard & chboard are the same
                            for file in list(range(8)):
                                if chboard(rank, file) != staleboard(rank, file):  # if pawn is movable, stalemate false
                                    return False
            elif pieceidentifier(staleboard, piece) == 21:  ##### P2 knight #####
                piecepos = piecelocator(staleboard, piece)
                for p2kncoord in [[piecepos[0] - 1, piecepos[1] - 2], [piecepos[0] - 1, piecepos[1] + 2],
                                  [piecepos[0] + 1, piecepos[1] - 2], [piecepos[0] + 1, piecepos[1] + 2],
                                  [piecepos[0] - 2, piecepos[1] - 1], [piecepos[0] - 2, piecepos[1] + 1],
                                  [piecepos[0] + 2, piecepos[1] - 1], [piecepos[0] + 2, piecepos[1] + 1]]:
                    staleboard = cloneboard(chboard)
                    applyknightmove(staleboard, turn, piece, p2kncoord[0], p2kncoord[1])
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if knight is movable, stalemate false
                                return False
            elif pieceidentifier(staleboard, piece) == 22:  ##### P2 bishop #####
                piecepos = piecelocator(staleboard, piece)
                p2bcoordlist = []
                for i in list(range(8)):
                    p2bcoordlist.append([piecepos[0] + i, piecepos[1] + i])
                    p2bcoordlist.append([piecepos[0] - i, piecepos[1] - i])
                    p2bcoordlist.append([piecepos[0] + i, piecepos[1] - i])
                    p2bcoordlist.append([piecepos[0] - i, piecepos[1] + i])
                for p2bcoord in p2bcoordlist:
                    staleboard = cloneboard(chboard)
                    applybishopmove(staleboard, turn, piece, p2bcoord[0], p2bcoord[1])
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if bishop is movable, stalemate false
                                return False
            elif pieceidentifier(staleboard, piece) == 23:  ##### P2 rook #####
                piecepos = piecelocator(staleboard, piece)
                p2rcoordlist = []
                for i in list(range(8)):
                    p2rcoordlist.append([piecepos[0] + i, piecepos[1]])
                    p2rcoordlist.append([piecepos[0] - i, piecepos[1]])
                    p2rcoordlist.append([piecepos[0], piecepos[1]] + i)
                    p2rcoordlist.append([piecepos[0], piecepos[1]] - i)
                for p2rcoord in p2rcoordlist:
                    staleboard = cloneboard(chboard)
                    applyrookmove(staleboard, turn, piece, p2bcoord[0], p2bcoord[1])
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if rook is movable, stalemate false
                                return False
            elif pieceidentifier(staleboard, piece) == 24:  ##### P2 queen #####
                piecepos = piecelocator(staleboard, piece)
                for p2qrank in list(range(8)):
                    for p2qfile in list(range(8)):
                        staleboard = cloneboard(chboard)
                        applyqueenmove(staleboard, turn, piece, p2qrank, p2qfile)
                        for rank in list(range(8)):
                            for file in list(range(8)):
                                if chboard(rank, file) != staleboard(rank,file):  # if queen is movable, stalemate false
                                    return False
            elif pieceidentifier(staleboard, piece) == 25:  ##### P2 king #####
                piecepos = piecelocator(staleboard, piece)
                p2kicoordlist = [[piecepos[0] + 1, piecepos[1]], [piecepos[0] - 1, piecepos[1]],
                                 [piecepos[0], piecepos[1] - 1], [piecepos[0], piecepos[1] + 1],
                                 [piecepos[0] + 1, piecepos[1] + 1], [piecepos[0] + 1, piecepos[1] - 1],
                                 [piecepos[0] - 1, piecepos[1] + 1], [piecepos[0] - 1, piecepos[1] - 1]]
                if castlecheck(staleboard, turn, movehistlist) != ['n','n']:  # if castling is possible
                    # or else nothing added to coordlist
                    for castlefile in list(range(8)):
                        p2kicoordlist.append([piecepos[0], piecepos[1] + castlefile])
                        p2kicoordlist.append([piecepos[0], piecepos[1] - castlefile])
                for p2kicoord in p2kicoordlist:
                    staleboard = cloneboard(chboard)
                    applykingmove(staleboard, turn, piece, p2kicoord[0], p2kicoord[1], movehistlist)
                    for rank in list(range(8)):  # see if staleboard & chboard are the same
                        for file in list(range(8)):
                            if chboard(rank, file) != staleboard(rank, file):  # if king is movable, stalemate false
                                return False
            else:
                continue  # Not P2 piece

        return True  # P2 cannot move any pieces, STALEMATE

    else:
        return False  # Error: not turn 1 or 2


def fiftymovecheck(chboard, movehistlist):  # determines if fifty move rule draw can be declared by the player
    temphistlist, templistsize, movecounter = clonehistlist(movehistlist), len(temphistlist), 0
    temphistlist.reverse()
    if templistsize >= 100:
        for move in temphistlist:  # condition: no pawn movement
            movecounter += 0.5
            if move[0] in (piecetypelist(1, 'pawn') + piecetypelist(2, 'pawn')):
                return False
            if (move[1] == 'x') or (move[1] == 'ep'):  # condition: no piece captured
                return False
            if movecounter == 50:  # if no pawn movement or piece captures take place
                return True
    else:
        return False


def threefoldcheck(chboard, boardhistlist, movehistlist):  # determines if three-fold repetition rule draw can be declared by the player
    tfboard, tfcounter, tempboardlist, tfturnlist, tfmovelist, tfsubmovelist = np.zeros((8, 8)), 0, cloneboardlist(boardhistlist), [], [], []
    tfboardlist, tfsubboardlist = [], []
    eplist, tfepstatus = [], False  # tfepstatus determines if ep status stayed the same throughout
    castlelist, tfcastlestatus, p1indencastle, p2indencastle = [], False, 0, 0  # tfcastlestatus determines if ep status
    # stayed the same throughout
    for i in list(range(len(tempboardlist) + 1)):  # convert tempboardlist boards to uniformed pieceIDs for each piecetypes
        tempboardlist[i] = unipiecedboard(tempboardlist[i])
    tfboard = tempboardlist[len(tempboardlist) - 1]

    for board in tempboardlist:
        if np.array_equal(board, tfboard):
            tfcounter += 1

    if tfcounter >= 3:  # three identical positions (LATEST THREE)
        tfcounter = 0
        for board in tempboardlist:
            if np.array_equal(board, tfboard):
                tfturnlist.append(tfcounter)  # tfturnlist used for recording board positions
            tfcounter += 1

        if len(tfturnlist) > 3:
            for removelatest in list(range(len(tfturnlist) - 3)):
                tfturnlist.pop(0)  # make turnlist have only three latest turns with same position

        for turnlist in tfturnlist:
            for i in list(range(turnlist + 1)):
                tfsubmovelist.append(movehistlist[i])
                tfsubboardlist.append(boardhistlist[i])
            tfboardlist.append(tfsubboardlist)  # tfboardlist used for recording boardhistlist
            tfmovelist.append(tfsubmovelist)  # tfmovelist used for recording movehistlist
            tfsubboardlist = []
            tfsubmovelist = []

        for i in list(range(len(tfboardlist))):  # TEST FOR ANY EP RIGHTS
            testboard = cloneboard(tfboardlist[i][len(tfboardlist[i]) - 1])
            testhist = tfmovelist[i]

            if testhist[len(testhist) - 1][0] in piecetypelist(2, 'all'):  # P1 TURN TO MOVE (search EP for rights)
                for rank in list(range(8)):
                    for file in list(range(8)):
                        if testboard[rank, file] in piecetypelist(1, 'pawn'):  # Search for P1 pawns
                            for p1rank in list(range(8)):
                                for p1file in list(range(8)):
                                    if pawncheckmove(testboard, 1, testboard[rank, file], p1rank, p1file, testhist) == ['True', 'ep']:  # EP PRESENT
                                        eplist.append([testboard[rank, file], p1rank, p1file])

            if testhist[len(testhist) - 1][0] in piecetypelist(1, 'all'):  # P2 TURN TO MOVE (search EP for rights)
                for rank in list(range(8)):
                    for file in list(range(8)):
                        if testboard[rank, file] in piecetypelist(2, 'pawn'):  # Search for P2 pawns
                            for p2rank in list(range(8)):
                                for p2file in list(range(8)):
                                    if pawncheckmove(testboard, 2, testboard[rank, file], p2rank, p2file, testhist) == ['True', 'ep']:  # EP PRESENT
                                        eplist.append([testboard[rank, file], p2rank, p2file])

        if len(eplist) == 0:  # Determine status is constant throughout
            tfepstatus = True  # No EP status
        elif len(eplist) > 0:
            tfepstatus = True  # EP status constant throughout
            for ep in eplist:
                if eplist.count(ep) != len(tfturnlist):
                    tfepstatus = False  # EP status not constant throughout
                    break

        for i in list(range(len(tfboardlist))):  # TEST FOR ANY CASTLING RIGHTS
            testboard = cloneboard(tfboardlist[i][len(tfboardlist[i]) - 1])
            testhist = tfmovelist[i]

            castlelist.append([1, castlecheck(testboard, 1, testhist)])  # P1 castling rights
            castlelist.append([2, castlecheck(testboard, 2, testhist)])  # P2 castling rights

        for count in list(range(6)):  # counting number of same castling status for P1 & P2
            if count == 0:
                if castlelist[0] == castlelist[0]:
                    p1indencastle += 1
            elif count % 2 == 0:
                if castlelist[0] == castlelist[count]:
                    p1indencastle += 1
            elif count % 2 != 0:
                if castlelist[1] == castlelist[count]:
                    p2indencastle += 1

        if (p1indencastle == 3) and (p2indencastle == 3):
            tfcastlestatus = True  # Castle status stay constant throughout
        else:
            tfcastlestatus = False  # Castle status not constant

        ##### Determines three-fold repetition status #####
        if (tfcastlestatus == True) and (tfepstatus == True):
            return True  # both EP & Castle status are constant throughout the positions
        else:
            return False

    else:  # no three identical positions
        return False


def checkcheck(chboard, turn, movehistlist):  # determines if any player's king is currently in check
    tempboard, kingpos = cloneboard(chboard), [99, 99]
    if turn == 1:  # Player 1
        kingpos = piecelocator(tempboard, piecetypelist(turn, 'king')[0])

        for rank in list(range(8)):
            for file in list(range(8)):
                if tempboard[rank, file] in piecetypelist(2, 'pawn'):
                    if pawncheckmove(tempboard, 2, tempboard[rank, file], kingpos[0], kingpos[1], movehistlist)[
                        0] == True:
                        return True  # King can be captured by P2 pawn

                elif tempboard[rank, file] in piecetypelist(2, 'knight'):
                    if knightcheckmove(tempboard, 2, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P2 knight

                elif tempboard[rank, file] in piecetypelist(2, 'bishop'):
                    if bishopcheckmove(tempboard, 2, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P2 bishop

                elif tempboard[rank, file] in piecetypelist(2, 'rook'):
                    if rookcheckmove(tempboard, 2, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P2 rook

                elif tempboard[rank, file] in piecetypelist(2, 'queen'):
                    if queencheckmove(tempboard, 2, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P2 queen

        return False  # no check conditions for player 1

    if turn == 2:  # Player 2
        kingpos = piecelocator(tempboard, piecetypelist(turn, 'king')[0])

        for rank in list(range(8)):
            for file in list(range(8)):

                if tempboard[rank, file] in piecetypelist(1, 'pawn'):
                    if pawncheckmove(tempboard, 1, tempboard[rank, file], kingpos[0], kingpos[1], movehistlist)[0] == True:
                        return True  # King can be captured by P1 pawn

                elif tempboard[rank, file] in piecetypelist(1, 'knight'):
                    if knightcheckmove(tempboard, 1, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P1 knight

                elif tempboard[rank, file] in piecetypelist(1, 'bishop'):
                    if bishopcheckmove(tempboard, 1, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P1 bishop

                elif tempboard[rank, file] in piecetypelist(1, 'rook'):
                    if rookcheckmove(tempboard, 1, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P1 rook

                elif tempboard[rank, file] in piecetypelist(1, 'queen'):
                    if queencheckmove(tempboard, 1, tempboard[rank, file], kingpos[0], kingpos[1]) == True:
                        return True  # King can be captured by P1 queen

        return False  # no check conditions for player 2

    else:
        return False  # error: invalid not turn 1 or 2


def checkmatecheck(chboard, turn, movehistlist):  # determines if P1/P2 is in checkmate
    # no matter how the checkmated player moves, he cannot remove/evade the threat of check
    simboard = cloneboard(chboard)

    if checkcheck(simboard, turn, movehistlist) == True:  # Player currently in a check

        if turn == 1:
            for rrank in list(range(8)):
                for ffile in list(range(8)):
                    if simboard[rrank, ffile] in piecetypelist(1, 'pawn'):
                        for p1rank in list(range(8)):
                            for p1file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applypawnmove(simboard, turn, simboard[rrank, ffile], 100, p1rank, p1file, movehistlist)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P1 pawn movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(1, 'knight'):
                        for k1rank in list(range(8)):
                            for k1file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applyknightmove(simboard, turn, simboard[rrank, ffile], k1rank, k1file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P1 knight movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(1, 'bishop'):
                        for b1rank in list(range(8)):
                            for b1file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applybishopmove(simboard, turn, simboard[rrank, ffile], b1rank, b1file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P1 bishop movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(1, 'rook'):
                        for r1rank in list(range(8)):
                            for r1file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applyrookmove(simboard, turn, simboard[rrank, ffile], r1rank, r1file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P1 rook movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(1, 'queen'):
                        for q1rank in list(range(8)):
                            for q1file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applyqueenmove(simboard, turn, simboard[rrank, ffile], q1rank, q1file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P1 queen movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(1, 'king'):
                        for ki1rank in list(range(8)):
                            for ki1file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applykingmove(simboard, turn, simboard[rrank, ffile], ki1rank, ki1file, movehistlist)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P1 king movement can remove CHECK

            return True  # Checkmate true when no possible p1 piece movement can remove CHECK

        elif turn == 2:
            for rrank in list(range(8)):
                for ffile in list(range(8)):
                    if simboard[rrank, ffile] in piecetypelist(2, 'pawn'):
                        for p2rank in list(range(8)):
                            for p2file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applypawnmove(simboard, turn, simboard[rrank, ffile], 200, p2rank, p2file, movehistlist)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P2 pawn movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(2, 'knight'):
                        for k2rank in list(range(8)):
                            for k2file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applyknightmove(simboard, turn, simboard[rrank, ffile], k2rank, k2file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P2 knight movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(2, 'bishop'):
                        for b2rank in list(range(8)):
                            for b2file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applybishopmove(simboard, turn, simboard[rrank, ffile], b2rank, b2file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P2 bishop movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(2, 'rook'):
                        for r2rank in list(range(8)):
                            for r2file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applyrookmove(simboard, turn, simboard[rrank, ffile], r2rank, r2file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P2 rook movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(2, 'queen'):
                        for q2rank in list(range(8)):
                            for q2file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applyqueenmove(simboard, turn, simboard[rrank, ffile], q2rank, q2file)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P2 queen movement can remove CHECK

                    elif simboard[rrank, ffile] in piecetypelist(2, 'king'):
                        for ki2rank in list(range(8)):
                            for ki2file in list(range(8)):
                                simboard = cloneboard(chboard)
                                applykingmove(simboard, turn, simboard[rrank, ffile], ki2rank, ki2file, movehistlist)
                                if checkcheck(simboard, turn, movehistlist) == False:
                                    return False  # checkmate is not true as P2 king movement can remove CHECK

            return True  # Checkmate true when no possible p2 piece movement can remove CHECK

        else:
            return False  # error: not turn 1 or 2
    else:
        return False  # player's king not in check


def cloneboard(chboard):  # copies chboard onto a tempboard
    tempboard = np.zeros((8, 8))
    ranks, files = chboard.shape[0], chboard.shape[1]
    tempboard = np.zeros((ranks, files))
    for rrank in range(ranks):
        for ffile in range(files):
            tempboard[rrank, ffile] = chboard[rrank, ffile]
    return tempboard


def clonehistlist(movehistlist):  # copies movehistlist onto a temphistlist
    temphistlist = len(movehistlist), list(range(len(movehistlist)))
    for i in list(range(len(movehistlist))):  # duplicate movehistlist with templist
        temphistlist[i] = movehistlist[i]
    return temphistlist


def cloneboardlist(boardhistlist):  # copies boardhiistlist onto a tempboardlist
    tempboardlist = len(boardhistlist), list(range(len(boardhistlist)))
    for i in list(range(len(boardhistlist))):  # duplicate boardhistlist with templist
        tempboardlist[i] = boardhistlist[i]
    return tempboardlist


def unipiecedboard(chboard):  # converts all pieceids of respective piecetypes (on a board) to be only one pieceid per piecetype
    for rank in list(range(8)):
        for file in list(range(8)):
            if chboard[rank, file] == 0:
                continue
            chboard[rank, file] = pieceidentifier(chboard[rank, file])
    return


def pospiecemove(chboard, turn, pieceid, movehistlist):  # determines all possible locations that a piece can move to
    poslist = []
    if pieceid in piecetypelist(turn, 'pawn'):  # check for all pawn movement locations
        for rank in list(range(chboard.shape[0])):
            for file in list(range(chboard.shape[1])):
                if pawncheckmove(chboard, turn, pieceid, rank, file, movehistlist)[0] == True:
                    poslist.append([rank, file])
        return poslist
    elif pieceid in piecetypelist(1, 'knight'):  # check for all knight movement locations
        for rank in list(range(chboard.shape[0])):
            for file in list(range(chboard.shape[1])):
                if knightcheckmove(chboard, turn, pieceid, rank, file) == True:
                    poslist.append([rank, file])
        return poslist
    elif pieceid in piecetypelist(1, 'bishop'):  # check for all bishop movement locations
        for rank in list(range(chboard.shape[0])):
            for file in list(range(chboard.shape[1])):
                if bishopcheckmove(chboard, turn, pieceid, rank, file) == True:
                    poslist.append([rank, file])
        return poslist
    elif pieceid in piecetypelist(1, 'rook'):  # check for all rook movement locations
        for rank in list(range(chboard.shape[0])):
            for file in list(range(chboard.shape[1])):
                if rookcheckmove(chboard, turn, pieceid, rank, file) == True:
                    poslist.append([rank, file])
        return poslist
    elif pieceid in piecetypelist(1, 'queen'):  # check for all queen movement locations
        for rank in list(range(chboard.shape[0])):
            for file in list(range(chboard.shape[1])):
                if queencheckmove(chboard, turn, pieceid, rank, file) == True:
                    poslist.append([rank, file])
        return poslist
    elif pieceid in piecetypelist(1, 'king'):  # check for all king movement locations
        for rank in list(range(chboard.shape[0])):
            for file in list(range(chboard.shape[1])):
                if kingcheckmove(chboard, turn, pieceid, rank, file, movehistlist) == True:
                    poslist.append([rank, file])
        return poslist
    else:
        return poslist  # error: invalid pieceid


def movehistory(chboard, tempboard, movehistlist):  # Modifies a list by adding new moves
    manalysis = []  # FOR CASTLING and EN PASSANT (-1 pawn piece), both chboard is ALWAYS O!
    captured, moved = 'o', 0  # captured to determine any piece captured, moved to determine pieceid moved
    rin, fin = -1, -1  # rank index, file index
    staticboard = np.zeros((8, 8))
    staticboard[6, 0], staticboard[6, 1], staticboard[6, 2], staticboard[6, 3], staticboard[6, 4], staticboard[6, 5], \
    staticboard[6, 6], staticboard[6, 7] = 1, 2, 3, 4, 5, 6, 7, 8
    staticboard[7, 0], staticboard[7, 1], staticboard[7, 2], staticboard[7, 3], staticboard[7, 4], staticboard[7, 5], \
    staticboard[7, 6], staticboard[7, 7] = 15, 12, 13, 17, 18, 14, 11, 16
    staticboard[1, 0], staticboard[1, 1], staticboard[1, 2], staticboard[1, 3], staticboard[1, 4], staticboard[1, 5], \
    staticboard[1, 6], staticboard[1, 7] = 21, 22, 23, 24, 25, 26, 27, 28
    staticboard[0, 0], staticboard[0, 1], staticboard[0, 2], staticboard[0, 3], staticboard[0, 4], staticboard[0, 5], \
    staticboard[0, 6], staticboard[0, 7] = 35, 32, 34, 37, 38, 33, 31, 36

    for rank in list(range(0, 8)):  # chboard is current board after player moved
        for file in list(range(0, 8)):
            if chboard[rank, file] != tempboard[rank, file]:  # tempboard should always be 1 turn BEHIND chboard!
                manalysis.append(
                    [tempboard[rank, file], chboard[rank, file], [rank, file]])  # append [tp,chp,[rank,file]]
    chpiececount, tpiececount = np.count_nonzero(chboard), np.count_nonzero(tempboard)
    if chpiececount != tpiececount:  # determine if a piece was captured
        captured = 'x'  ######
    else:
        captured = 'o'  ######

    if len(manalysis) == 4:  # CASTLING
        if manalysis[0][2][0] == 7:  # When P1 castles
            for i in manalysis:
                if i[2] == [7, 7]:  # King side castle (right)
                    movehistlist.append([18, captured, 'k', 'c'])
                    return
            for i in manalysis:
                if i[2] == [7, 0]:  # Queen side castle (left)
                    movehistlist.append([18, captured, 'q', 'c'])
                    return
        elif manalysis[0][2][0] == 0:  # When p2 castles
            for i in manalysis:
                if i[2] == [0, 7]:  # King side castle (right)
                    movehistlist.append([38, captured, 'k', 'c'])
                    return
            for i in manalysis:
                if i[2] == [0, 0]:  # Queen side castle (left)
                    movehistlist.append([38, captured, 'q', 'c'])
                    return

    elif len(manalysis) == 3:  # EN PASSANT
        if len(uncaplist(tempboard, 1)) != len(uncaplist(chboard, 1)):  # player 1 piece was captured
            for sets in manalysis:
                if sets[1] in list(range(21, 29)):
                    moved = sets[1]
                    if (sets[0] == 0) and (moved == sets[1]):
                        rank, file = sets[2][0], sets[2][1]
                        movehistlist.append([moved, 'ep', rank, file])
                        return
        elif len(uncaplist(tempboard, 2)) != len(uncaplist(chboard, 2)):  # player 2 piece was captured
            for sets in manalysis:
                if sets[1] in list(range(1, 9)):
                    moved = sets[1]
                    if (sets[0] == 0) and (moved == sets[1]):
                        rank, file = sets[2][0], sets[2][1]
                        movehistlist.append([moved, 'ep', rank, file])
                        return

    else:  # its a normal move/capture
        if manalysis[0][1] == 0:  # if piece moved, chboard will have '0'
            moved = manalysis[0][0]  ##### piece that moved
            rank, file = manalysis[1][2][0], manalysis[1][2][1]  ##### rank and file piece moved to
            movehistlist.append([moved, captured, rank, file])
            return
        elif manalysis[1][1] == 0:  # if piece moved, chboard will have '0'
            moved = manalysis[1][0]  ##### piece that moved
            rank, file = manalysis[0][2][0], manalysis[0][2][1]  ##### rank and file piece moved to
            movehistlist.append([moved, captured, rank, file])
            return


def boardhistory(chboard, boardhistlist):  # adds current board to boardhistlist
    histboard = cloneboard(chboard)
    boardhistlist.append(histboard)
    return


def clearboard(chboard):
    chboard[6,0],chboard[6,1],chboard[6,2],chboard[6,3],chboard[6,4],chboard[6,5],chboard[6,6],chboard[6,7] = 1,2,3,4,5,6,7,8
    chboard[7,0],chboard[7,1],chboard[7,2],chboard[7,3],chboard[7,4],chboard[7,5],chboard[7,6],chboard[7,7] = 15,12,13,17,18,14,11,16
    chboard[1,0],chboard[1,1],chboard[1,2],chboard[1,3],chboard[1,4],chboard[1,5],chboard[1,6],chboard[1,7] = 21,22,23,24,25,26,27,28
    chboard[0,0],chboard[0,1],chboard[0,2],chboard[0,3],chboard[0,4],chboard[0,5],chboard[0,6],chboard[0,7] = 35,32,34,37,38,33,31,36
    return chboard


def chessim(chboard, movehistlist, boardhistlist, pmtdpieceid, turn, pieceid, rank, file):  # test function for CURRENTLY ALL PIECES
    tempboard = cloneboard(chboard)
    if pieceid in piecetypelist(turn, 'pawn'):
        if pawncheckmove(chboard, turn, pieceid, rank, file, movehistlist)[1] == 'p':
            chboard = applypawnmove(chboard, turn, pieceid, pmtdpieceid, rank, file, movehistlist)
        else:
            if turn == 1:
                chboard = applypawnmove(chboard, turn, pieceid, 100, rank, file, movehistlist)
            elif turn == 2:
                chboard = applypawnmove(chboard, turn, pieceid, 200, rank, file, movehistlist)
    elif pieceid in piecetypelist(turn, 'knight'):
        chboard = applyknightmove(chboard, turn, pieceid, rank, file)
    elif pieceid in piecetypelist(turn, 'bishop'):
        chboard = applybishopmove(chboard, turn, pieceid, rank, file)
    elif pieceid in piecetypelist(turn, 'rook'):
        chboard = applyrookmove(chboard, turn, pieceid, rank, file)
    elif pieceid in piecetypelist(turn, 'queen'):
        chboard = applyqueenmove(chboard, turn, pieceid, rank, file)
    elif pieceid in piecetypelist(turn, 'king'):
        chboard = applykingmove(chboard, turn, pieceid, rank, file, movehistlist)

    for i in range(8):
        for j in range(8):
            if tempboard[i, j] != chboard[i, j]:
                movehistory(chboard, tempboard, movehistlist)
                boardhistory(chboard, boardhistlist)
                return chboard
    return chboard  # Error

