import Chess_function as ch
import numpy as np
import random


def level0ai(chboard, turn, movehistlist, boardhistlist): # generates a random move based on its turn
    if ch.checkmatecheck(chboard, turn, movehistlist, boardhistlist) == True or ch.stalematecheck(chboard, movehistlist, turn) == True: # if checkmate, exit
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
    if ch.checkmatecheck(chboard, turn, movehistlist, boardhistlist) == True or ch.stalematecheck(chboard, movehistlist, turn) == True: # if checkmate, exit
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


def level2ai(chboard, turn, movehistlist, boardhistlist): # min-max search tree, 3 ply (depth), NOT USING RECURSION BECAUSE ALOT SLOWER THAN ITERATION (in this case, processing speed matters alot)
    if ch.checkmatecheck(chboard, turn, movehistlist, boardhistlist) == True or ch.stalematecheck(chboard, movehistlist, turn) == True: # if checkmate, exit
        return [999, 999, 999, 999]
    countthird = 0
    # white turn = 1, black turn = 2 #
    minimaxtree = []
    if turn == 1:
        oppturn = 2
    elif turn == 2:
        oppturn = 1
    print('creating minimax tree, first branch')
    ## first primary branch created ##
    minimaxtree = moveexplorer(chboard, turn, movehistlist, boardhistlist) # [chboard, turn, movehistlist, boardhistlist, INSERT NEW BRANCH HERE]
    ## second branch created ##
    print('creating second branch')
    for secondply in minimaxtree:
        secondply.append(moveexplorer(secondply[0],  turninverter(secondply[1]), secondply[2], secondply[3]))
        ## third branch created ##
    print('creating third branch')
    for secondply in minimaxtree:
        for thirdply in secondply[4]:
            # LEAF/LEAVES of the tree #
            thirdply.append(moveexplorer(thirdply[0], turninverter(thirdply[1]), thirdply[2], thirdply[3]))
            print('number of 3rd branch =', countthird, 'size of 3rd branch (no. of leaves) =', len(thirdply[4]))
            countthird += 1
    # evaluation of board #
    firstindex, secondindex = 0, 1
    summarybranch = [] # to hold the index and evaluation values of all boards
    max = 9999
    min = -9999
    current, pruner = 0, 0 # pruner for alpha-beta pruning
######################################### Evaluating 2rd ply/branch ##########################################################
    print('evaluating third branch')
    for firstply in minimaxtree:
        summarybranch.append([[firstindex]])
        secondindex = 0 # Specifically FOR PRUNER USE
        for secondply in firstply[4]:
            if turn == 1:
                current = min
            elif turn == 2:
                current = max

            for thirdply in secondply[4]:
                if secondindex == 0:
                    if turn == 1: # find maximum evaluation
                        if totalboardvalue(thirdply[0], thirdply[2], thirdply[3]) > current:
                            current = totalboardvalue(thirdply[0], thirdply[2], thirdply[3])
                    elif turn == 2: # find minimum evaluation
                        if totalboardvalue(thirdply[0], thirdply[2], thirdply[3]) < current:
                            current = totalboardvalue(thirdply[0], thirdply[2], thirdply[3])

                ###### ALPHA-BETA PRUNING (third branch) ######
                else:
                    if turn == 1: # find maximum evaluation
                        if totalboardvalue(thirdply[0], thirdply[2], thirdply[3]) > current:
                            current = totalboardvalue(thirdply[0], thirdply[2], thirdply[3])
                            if pruner < current:
                                break
                    elif turn == 2: # find minimum evaluation
                        if totalboardvalue(thirdply[0], thirdply[2], thirdply[3]) < current:
                            current = totalboardvalue(thirdply[0], thirdply[2], thirdply[3])
                            if pruner > current:
                                break
            ### compiling results phase ###
            if secondindex == 0: # For first set: evaluation is accepted
                pruner = current # Pruner needs a benchmark
                secondindex += 1
                # after finding most favourable eval for third branch, append into second branch #
                summarybranch[firstindex].append(current)  # [ [[firstindex], current eval, current eval], [[firstindex], current eval, current eval,....], ..... ]
                continue
            else:
                pruner = current # Pruner sets a better benchmark
                summarybranch[firstindex].append(current)
        firstindex += 1
        print('3rd branch done')
######################################### Evaluating 2nd ply/branch ##########################################################
    # evaluating the tree (2nd ply) #
    if turn == 1:  # find minimum evaluation
        current = max
    elif turn == 2:  # find maximum evaluation
        current = min
    firstindex, secondindex, pruneindex = 0, 0, 0
    print('evaluating second branch')
    for findex in summarybranch:
        secondindex = 0 # secondindex only used to for indexing the second element onwards (evaluations)
        for sindex in findex:
            if pruneindex == 0:
                if secondindex >= 1: # iterate the second element (eval of second branch)
                    if turn == 1:  # find minimum evaluation
                        if sindex < current:
                            current = sindex
                    elif turn == 2:  # find maximum evaluation
                        if sindex > current:
                            current = sindex

            ###### ALPHA-BETA PRUNING (second branch) ######
            elif pruneindex >= 1:
                if secondindex >= 1: # iterate the second element (eval of second branch)
                    if turn == 1:  # find minimum evaluation
                        if sindex < current:
                            current = sindex
                            if pruner > current: # if 2nd branch eval is bigger than the 3rd branch eval on another 2nd branch, prune it
                                break
                    elif turn == 2:  # find maximum evaluation
                        if sindex > current:
                            current = sindex
                            if pruner < current: # if 2nd branch eval is smaller than the 3rd branch eval on another 2nd branch, prune it
                                break
            secondindex += 1 # nothing important
        ### compiling results phase ###
        if pruneindex == 0:
            pruner = current
            pruneindex += 1
            summarybranch[firstindex][0].append(current) # [ [[firstindex, current], ......], [[firstindex, current], ......], ..... ]
            continue
        elif pruneindex >= 1:
            pruner = current # pruner sets a better benchmark
            summarybranch[firstindex][0].append(current) # [ [[firstindex, current], ......], [[firstindex, current], ......], ..... ]
    print('2nd branch done')
######################################### Evaluating 1st ply/branch ##########################################################
    # evaluating the tree (1st ply) #
    if turn == 1:  # find maximum evaluation
        current = min
        currentindex = 0
    elif turn == 2:  # find minimum evaluation
        current = max
        currentindex = 0
    print('evaluating first branch')
    for findex in summarybranch:
        if len(findex[0]) == 2:
            if turn == 1: # find maximum evaluation
                if findex[0][1] > current:
                    current = findex[0][1]
                    currentindex = findex[0][0] # index of minimaxtree with the best evaluation for white player (3 ply)
            elif turn == 2: # find minimum evaluation
                if findex[0][1] < current:
                    current = findex[0][1]
                    currentindex = findex[0][0] # index of minimaxtree with the best evaluation for white player (3 ply)
    print('1st branch done')
    print('outputting results... AI making move')
######################################### Convert index to moves for function to return ##########################################################
    besteval = []
    besteval.append(minimaxtree[currentindex][0])
    besteval.append(minimaxtree[currentindex][1])
    besteval.append(minimaxtree[currentindex][2])
    besteval.append(minimaxtree[currentindex][3])
    # resulting list -> [chboard, turn, movehistlist, boardhistlist] #

    movelistsize = len(besteval[2])
    if besteval[2][movelistsize-1] == [18, 'o', 'k', 'c']:
        return [18, random.randint(131, 138), 7, 6]
    elif besteval[2][movelistsize-1] == [18, 'o', 'q', 'c']:
        return [18, random.randint(131, 138), 7, 2]
    elif besteval[2][movelistsize-1] == [38, 'o', 'k', 'c']:
        return [38, random.randint(231, 238), 0, 6]
    elif besteval[2][movelistsize-1] == [38, 'o', 'q', 'c']:
        return [38, random.randint(231, 238), 0, 2]

    if turn == 1:
        return [besteval[2][movelistsize - 1][0], random.randint(131, 138), besteval[2][movelistsize - 1][2], besteval[2][movelistsize - 1][3]]
    elif turn == 2:
        return [besteval[2][movelistsize - 1][0], random.randint(231, 238), besteval[2][movelistsize - 1][2], besteval[2][movelistsize - 1][3]]


def turninverter(turn):
    if turn == 1:
        return 2
    elif turn == 2:
        return 1
    else:
        return 99 # error: invalid turn


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
    elif pieceid in ch.piecetypelist(2, 'king'):
        return -900
    else:
        return 0  # invalid pieceid


def totalboardvalue(chboard, movehistlist, boardhistlist): # sums up the value of all black and white piece
    total = 0
    for rank in range(8):
        for file in range(8):
            total += pieceeval(chboard[rank][file])
    if ch.checkmatecheck(chboard, 1, movehistlist, boardhistlist) == True: # white checkmate, win for black
        total -= 900
    if ch.checkmatecheck(chboard, 2, movehistlist, boardhistlist) == True: # black checkmate, win for white
        total += 900
    return total


def moveexplorer(chboard, turn, movehistlist, boardhistlist): # explores all possible moves for a turn
    boardsetlist = [] # stores boards
    if turn == 1:
        pieceprom = random.randint(131, 138)
    elif turn == 2:
        pieceprom = random.randint(231, 238)
    uncapped = ch.uncaplist(chboard, turn)
    simboard = np.copy(chboard)
    simmovelist = ch.clonehistlist(movehistlist)
    simboardlist = ch.cloneboardlist(boardhistlist)

    # if checkmate, return boardsetlist as the arguments #
    if ch.checkmatecheck(simboard, turn, simmovelist, simboardlist) == True or ch.checkmatecheck(simboard, turninverter(turn), simmovelist, simboardlist) == True:
        boardsetlist.append([simboard, turn, simmovelist, simboardlist])
        return boardsetlist # returns the checkmated board

    # assume that the player might be in check #
    for piece in uncapped:
        for rank in range(8):
            for file in range(8):
                if ch.onemovecheckcheck(chboard, boardhistlist, movehistlist, turn, piece, rank, file) == False: # Ensure player will not be in check on opponent's turn (self-check)
                    ch.chessim(simboard, simmovelist, simboardlist, pieceprom, turn, piece, rank, file)
                    boardsetlist.append([simboard, turn, simmovelist, simboardlist]) # [chboard, turn, movehistlist, boardhistlist]
                    simboard = np.copy(chboard)
                    simmovelist = ch.clonehistlist(movehistlist)
                    simboardlist = ch.cloneboardlist(boardhistlist)
    return boardsetlist # returns a list of possible [chessboards and respective history lists] (moves)
