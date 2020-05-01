import Chess_vs_human as chh
import Chess_vs_ai as cha
import numpy as np
import pygame as pg
import sys

BLACK = pg.Color('grey')
WHITE = pg.Color('white')
GREEN = (0,90,0)
OLIVEGREEN = (19, 122, 0)
FORESTGREEN = (0,50,0)
LIGHTBROWN = (205,192,176)
LEMON = (238,233,191)
ORANGE = (238,64,0)
CRIMSON = (220,20,60)

CODERShist = pg.font.Font("./media/Coder's Crux.ttf", 27)

screen_width = 850
screen_height = 673


def menu():
    global MSCREEN
    pg.init()
    pg.display.set_caption('Chess by bryanlzl')
    MSCREEN = pg.display.set_mode((screen_width, screen_height))
    MSCREEN.fill(FORESTGREEN)

    pg.event.set_blocked([pg.MOUSEMOTION, pg.MOUSEBUTTONUP])

    while True:
        menuoptions()
        decors()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()


def menuoptions():
    vsai = pg.Rect(310, 450, 230, 50)
    playhumanvshuman = pg.Rect(310, 550, 230, 50)
    pg.draw.rect(MSCREEN, (179, 179, 179), vsai)
    pg.draw.rect(MSCREEN, (179, 179, 179), playhumanvshuman)


def decors():
    white_knight = pg.image.load("./media/white_knight.png")
    black_knight = pg.image.load("./media/black_knight.png")
    whiteknight = pg.transform.flip(white_knight, True, False)
    MSCREEN.blit(pg.transform.scale(black_knight, (150, 150)), (610, 127))
    MSCREEN.blit(pg.transform.scale(whiteknight, (160, 160)), (80, 125))

#### RUN THE GAME ####

menu()
