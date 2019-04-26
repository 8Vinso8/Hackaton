import pygame as pg


res = 600, 600
win = pg.display.set_mode(res)
pg.display.set_caption('Drawing')
green = (0, 255, 0)
black = (0, 0, 0)
working = True
blue = (0, 0, 200)
yellow = (255, 255, 0)
win.fill(blue)
pg.draw.ellipse(win, yellow, pg.Rect(450, 0, 150, 150))
pg.draw.rect(win, green, pg.Rect(0, 500, 600, 100))
pg.draw.rect(win, black, pg.Rect(200, 300, 200, 200))
pg.draw.polygon(win, yellow, ((200, 300), (400, 300), (300, 250)))
pg.draw.line(win, black, (450, 500), (475, 400), 2)
pg.draw.line(win, black, (475, 400), (500, 500), 2)
pg.draw.line(win, black, (475, 400), (475, 350), 2)
pg.draw.circle(win, black, (475, 325), 25)
pg.draw.line(win, black, (475, 350), (500, 375), 5)
pg.draw.line(win, black, (475, 350), (450, 375), 5)
pg.display.update()
while working:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            working = False
