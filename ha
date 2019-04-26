import pygame as pg
from pygame.locals import *


res = 600, 600
win = pg.display.set_mode(res)
pg.display.set_caption('Drawing')
green = (0, 255, 0)
black = (0, 0, 0)
working = True
blue = (0, 0, 200)
yellow = (255, 255, 0)
x, y = 475, 325
def house_col(x, y):
    return pg.Rect.colliderect(pg.Rect(x - 25, y - 25, 50, 75), pg.Rect(200, 300, 200, 200))

while working:
    for event in pg.event.get():
        if event.type == QUIT:
            working = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                if not house_col(x - 25, y) and not x - 25 <= 0:
                    x -= 25
            if event.key == K_RIGHT:
                if not house_col(x + 25, y) and not x + 25 >= 600:
                    x += 25
            if event.key == K_DOWN:
                if not house_col(x, y + 25) and not y + 50 >= 500:
                    y += 25
            if event.key == K_UP:
                if not y - 25 <= 0:
                    y -= 25

    win.fill(blue)
    pg.draw.ellipse(win, yellow, pg.Rect(450, 0, 150, 150))
    pg.draw.rect(win, green, pg.Rect(0, 500, 600, 100))
    pg.draw.rect(win, black, pg.Rect(200, 300, 200, 200))
    pg.draw.polygon(win, yellow, ((200, 300), (400, 300), (300, 250)))
    pg.draw.circle(win, black, (x, y), 25)
    pg.draw.line(win, black, (x, y + 25), (x + 25, y + 50), 5)
    pg.draw.line(win, black, (x, y + 25), (x - 25, y + 50), 5)
    pg.display.update()
