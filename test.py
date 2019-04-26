import pygame as pg
from pygame.locals import *

pg.init()
end = False
res = 600, 600
win = pg.display.set_mode(res)
pg.display.set_caption('test')
yellow = (255, 255, 0)
blue = (0, 0, 255)
black = 0, 0, 0
brown = 139, 69, 19
green = 0, 255, 0
x, y = 500, 400


def house_col(x, y):
    return pg.Rect.colliderect(pg.Rect(x - 25, y - 25, 50, 75), pg.Rect(200, 300, 200, 100))


while not end:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            end = True
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
    pg.draw.polygon(win, brown, ((200, 300), (400, 300), (300, 200)))
    pg.draw.circle(win, yellow, (600, 0), 100)
    pg.draw.rect(win, brown, ((200, 300), (200, 100)))
    pg.draw.rect(win, green, ((0, 400), (600, 200)))
    pg.draw.line(win, black, (200, 300), (400, 300))
    man = pg.image.load('VV.png').convert()
    man.set_colorkey((255, 255, 255))
    man_rect = man.get_rect(bottomright=(x, y))
    win.blit(man, man_rect)
    pg.display.update()


