import pygame
from pygame.locals import *
#self.rect = pygame.Rect(pos[0], pos[1], res[0], res[1])

is_next_move_left = True
bullet_images = 'bullet1.png, bullet2.png'
enemy_images = ['enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png']
background_images = ['back1.png', 'back2.png', 'back3.png']
player_res = (93, 60)
enemy_res = (60, 93)
bullet_res = (15, 48)


def shoot(pos, res):
    bullets.append(bullet((pos[0] + res[0] // 2, pos[1] + res[1] // 2), 'bullet.png', 5))


def move_all():
    if Enemy.is_next_move_left:
        if Enemy.enemies[0].get_x() - 70 >= 0:
            for i in Enemy.enemies:
                i.move(-10, 0)
        else:
            Enemy.is_next_move_left = False
    else:
        if Enemy.enemies[-1].get_x() + 10 <= resolution[0]:
            for i in Enemy.enemies:
                i.move(10, 0)
        else:
            Enemy.is_next_move_left = True


class Thing:
    def __init__(self, pos, image, res):
        self.resolution = res
        self.position = pos  # (X, Y)
        self.image = pygame.image.load(image).convert()  # Image_name.png
        self.image.set_colorkey((0, 0, 0))

    def draw(self):
        self.image_rect = self.image.get_rect(bottomright=(self.position[0] + self.resolution[0],
                                                           self.position[1] + self.resolution[1]))
        window.blit(self.image, self.image_rect)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.resolution[0], self.resolution[1])

    def move(self, x, y):  # X, y - перемещение по x и y
        self.position = (self.position[0] + x, self.position[1] + y)


class bullet(Thing):
    def __init__(self, pos, image, speed):
        self.speed = speed
        super().__init__(pos, image, bullet_res)

    def move(self, x, y):  # X, y - перемещение по x и y
        if self.get_y() < -50 or self.get_y() > 950:
            bullets.pop(0)
        else:
            super().move(x, y)


class Enemy(Thing):
    enemies = list()

    def __init__(self, pos, image, res):
        Enemy.enemies.append(self)
        super().__init__(pos, image, res)


class Player(Thing):
    def __init__(self, pos, image, res, health):
        self.health = health
        super().__init__(pos, image, res)


def collision(rect1, rect2):
    return rect1.colliderect(rect2)


blue = 0, 191, 255


resolution = 1600, 900
window: pygame.Surface = pygame.display.set_mode(resolution, FULLSCREEN)
fullscreen = True
pygame.display.set_caption('Kremlin Travel')
working = True
bullets = list()
player = Player([800, 700], 'player.png', player_res, 100)
phone = Thing((0, 0), background_images[0], (1600, 900))
while working:
    for event in pygame.event.get():
        if event.type == QUIT:
            working = False
        if event.type == KEYDOWN:
            if event.key == K_F1:
                if fullscreen:
                    window: pygame.Surface = pygame.display.set_mode(resolution)
                    fullscreen = False
                else:
                    window: pygame.Surface = pygame.display.set_mode(resolution, FULLSCREEN)
                    fullscreen = True
            if event.key == K_ESCAPE:
                working = False
            if event.key == K_SPACE:
                shoot(player.position, player.resolution)
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        if not player.get_x() - 10 <= 0:
            player.move(-10, 0)
    if keys[K_d]:
        if not player.get_x() + player.resolution[0] + 10 >= 1600:
            player.move(10, 0)
    if keys[K_w]:
        if not player.get_y() - 5 <= 700:
            player.move(0, -5)
    if keys[K_s]:
        if not player.get_y() + player.resolution[1] + 5 >= 900:
            player.move(0, 5)
    phone.draw()
    player.draw()
    for i in bullets:
        i.draw()
        i.move(0, -10)
    pygame.display.update()
    pygame.time.Clock().tick(120)
pygame.quit()