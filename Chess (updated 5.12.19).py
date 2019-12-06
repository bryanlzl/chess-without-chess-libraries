import numpy as np

chboard = np.zeros((8,8))
chboard[6,0],chboard[6,1],chboard[6,2],chboard[6,3],chboard[6,4],chboard[6,5],chboard[6,6],chboard[6,7] = 1,2,3,4,5,6,7,8
chboard[7,0],chboard[7,1],chboard[7,2],chboard[7,3],chboard[7,4],chboard[7,5],chboard[7,6],chboard[7,7] = 15,11,13,17,18,14,12,16
chboard[1,0],chboard[1,1],chboard[1,2],chboard[1,3],chboard[1,4],chboard[1,5],chboard[1,6],chboard[1,7] = 31,32,33,34,35,36,37,38
chboard[0,0],chboard[0,1],chboard[0,2],chboard[0,3],chboard[0,4],chboard[0,5],chboard[0,6],chboard[0,7] = 26,22,24,28,27,23,21,25
print(chboard)

def p1uncaplist(chboard,turn): # analyses the board for p1 pieces left, returns a list of p1 pieces left
    p1piecelist = [1,2,3,4,5,6,7,8,11,12,13,14,15,16,17,18]
    p2piecelist = [31,32,33,34,35,36,37,38,21,22,23,24,25,26,27,28]
    pieceremain = []
    if turn == 1: # if player 1
        for rank in chboard:
            for file in rank:
                if file in p1piecelist:
                    pieceremain.append(file)
        return pieceremain
    if turn == 2: # if player 2
        for rank in chboard:
            for file in rank:
                if file in p2piecelist:
                    pieceremain.append(file)
        return pieceremain


def piecelocator(chboard,pieceid): # finds location of piece on the board, returns a list [rank,file]
    indexcount = 0
    for rank in chboard:
        for file in rank:
            if file == pieceid:
                y = indexcount // 8
                x = indexcount - ((indexcount // 8) * 8)
                return [y,x]
            indexcount += 1
            
def p2pawncheckmove(chboard,pieceid,rank,file): # determine if P2pawn can move or capture or NONE
    pawnlist, pawnpos = [31,32,33,34,35,36,37,38], piecelocator(chboard,pieceid)
    print(pawnpos)
    if pieceid in pawnlist:
        if (0 <= rank <= 7) and (0 <= file <= 7):
            if 0 > (pawnpos[0] + 1) > 7: # Check if pawn can move forward
                return False # Cannot move forward anymore, no point determining move or capture
            else:
                vertf = [pawnpos[0]+1,pawnpos[1]]
            if 0 > (pawnpos[1] + 1) > 7: # Check if LDIAG is possible
                print('Error: Invalid move')
                rdiagf = None
            else:
                rdiagf = [pawnpos[0]+1,pawnpos[1]+1]
            if 0 > (pawnpos[1] - 1) > 7:
                print('Error: Invalid move') # Check if RDIAG is possible
                ldiagf = None
            else:
                ldiagf = [pawnpos[0]+1,pawnpos[1]-1]
                    
            if vertf == [rank,file]: # Verify if piece can move forward
                if chboard[vertf[0],vertf[1]] == 0:
                    return True # MOVE 
                else: 
                    return False
            elif rdiagf == [rank,file]: # verify if piece can capture RDIAG
                if chboard[rdiagf[0],rdiagf[1]] in p1uncaplist(chboard,1): # capture if rdiagf position has enemy pieces, else rdiagf invalid
                    return True # CAPTURE
                else: 
                    return False
            elif ldiagf == [rank,file]: # verify if piece can capture LDIAG
                if chboard[ldiagf[0],ldiagf[1]] in p1uncaplist(chboard,1): # capture if ldiagf position has enemy pieces, else ldiagf invalid
                    return True # CAPTURE
                else:
                    return False
            else:
                return False #vertf/ldiagf/rdiagf not possible
        else:
            return False #rank/turn inout out of range
    else:
        return False #pieceid not in pawnlist

def p1pawncheckmove(chboard,pieceid,rank,file): # determine if P1pawn can move or capture or NONE
    pawnlist, pawnpos = [1,2,3,4,5,6,7,8], piecelocator(chboard,pieceid)
    print(pawnpos)
    if pieceid in pawnlist:
        if (0 <= rank <= 7) and (0 <= file <= 7):
            if 0 > (pawnpos[0] - 1) > 7: # Check if pawn can move forward
                return False # Cannot move forward anymore, no point determining move or capture
            else:
                vertf = [pawnpos[0]-1,pawnpos[1]]
            if 0 > (pawnpos[1] + 1) > 7: # Check if LDIAG is possible
                print('Error: Invalid move')
                rdiagf = None
            else:
                rdiagf = [pawnpos[0]-1,pawnpos[1]+1]
            if 0 > (pawnpos[1] - 1) > 7:
                print('Error: Invalid move') # Check if RDIAG is possible
                ldiagf = None
            else:
                ldiagf = [pawnpos[0]-1,pawnpos[1]-1]
                    
            if vertf == [rank,file]: # Verify if piece can move forward
                if chboard[vertf[0],vertf[1]] == 0:
                    return True # MOVE 
                else: 
                    return False
            elif rdiagf == [rank,file]: # verify if piece can capture RDIAG
                if chboard[rdiagf[0],rdiagf[1]] in p1uncaplist(chboard,2): # capture if rdiagf position has enemy pieces, else rdiagf invalid
                    return True # CAPTURE
                else: 
                    return False
            elif ldiagf == [rank,file]: # verify if piece can capture LDIAG
                if chboard[ldiagf[0],ldiagf[1]] in p1uncaplist(chboard,2): # capture if ldiagf position has enemy pieces, else ldiagf invalid
                    return True # CAPTURE
                else:
                    return False
            else:
                return False #vertf/ldiagf/rdiagf not possible
        else:
            return False #rank/turn inout out of range
    else:
        return False #pieceid not in pawnlist

def pawncheckmove(chboard,turn,pieceid,rank,file): # CORE PAWN MOVEMENT/CAPTURE FUNCTION
    if turn == 1:
        return p1pawncheckmove(chboard,pieceid,rank,file)
    elif turn == 2:
        return p2pawncheckmove(chboard,pieceid,rank,file)