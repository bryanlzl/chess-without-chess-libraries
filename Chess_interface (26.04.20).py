import ChessFuncHere as ch
import itertools, sys
import numpy as np
import pygame as pg

movehistlist = []
boardhistlist = []

chboard = np.zeros((8, 8))
chboard[6, 0], chboard[6, 1], chboard[6, 2], chboard[6, 3], chboard[6, 4], chboard[6, 5], chboard[6, 6], chboard[6, 7] = 1, 2, 3, 4, 5, 6, 7, 8
chboard[7, 0], chboard[7, 1], chboard[7, 2], chboard[7, 3], chboard[7, 4], chboard[7, 5], chboard[7, 6], chboard[7, 7] = 15, 12, 13, 17, 18, 14, 11, 16
chboard[1, 0], chboard[1, 1], chboard[1, 2], chboard[1, 3], chboard[1, 4], chboard[1, 5], chboard[1, 6], chboard[1, 7] = 21, 22, 23, 24, 25, 26, 27, 28
chboard[0, 0], chboard[0, 1], chboard[0, 2], chboard[0, 3], chboard[0, 4], chboard[0, 5], chboard[0, 6], chboard[0, 7] = 35, 32, 34, 37, 38, 33, 31, 36

def rfconverter(sysrank,sysfile): # converts system rank file to real rank file
    counter,holder,realfile = 0,0,0
    realrank = 'a'
    realranklist = ['a','b','c','d','e','f','g','h']
    notrealfilelist = [7,6,5,4,3,2,1,0]
    holder = sysrank
    sysrank = sysfile
    sysfile = holder
    for i in notrealfilelist:
        if sysfile == 0:
            realfile = i
            break
        sysfile -= 1

    for i in realranklist:
        if counter == sysrank:
            realrank = i
            break
        counter += 1
    return [realrank,realfile]

### INTERFACE START###
pg.init()

BLACK = pg.Color('grey')
WHITE = pg.Color('white')
GREEN = (0,90,0)
FORESTGREEN = (0,50,0)
LIGHTBROWN = (205,192,176)
LEMON = (238,233,191)
ORANGE = (238,64,0)

screen_width = 850
screen_height = 673

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

grid = [] # 2D list that holds all positions and coordinates of each grid
prombutton = [] # 1D list of pawn promote buttons

## GRID FOR CHESS BOARD ##
for x in range(8):
    layer = []
    for y in range(8):
        layer.append(pg.Rect(x*70, y*70, 70, 70))
    grid.append(layer)

## BUTTONS FOR PROMOTION ##
for y in range(4):
    prombutton.append(pg.Rect(575, 60+(y*50*1.05), 80, 25))

## BUTTON FOR UNDO ##
undobutton = pg.Rect(570, 260 + (0 * 50 * 1.05), 115, 30)

def strip_from_sheet(sheet, start, size, columns, rows=1):
  frames = []
  for j in range(rows):
    for i in range(columns):
      location = (start[0] + size[0] * i, start[1] + size[1] * j)
      frames.append(sheet.subsurface(pg.Rect(location, size)))
  return frames


sheet = pg.image.load("./media/Chess_Pieces_Sprite.png")
size = sheet.get_size()
frames = strip_from_sheet(sheet, (0, 0), ((size[0] / 6, size[1] / 2)), 6, 2)

chess_sprites = [
    {"name": "King", "id": 0, "piece_type": ch.piecetypelist(1, "king"), "position": [(280, 490)], "sprites": frames[0]},
    {"name": "Queen", "id": 1, "piece_type": ch.piecetypelist(1, "queen"), "position": [(210, 490)], "sprites": frames[1]},
    {"name": "Bishop", "id": 2, "piece_type": ch.piecetypelist(1, "bishop"), "position": [(140, 490), (350, 490)], "sprites": frames[2]},
    {"name": "Knight", "id": 3, "piece_type": ch.piecetypelist(1, "knight"), "position": [(420, 490), (70, 490)], "sprites": frames[3]},
    {"name": "Rook", "id": 4, "piece_type": ch.piecetypelist(1, "rook"), "position": [(0, 490), (490, 490)], "sprites": frames[4]},
    {"name": "Pawn", "id": 5, "piece_type": ch.piecetypelist(1, "pawn"), "position": [((i - 1) * 70, 420) for i in ch.piecetypelist(1, "pawn")], "sprites": frames[5]},
    {"name": "B_King", "id": 6, "piece_type": ch.piecetypelist(2, "king"), "position": [(280, 0)], "sprites": frames[6]},
    {"name": "B_Queen", "id": 7, "piece_type": ch.piecetypelist(2, "queen"), "position": [(210, 0)], "sprites": frames[7]},
    {"name": "B_Bishop", "id": 8, "piece_type": ch.piecetypelist(2, "bishop"), "position": [(350, 0), (140, 0)], "sprites": frames[8]},
    {"name": "B_Knight", "id": 9, "piece_type": ch.piecetypelist(2, "knight"), "position": [(420, 0), (70, 0)], "sprites": frames[9]},
    {"name": "B_Rook", "id": 10, "piece_type": ch.piecetypelist(2, "rook"), "position": [(0, 0), (490, 0)], "sprites": frames[10]},
    {"name": "B_Pawn", "id": 11, "piece_type": ch.piecetypelist(2, "pawn"), "position": [((i - 21) * 70, 70) for i in ch.piecetypelist(2, "pawn")], "sprites": frames[11]}
]


def main():
    global SCREEN, CLOCK
    pg.init()
    pg.display.set_caption('Chess by bryanlzl')
    SCREEN = pg.display.set_mode((screen_width, screen_height))
    CLOCK = pg.time.Clock()
    SCREEN.fill(GREEN)
    fclick = 0
    pawnpromote = 0

    pg.event.set_blocked([pg.MOUSEMOTION, pg.MOUSEBUTTONUP])

    while True:
        drawGrid()
        rendersprites()
        drawpromoteButtons()
        promotebuttonText()
        drawundobutton()
        gamestatusbox()

        if fclick != 0 and pawnpromote != 1:
            movemarkers(chboard, movehistlist, fclick) ## highlight movable positions ##

        if pawnpromote == 1:
            promhighlights() ## highlight promotion buttons ##

        if len(movehistlist) >= 1: # Announces the current check status
            movedpiece = movehistlist[len(movehistlist)-1][0] # [movedpiece, captured, rank, file]
            pieceidentified = ch.pieceidentifier(movedpiece)
            if pieceidentified < 20 and pieceidentified != 99: # If white made previous move
                gamestatustext(chboard, 2, boardhistlist, movehistlist)
            elif pieceidentified >= 20 and pieceidentified != 99:
                gamestatustext(chboard, 1, boardhistlist, movehistlist)

        for event in pg.event.get():

            #if (event.type == pg.MOUSEBUTTONDOWN) and (undobutton.collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])):
                #chboard = ch.undomove(chboard,boardhistlist,movehistlist)[0]
                #pass

            if event.type == pg.MOUSEBUTTONDOWN and (fclick == 0 or fclick[0] == 999) and pg.mouse.get_pressed()[0]:
                fclick = firstclick() # [pieceid, turn]
                continue

            elif (event.type == pg.MOUSEBUTTONDOWN) and (fclick != 0) and pg.mouse.get_pressed()[0] and (pawnpromote == 0): # first click is in the board and on any piece
                sclick = secondclick() ### [rank, file] ###
                if sclick[0] != 999: # second click is in the board

                    if ch.pawncheckmove(chboard, fclick[1], fclick[0], sclick[0], sclick[1], movehistlist) == [True, 'p']: ## promote pawn!! ##
                        pawnpromote = 1
                        continue

                    ch.chessim(chboard, movehistlist, boardhistlist, 100, fclick[1], fclick[0], sclick[0], sclick[1])
                    fclick = 0
                    continue

            elif (event.type == pg.MOUSEBUTTONDOWN) and (fclick != 0) and pg.mouse.get_pressed()[0] and pawnpromote == 1:
                pclick = promclick(fclick, sclick)
                if pclick[0] != 999:
                    ch.chessim(chboard, movehistlist, boardhistlist, pclick[0], pclick[1], pclick[2], pclick[3], pclick[4])
                    pawnpromote = 0
                    fclick = 0
                    continue
                else:
                    continue

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()


def rendersprites():
    counter,x,y = 0,0,0
    spriteSize = 70  # Set the size of the grid block
    for row in chboard:
        x = 0
        for col in row:
            rect = pg.Rect(x * spriteSize, y * spriteSize, spriteSize, spriteSize)
            for i in chess_sprites:
                sprite_id = i["id"]
                piece_type = i["piece_type"]
                position = i["position"]
                sprite = i["sprites"]
                if col in piece_type:
                    SCREEN.blit(pg.transform.scale(sprite, (70, 70)), rect)
            x += 1
        y += 1


def drawGrid():
    counter = 0
    blockSize = 70 #Set the size of the grid block

    for x in range(8):
        if x % 2 == 0:
            counter = 0
        else:
            counter = 1
        for y in range(8):
            rect = pg.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            if counter % 2 == 0:
                pg.draw.rect(SCREEN, WHITE, rect)
            else:
                pg.draw.rect(SCREEN, BLACK, rect)
            counter += 1


def drawpromoteButtons():
    counter = 0
    width = 80
    height = 25

    contain = pg.Rect(570, 10 + (0 * 50 * 1.05), 115, 240)
    pg.draw.rect(SCREEN, (112, 128, 144), contain)

    contain = pg.Rect(570, 10 + (0 * 50 * 1.05), 115, 30)
    pg.draw.rect(SCREEN, LIGHTBROWN, contain)

    for y in range(4): # BUTTONS
        rect = pg.Rect(575, 60+(y*50*1.05), width, height)
        pg.draw.rect(SCREEN, LEMON, rect)


def promotebuttonText():
    POKEFONT1 = pg.font.Font("./media/8-Bit Madness.ttf", 23)
    text = ['Knight','Bishop','Rook','Queen']
    for y in range(4):
        SCREEN.blit(POKEFONT1.render(text[y], True, (0, 0, 0)), (585, 63+(y*50*1.05)))
    SCREEN.blit(POKEFONT1.render('Promotion!', True, (0, 0, 0)), (580, 18))


def mousepostoboard(x,y): # mouse click on board, returns row and col
    row,col = 0,0
    for i in grid:
        col = 0
        for j in i:
            if j.collidepoint(x,y):
                return (col, row) # returns location on chboard
            col += 1
        row += 1
    return (999, 999) # error: no location on chboard


def mousepostoprom(x,y):
    index = 0
    for i in prombutton:
        if i.collidepoint(x,y):
            if index == 0:
                return 'knight'
            elif index == 1:
                return 'bishop'
            elif index == 2:
                return 'rook'
            elif index == 3:
                return 'queen'
        index += 1
    return 'none'


def firstclick():
    if pg.mouse.get_pressed()[0]:
        pos1 = pg.mouse.get_pos()
        if mousepostoboard(pos1[0], pos1[1]) != (999, 999): # clicked on a point of chboard
            if chboard[mousepostoboard(pos1[0], pos1[1])[0]][mousepostoboard(pos1[0], pos1[1])[1]] != 0:
                selectedpiece = chboard[mousepostoboard(pos1[0], pos1[1])[0]][mousepostoboard(pos1[0], pos1[1])[1]]  # TAKE SELECTED PIECEID
                if ch.pieceidentifier(selectedpiece) < 20:  # TAKE EITHER TURN VALUE
                    turn = 1
                if ch.pieceidentifier(selectedpiece) >= 20:  # TAKE EITHER TURN VALUE
                    turn = 2
                return [selectedpiece, turn]

            else:
                return [999, 999]
        else:
            return [999, 999]
    else:
        return [999, 999]


def movemarkers(chboard, movehistlist, fclick): # finds out and marks out possible moves of a piece on the board display
    movelist = []
    for row in range(8):
        for col in range(8):
            if ch.pieceidentifier(fclick[0]) == 10 or ch.pieceidentifier(fclick[0]) == 20: # if PAWN
                if ch.pawncheckmove(chboard, fclick[1], fclick[0], row, col, movehistlist)[0] == True:
                    movelist.append([row, col])
                    continue
            if ch.pieceidentifier(fclick[0]) == 11 or ch.pieceidentifier(fclick[0]) == 21: # if KNIGHT
                if ch.knightcheckmove(chboard, fclick[1], fclick[0], row, col) == True:
                    movelist.append([row, col])
                    continue
            if ch.pieceidentifier(fclick[0]) == 12 or ch.pieceidentifier(fclick[0]) == 22: # if BISHOP
                if ch.bishopcheckmove(chboard, fclick[1], fclick[0], row, col) == True:
                    movelist.append([row, col])
                    continue
            if ch.pieceidentifier(fclick[0]) == 13 or ch.pieceidentifier(fclick[0]) == 23: # if ROOK
                if ch.rookcheckmove(chboard, fclick[1], fclick[0], row, col) == True:
                    movelist.append([row, col])
                    continue
            if ch.pieceidentifier(fclick[0]) == 14 or ch.pieceidentifier(fclick[0]) == 24: # if QUEEN
                if ch.queencheckmove(chboard, fclick[1], fclick[0], row, col) == True:
                    movelist.append([row, col])
                    continue
            if ch.pieceidentifier(fclick[0]) == 15 or ch.pieceidentifier(fclick[0]) == 25: # if KING
                    if ch.kingcheckmove(chboard, fclick[1], fclick[0], row, col, movehistlist)[0] == True:
                        movelist.append([row, col])
                        continue

    for move in movelist: # Displays all positions the piece can move to
        crow, ccol = move[0], move[1]
        for x in range(8):     ## pg.draw.circle(surface, color, center, radius) ##
            for y in range(8):
                if crow != 0:
                    continue
                if ccol == 0:
                    pg.draw.circle(SCREEN, (0, 170, 0), (35 + (y * 70), 35 + (x * 70)), 10)
                    break
                elif crow == 0 and ccol != 0:
                    ccol -= 1
            crow -= 1

    piecepos = ch.piecelocator(chboard, fclick[0])

    for move in movelist: # Hightlights selected piece
        for x in range(8):     ## pg.draw.circle(surface, color, center, radius) ##
            for y in range(8):
                if piecepos[0] != 0:
                    continue
                if piecepos[1] == 0:
                    h_rect = pg.Rect(y * 70, x * 70, 70, 70)
                    pg.draw.rect(SCREEN, (0, 170, 0), h_rect, 3)
                    break
                elif piecepos[0] == 0 and piecepos[1] != 0:
                    piecepos[1] -= 1
            piecepos[0] -= 1


def secondclick():
    if pg.mouse.get_pressed()[0]:
        pos1 = pg.mouse.get_pos()
        if mousepostoboard(pos1[0], pos1[1]) != (999, 999): # clicked on a point of chboard
            destboard = mousepostoboard(pos1[0], pos1[1]) # TAKE CHBOARD COORDINATES
            return [destboard[0], destboard[1]]
        else:
            return [999, 999]
    else:
        return [999, 999]


def promclick(fclick, sclick): # Click which piece for promotion, RETURNS PROMOTED PIECE ID (pmtdpieceid)
    if pg.mouse.get_pressed()[0]:
        pos1 = pg.mouse.get_pos()

        if mousepostoprom(pos1[0], pos1[1]) == 'knight':
            for piece in ch.piecetypelist(fclick[1], 'knight'):
                if piece not in ch.uncaplist(chboard, fclick[1]):
                    return [piece, fclick[1], fclick[0], sclick[0], sclick[1]]  ###[pmtdpieceid, turn, pieceid, rank, file]###

        elif mousepostoprom(pos1[0], pos1[1]) == 'bishop':
            for piece in ch.piecetypelist(fclick[1], 'bishop'):
                if piece not in ch.uncaplist(chboard, fclick[1]):
                    return [piece, fclick[1], fclick[0], sclick[0], sclick[1]]

        elif mousepostoprom(pos1[0], pos1[1]) == 'rook':
            for piece in ch.piecetypelist(fclick[1], 'rook'):
                if piece not in ch.uncaplist(chboard, fclick[1]):
                    return [piece, fclick[1], fclick[0], sclick[0], sclick[1]]

        elif mousepostoprom(pos1[0], pos1[1]) == 'queen':
            for piece in ch.piecetypelist(fclick[1], 'queen'):
                if piece not in ch.uncaplist(chboard, fclick[1]):
                    return [piece, fclick[1], fclick[0], sclick[0], sclick[1]]

        return [999, 999, 999, 999, 999]
    else:
        return [999, 999, 999, 999, 999]


def promhighlights():
    for y in range(4):
        rect = pg.Rect(575, 60 + (y * 50 * 1.05), 80, 25)
        pg.draw.rect(SCREEN, (0, 230, 0), rect, 5)

    prombox = pg.Rect(570, 11 + (0 * 50 * 1.05), 114, 237)
    pg.draw.rect(SCREEN, (0, 200, 0), prombox, 3)


def gamestatusbox():
    POKEFONT = pg.font.Font("./media/8-Bit Madness.ttf", 25)
    gstatbox = pg.Rect(140, 570, 280, 90)
    pg.draw.rect(SCREEN, LIGHTBROWN, gstatbox)
    SCREEN.blit(POKEFONT.render('Condition:', True, (0, 0, 0)), (142, 573))


def gamestatustext(chboard, turn, boardhistlist, movehistlist):
    POKEFONT = pg.font.Font("./media/8-Bit Madness.ttf", 35)
    if ch.checkcheck(chboard, turn, movehistlist) == True:
        if turn == 1:
            SCREEN.blit(POKEFONT.render('White Check', True, ORANGE), (195, 607))
        elif turn == 2:
            SCREEN.blit(POKEFONT.render('Black Check', True, ORANGE), (195, 607))
    else:
        return


def drawundobutton():
    POKEFONT = pg.font.Font("./media/8-Bit Madness.ttf", 32)
    undo = pg.Rect(570, 260 + (0 * 50 * 1.05), 115, 30)
    pg.draw.rect(SCREEN, (139,62,47), undo)
    SCREEN.blit(POKEFONT.render('U N D O', True, (0, 0, 0)), (588, 265))


#### RUNS THE GAME ####

main()