import Chess_vs_human as chh
import Chess_vs_ai as cha
import pygame as pg
import sys

BLACK = pg.Color('grey')
WHITE = pg.Color('white')
GREEN = (0,90,0)
LIGHTGREEN = (127,255,0)
OLIVEGREEN = (19, 122, 0)
FORESTGREEN = (0,50,0)
LIGHTBROWN = (205,192,176)
LEMON = (238,233,191)
ORANGE = (238,64,0)
RED = (255,48,48)
CRIMSON = (220,20,60)

CODERSFONT = pg.font.Font("./media/Coder's Crux.ttf", 27)
POKEFONT = pg.font.Font("./media/8-Bit Madness.ttf", 35)

screen_width = 850
screen_height = 673


def menu():
    global MSCREEN
    pg.init()
    pg.display.set_caption('Chess by bryanlzl')
    MSCREEN = pg.display.set_mode((screen_width, screen_height))
    playerselected = 0
    aiselected = -1
    turnselected = -1
    gamesettings = []

    pg.event.set_blocked([pg.MOUSEMOTION, pg.MOUSEBUTTONUP])

    while True:
        MSCREEN.fill(FORESTGREEN)
        menuoptiondisplay()
        decorsntitle()

        if playerselected == 1:
            popup1p()

        elif playerselected == 2:
            popup2p()

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN and playerselected == 0:
                playerselected = playbuttonselect()
                continue

            if event.type == pg.MOUSEBUTTONDOWN and (playerselected == 1 or playerselected == 2):
                if pg.Rect(150, 370, 550, 200).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == False: # if click anywhere outside the popup box
                    playerselected = 0
                    aiselected = -1
                    turnselected = -1

            if event.type == pg.MOUSEBUTTONDOWN and playerselected == 1 and aiselected == -1 and turnselected == -1: # SINGLE PLAYER/AI SELECT
                if pg.Rect(150, 370, 550, 200).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True:
                    if pg.Rect(200, 422, 140, 30).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True: # AI LEVEL 0
                        aiselected = 0
                        continue
                    elif pg.Rect(200, 457, 140, 30).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True:  # AI LEVEL 1
                        aiselected = 1
                        continue
                    elif pg.Rect(200, 492, 140, 30).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True:  # AI LEVEL 2
                        aiselected = 2
                        continue
                    elif pg.Rect(200, 527, 140, 30).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True:  # AI LEVEL 3
                        aiselected = 3
                        continue
                    else:
                        aiselected = -1
                        continue
                else:
                    aiselected = -1
                    continue

            elif event.type == pg.MOUSEBUTTONDOWN and playerselected == 1 and aiselected != -1 and turnselected == -1: # SINGLE PLAYER/AI SELECT/AI TURN
                if pg.Rect(150, 370, 550, 200).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True:
                    if pg.Rect(348, 422, 109, 65).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True: # choosing AI turn
                        turnselected = 0
                    elif pg.Rect(348, 492, 109, 65).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True: # choosing AI turn
                        turnselected = 1
                    else:
                        turnselected = -1
                        aiselected = -1
                        continue
                else:
                    turnselected = -1
                    aiselected = -1
                    continue

            elif event.type == pg.MOUSEBUTTONDOWN and playerselected == 1 and aiselected != -1 and turnselected != -1:  # SINGLE PLAYER/AI SELECT/AI TURN/START GAME
                if pg.Rect(150, 370, 550, 200).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True:
                    if pg.Rect(465, 422, 191, 135).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True: # Start vs AI game mode
                        if aiselected != 2 and aiselected != 3:
                            gamesettings.append(aiselected)
                            gamesettings.append(turnselected)
                            turnselected = -1
                            aiselected = -1
                            cha.main(gamesettings[0], gamesettings[1])
                            ########## WORK IN PROGRESS ON WHAT TO DO NEXT ##########
                        else:
                            turnselected = -1
                            aiselected = -1
                            continue
                    else:
                        turnselected = -1
                        aiselected = -1
                        continue
                else:
                    turnselected = -1
                    aiselected = -1
                    continue

            if event.type == pg.MOUSEBUTTONDOWN and playerselected == 2: # TWO PLAYER/YES OR NO
                if pg.Rect(150, 370, 550, 200).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True:
                    if pg.Rect(348, 422, 109, 65).collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]) == True: # yes selected
                        playerselected = 0
                        chh.main()
                        ########## WORK IN PROGRESS ON WHAT TO DO NEXT ##########
                    else:
                        playerselected = 0
                        continue
                else:
                    playerselected = 0
                    continue

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        clickhighlights(playerselected, aiselected, turnselected)

        pg.display.update()


def menuoptiondisplay():
    selecttext = pg.font.Font("./media/8-Bit Madness.ttf", 55)
    vsai = pg.Rect(275, 375, 300, 65)
    playhumanvshuman = pg.Rect(275, 500, 300, 65)
    pg.draw.rect(MSCREEN, (179, 179, 179), vsai)
    pg.draw.rect(MSCREEN, (179, 179, 179), playhumanvshuman)
    pg.draw.rect(MSCREEN, (0, 0, 0), vsai, 10)
    pg.draw.rect(MSCREEN, (0, 0, 0), playhumanvshuman, 10)
    MSCREEN.blit(selecttext.render('1 Player', True, (0, 0, 0)), (339, 390))
    MSCREEN.blit(selecttext.render('2 Players', True, (0, 0, 0)), (320, 515))


def decorsntitle():
    white_knight = pg.image.load("./media/white_knight.png")
    black_knight = pg.image.load("./media/black_knight.png")
    titlefont = pg.font.Font("./media/8-Bit Madness.ttf", 216)
    titlefont = pg.font.Font("./media/8-Bit Madness.ttf", 216)
    createdby = pg.font.Font("./media/Coder's Crux.ttf", 27)
    whiteknight = pg.transform.flip(white_knight, True, False)
    MSCREEN.blit(titlefont.render('CHESS', True, (0, 0, 0)), (160, 145))
    MSCREEN.blit(titlefont.render('CHESS', True, (255, 255, 255)), (160, 125))
    MSCREEN.blit(pg.transform.scale(black_knight, (155, 160)), (675, 122))
    MSCREEN.blit(pg.transform.scale(whiteknight, (150, 150)), (25, 125))
    MSCREEN.blit(createdby.render('Created by: bryanlzl', True, (255, 255, 255)), (630, 646))


def popup1p():
    readyfont1 = pg.font.Font("./media/Coder's Crux.ttf", 45)
    readyfont2 = pg.font.Font("./media/Coder's Crux.ttf", 28)

    popup = pg.Rect(150, 370, 550, 200)
    ailevel0 = pg.Rect(200, 422, 140, 30)
    ailevel1 = pg.Rect(200, 457, 140, 30)
    ailevel2 = pg.Rect(200, 492, 140, 30)
    ailevel3 = pg.Rect(200, 527, 140, 30)
    aiturnselect0 = pg.Rect(348, 422, 109, 65)
    aiturnselect1 = pg.Rect(348, 492, 109, 65)
    startaigame = pg.Rect(465, 422, 191, 135)

    pg.draw.rect(MSCREEN, (69, 139, 0), popup)
    pg.draw.rect(MSCREEN, (0, 0, 0), popup, 10)
    pg.draw.rect(MSCREEN, LEMON, ailevel0)
    pg.draw.rect(MSCREEN, LEMON, ailevel1)
    pg.draw.rect(MSCREEN, LEMON, ailevel2)
    pg.draw.rect(MSCREEN, LEMON, ailevel3)
    pg.draw.rect(MSCREEN, (0, 0, 0), ailevel0, 5)
    pg.draw.rect(MSCREEN, (0, 0, 0), ailevel1, 5)
    pg.draw.rect(MSCREEN, (0, 0, 0), ailevel2, 5)
    pg.draw.rect(MSCREEN, (0, 0, 0), ailevel3, 5)
    pg.draw.rect(MSCREEN, LEMON, aiturnselect0)
    pg.draw.rect(MSCREEN, LEMON, aiturnselect1)
    pg.draw.rect(MSCREEN, (0, 0, 0), aiturnselect0, 5)
    pg.draw.rect(MSCREEN, (0, 0, 0), aiturnselect1, 5)
    pg.draw.rect(MSCREEN, LEMON, startaigame)
    pg.draw.rect(MSCREEN, (0, 0, 0), startaigame, 5)

    MSCREEN.blit(readyfont1.render('Select computer level', True, (0, 0, 0)), (240, 387))
    MSCREEN.blit(readyfont1.render('0', True, (0, 0, 0)), (266, 427))
    MSCREEN.blit(readyfont1.render('1', True, (0, 0, 0)), (266, 462))
    MSCREEN.blit(readyfont1.render('2', True, (0, 0, 0)), (266, 497))
    MSCREEN.blit(readyfont1.render('3', True, (0, 0, 0)), (266, 532))
    MSCREEN.blit(readyfont2.render('COM plays', True, (0, 0, 0)), (353, 436))
    MSCREEN.blit(readyfont2.render('WHITE', True, (0, 0, 0)), (375, 460))
    MSCREEN.blit(readyfont2.render('COM plays', True, (0, 0, 0)), (353, 505))
    MSCREEN.blit(readyfont2.render('BLACK', True, (0, 0, 0)), (375, 529))
    MSCREEN.blit(readyfont1.render('START GAME', True, (0, 0, 0)), (476, 480))


def popup2p():
    readyfont = pg.font.Font("./media/Coder's Crux.ttf", 47)
    popup = pg.Rect(150, 370, 550, 200)
    yespop = pg.Rect(325, 435, 200, 40)
    nopop = pg.Rect(325, 505, 200, 40)

    pg.draw.rect(MSCREEN, (69, 139, 0), popup)
    pg.draw.rect(MSCREEN, (0, 0, 0), popup, 10)
    pg.draw.rect(MSCREEN, LEMON, nopop)
    pg.draw.rect(MSCREEN, (0, 0, 0), nopop, 5)
    pg.draw.rect(MSCREEN, LEMON, yespop)
    pg.draw.rect(MSCREEN, (0, 0, 0), yespop, 5)

    MSCREEN.blit(readyfont.render('Start two player mode?', True, (0, 0, 0)), (230, 387))
    MSCREEN.blit(readyfont.render('Yes', True, (0, 0, 0)), (400, 444))
    MSCREEN.blit(readyfont.render('No', True, (0, 0, 0)), (410, 515))


def playbuttonselect():
    oneplayer = pg.Rect(275, 375, 300, 65)
    twoplayer = pg.Rect(275, 500, 300, 65)
    modeselect = pg.mouse.get_pos()
    if oneplayer.collidepoint(modeselect[0], modeselect[1]) == True:
        return 1
    elif twoplayer.collidepoint(modeselect[0], modeselect[1]) == True:
        return 2
    else:
        return 0


def clickhighlights(playerselected, aiselected, turnselected): # Highlights the selected buttons in light green
    ailevel0 = pg.Rect(200, 422, 140, 30)
    ailevel1 = pg.Rect(200, 457, 140, 30)
    ailevel2 = pg.Rect(200, 492, 140, 30)
    ailevel3 = pg.Rect(200, 527, 140, 30)
    aiturnselect0 = pg.Rect(348, 422, 109, 65)
    aiturnselect1 = pg.Rect(348, 492, 109, 65)

    if playerselected == 1: # Highlight buttons for one player option
        if aiselected == 0:
            pg.draw.rect(MSCREEN, LIGHTGREEN, ailevel0, 5)
            if turnselected == 0:
                pg.draw.rect(MSCREEN, LIGHTGREEN, aiturnselect0, 5)
            elif turnselected == 1:
                pg.draw.rect(MSCREEN, LIGHTGREEN, aiturnselect1, 5)

        elif aiselected == 1:
            pg.draw.rect(MSCREEN, LIGHTGREEN, ailevel1, 5)
            if turnselected == 0:
                pg.draw.rect(MSCREEN, LIGHTGREEN, aiturnselect0, 5)
            elif turnselected == 1:
                pg.draw.rect(MSCREEN, LIGHTGREEN, aiturnselect1, 5)

        elif aiselected == 2:
            pg.draw.rect(MSCREEN, RED, ailevel2, 5)
            if turnselected == 0:
                pg.draw.rect(MSCREEN, RED, aiturnselect0, 5)
            elif turnselected == 1:
                pg.draw.rect(MSCREEN, RED, aiturnselect1, 5)

        elif aiselected == 3:
            pg.draw.rect(MSCREEN, RED, ailevel3, 5)
            if turnselected == 0:
                pg.draw.rect(MSCREEN, RED, aiturnselect0, 5)
            elif turnselected == 1:
                pg.draw.rect(MSCREEN, RED, aiturnselect1, 5)


#### RUN THE GAME ####

menu()