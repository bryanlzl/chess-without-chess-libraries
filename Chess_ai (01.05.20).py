import Chess_function as ch
import numpy as np
import random


def level0ai(chboard, turn, movehistlist, boardhistlist): # generates a random move based on its turn
    if ch.checkmatecheck(chboard, turn, movehistlist, boardhistlist) == True: # if checkmate, exit
        return [999, 999, 999, 999]
    piecelist = ch.uncaplist(chboard, turn)
    pieceselected = random.choice(piecelist)
    rank = random.randint(0, 7)
    file = random.randint(0, 7)
    if turn == 1:
        pieceprom = random.randint(131, 138)
    elif turn == 2:
        pieceprom = random.randint(231, 238)

    while True:
        pieceselected = random.choice(piecelist)
        rank = random.randint(0, 7)
        file = random.randint(0, 7)
        if turn == 1:
            pieceprom = random.randint(131, 138)
        elif turn == 2:
            pieceprom = random.randint(231, 238)

        if ch.chessimchecker(chboard, movehistlist, boardhistlist, pieceprom, turn, pieceselected, rank, file) == True:
            if ch.onemovecheckcheck(chboard, boardhistlist, movehistlist, turn, pieceselected, rank, file) == False:
                break

    return [pieceselected, pieceprom, rank, file] # [pieceid, pmtdpieceid, rank, file]


def level1ai(chboard, turn, movehistlist, boardhistlist): # generates a move that will capture enemy when it can, else random moves
    if ch.checkmatecheck(chboard, turn, movehistlist, boardhistlist) == True: # if checkmate, exit
        return [999, 999, 999, 999]
    caplist = possiblecaps(chboard, movehistlist, boardhistlist, turn) # [cappedpiece, pieceid, pmtdpieceid, rank, file]
    bestvaluecap = [0, 0, 0, 0, 0]

    if len(caplist) > 0: # if there are possible captures
        for i in caplist:
            if turn == 1:
                if pieceeval(i[0]) < bestvaluecap[0]: # white capturing black, more negative eval piece, better
                    bestvaluecap = i
            elif turn == 2:
                if pieceeval(i[0]) > bestvaluecap[0]: # black capturing white, more positive eval piece, better
                    bestvaluecap = i
        bestvaluecap.pop(0)
        return bestvaluecap # [pieceid, pmtdpieceid, rank, file]

    elif len(caplist) == 0: # if no possible captures, random move
        return level0ai(chboard, turn, movehistlist, boardhistlist) # [pieceid, pmtdpieceid, rank, file]


def possiblecaps(chboard, movehistlist, boardhistlist, turn): # creates a nested list of all possible captures for AI turn [cappedpiece, pieceid, pmtdpieceid, rank, file]
    possiblecaplist = []
    if turn == 1:
        oppturn = 2
        pieceprom = random.randint(131, 138)
    elif turn == 2:
        oppturn = 1
        pieceprom = random.randint(231, 238)
    opppiecelist = ch.uncaplist(chboard, oppturn)
    simboard = np.copy(chboard)
    piecelist = ch.uncaplist(chboard, turn)
    simmovelist = ch.clonehistlist(movehistlist)
    simboardlist = ch.cloneboardlist(boardhistlist)
    for piece in piecelist:
        for rank in range(8):
            for file in range(8):
                if ch.chessimchecker(simboard, simmovelist, simboardlist, pieceprom, turn, piece, rank, file) == True:
                    if ch.onemovecheckcheck(chboard, boardhistlist, movehistlist, turn, piece, rank, file) == False:
                        ch.chessim(simboard, simmovelist, simboardlist, pieceprom, turn, piece, rank, file)
                        caplist = listdiff(ch.uncaplist(simboard, oppturn), opppiecelist)
                        if len(caplist) > 0:
                            for i in caplist:
                                possiblecaplist.append([i, piece, pieceprom, rank, file]) # [cappedpiece, pieceid, pmtdpieceid, rank, file]
                        ch.undomove(simboard, simboardlist, simmovelist)
                    else:
                        continue
                else:
                    continue
    return possiblecaplist


def listdiff(list1, list2):
    listd = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return listd


def pieceeval(pieceid): #evaluates the piece and determines its value
    if pieceid in ch.piecetypelist(1, 'pawn'):
        return 10
    elif pieceid in ch.piecetypelist(1, 'knight'):
        return 30
    elif pieceid in ch.piecetypelist(1, 'bishop'):
        return 30
    elif pieceid in ch.piecetypelist(1, 'rook'):
        return 50
    elif pieceid in ch.piecetypelist(1, 'queen'):
        return 90
    elif pieceid in ch.piecetypelist(1, 'king'):
        return 900
    elif pieceid in ch.piecetypelist(2, 'pawn'):
        return -10
    elif pieceid in ch.piecetypelist(2, 'knight'):
        return -30
    elif pieceid in ch.piecetypelist(2, 'bishop'):
        return -30
    elif pieceid in ch.piecetypelist(2, 'rook'):
        return -60
    elif pieceid in ch.piecetypelist(2, 'queen'):
        return -90
    elif pieceid in ch.iecetypelist(2, 'king'):
        return -900
    else:
        return 0  # invalid pieceid

