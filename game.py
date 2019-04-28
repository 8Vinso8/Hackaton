import pygame
import random

from pygame.locals import *

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

is_next_move_left = True
boss_image = 'boss.png'
bullet_images = ['bullet1.png', 'bullet2.png']
enemy_images = ['enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png']
background_images = {'back1.png', 'back2.png', 'back3.png'}
boss_fight_background = 'boss_fight_back.png'
death_screen = 'death.png'

# Загрузка звуков
start_sound = pygame.mixer.Sound('start.wav')
soundtrack = pygame.mixer.Sound('soundtrack.wav')
soundtrack.set_volume(0.2)
shoot_sound = pygame.mixer.Sound('shoot.wav')
shoot_sound.set_volume(0.8)
hit_sound = pygame.mixer.Sound('hit.wav')

boss_res = (120, 172)
player_res = (93, 60)
enemy_res = (60, 93)
bullet_res = (15, 48)

difficult = 1
back = 0
new_level = True
score = 0  # В начало
green = (0, 255, 0)
red = (255, 0, 0)
score_font = pygame.font.SysFont(None, 75)
score_text = 'SCORE:'
hp_text = 'ФБК'
hp_font = pygame.font.SysFont(None, 75)
death_text = 'НАЖМИТЕ R ЧТОБЫ ЗАПЛАТИТЬ НОЛОГ ИЛИ ESC ЧТОБЫ ОТСИДЕТЬ'
death_font = pygame.font.SysFont(None, 50)


def create_enemy(line, n):
    y = 100 * line
    x = 100 * n
    enemies[line].append(Enemy((x, y), random.choice(enemy_images), enemy_res))


def collision(rect1, rect2):
    return rect1.colliderect(rect2)


def shoot(pos, res, is_friendly):
    if is_friendly:
        friendly_bullets.append(FriendlyBullet((pos[0] + res[0] // 2, pos[1] + res[1] // 2 - 90),
                                               bullet_images[0]))
        shoot_sound.play()
    else:
        enemy_bullets.append(EnemyBullet((pos[0] + res[0] // 2, pos[1] + res[1] // 2),
                                         bullet_images[1]))


class Thing:
    def __init__(self, pos, image, res):
        self.resolution = res
        self.position = pos  # (X, Y)
        self.image = pygame.image.load(image).convert()
        self.image_surf = self.image
        self.image_surf.set_colorkey((0, 0, 0))

    def draw(self):
        self.image_rect = self.image_surf.get_rect(
            bottomright=(self.position[0] + self.resolution[0],
                         self.position[1] + self.resolution[1]))
        window.blit(self.image_surf, self.image_rect)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.resolution[0], self.resolution[1])

    def move(self, x, y):  # X, y - перемещение по x и y
        self.position = (self.position[0] + x, self.position[1] + y)


class FriendlyBullet(Thing):
    def __init__(self, pos, image):
        super().__init__(pos, image, bullet_res)

    def move(self, x, y):  # X, y - перемещение по x и y
        if self.get_y() < -50:
            friendly_bullets.pop(0)
        else:
            super().move(x, y)


class EnemyBullet(Thing):
    def __init__(self, pos, image, ):
        super().__init__(pos, image, bullet_res)

    def move(self, x, y):  # X, y - перемещение по x и y
        if self.get_y() > 950:
            enemy_bullets.pop(0)
        else:
            super().move(x, y)


class Enemy(Thing):
    pass


class Player(Thing):
    def __init__(self, pos, image, res, health):
        self.health = health
        super().__init__(pos, image, res)

    def dmg(self, n):
        self.health -= n

    def get_health(self):
        return self.health


class Boss(Player):
    def draw(self):
        global angle
        angle += 30
        self.image_surf = pygame.transform.rotate(self.image, angle % 360)  # Image_name.png
        self.image_surf.set_colorkey((0, 0, 0))
        super().draw()


enemies = [[], [], [], []]
friendly_bullets = list()
enemy_bullets = list()
bosses = []
delay = 10
x = delay
angle = 0
blue = 0, 191, 255
resolution = 1600, 900
fullscreen = True
working = True
is_boss_fight = False

window: pygame.Surface = pygame.display.set_mode(resolution, FULLSCREEN)
pygame.display.set_caption('Kremlin Travel')

player = Player([800, 700], 'player.png', player_res, 3)
start_sound.play()
pygame.time.delay(1000)
death_screen = Thing((0, 0), death_screen, (1600, 900))
soundtrack.play()
while working:
    # Обработка нажатий
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
            if event.key == K_SPACE and x == delay:
                shoot(player.position, player.resolution, True)
                x = 0
            if event.key == K_f:
                player.dmg(-100000)
            if event.key == K_g:
                enemies = [[], [], [], []]
                enemy_bullets = list()
                if is_boss_fight:
                    for boss in bosses:
                        boss.health = 0
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        if not player.get_x() - 10 <= 0:
            player.move(-20, 0)
    if keys[K_d]:
        if not player.get_x() + player.resolution[0] + 10 >= 1600:
            player.move(20, 0)
    if keys[K_w]:
        if not player.get_y() - 5 <= 600:
            player.move(0, -10)
    if keys[K_s]:
        if not player.get_y() + player.resolution[1] + 5 >= 900:
            player.move(0, 10)

    # Работа с фонами и этапами
    if not any(enemies) and not is_boss_fight:
        if back == 9:
            if difficult < 4:
                for i in range(difficult):
                    bosses.append(Boss([800 + random.randint(-400, 400), 50], boss_image, boss_res, 2 + difficult))
            else:
                for i in range(4):
                    bosses.append(Boss([800 + random.randint(-400, 400), 50], boss_image, boss_res, 2 + difficult))
            is_boss_fight = True
            background = Thing((0, 0), boss_fight_background, (1600, 900))
        else:
            if back % 3 == 0 and background_images:
                background = Thing((0, 0), background_images.pop(), (1600, 900))
            if difficult < 4:
                for i in range(difficult):
                    for j in range(random.randint(1, 9)):
                        create_enemy(i, j)
            else:
                for i in range(4):
                    for j in range(random.randint(1, 12)):
                        create_enemy(i, j)
        back += 1
    if not working:
        break

    # Начинается отрисовка
    background.draw()

    for i in friendly_bullets:
        i.draw()
        for j in enemies.copy():
            for enemy in j:
                if collision(i.get_rect(), enemy.get_rect()):
                    j.remove(enemy)
                    if i in friendly_bullets:
                        friendly_bullets.remove(i)
                    score += 10
        if is_boss_fight:
            if collision(i.get_rect(), boss.get_rect()):
                boss.dmg(1)
                if i in friendly_bullets:
                    friendly_bullets.remove(i)
        i.move(0, -25)

    for i in enemy_bullets:
        i.draw()
        if collision(i.get_rect(), player.get_rect()):
            player.dmg(1)
            hit_sound.play()
            enemy_bullets.remove(i)
        i.move(0, 5)

    for i in enemies:
        for j in i:
            j.draw()
            if random.randint(0, 100) == 100:
                shoot(j.position, j.resolution, False)
    if is_boss_fight:
        for boss in bosses:
            boss.draw()
            if is_next_move_left:
                if boss.get_x() - 30 >= 0:
                    boss.move(-30, 0)
                else:
                    is_next_move_left = False
            else:
                if boss.get_x() + 150 <= resolution[0]:
                    boss.move(30, 0)
                else:
                    is_next_move_left = True
            if random.randint(0, 2 + difficult) == 0:
                shoot((boss.position[0] + random.randint(-100, 100),
                       boss.position[1]), boss.resolution, False)
    player.draw()

    if any(enemies):
        for i in enemies:
            if is_next_move_left:
                if all(list(_[0].get_x() - 10 >= 0 for _ in list(filter(lambda o: o, enemies)))):
                    for enemy in i:
                        enemy.move(-10, 0)
                else:
                    is_next_move_left = False
            else:
                if all(list(_[-1].get_x() + 70 <= resolution[0] for _ in list(filter(lambda o: o, enemies)))):
                    for enemy in i:
                        enemy.move(10, 0)
                else:
                    is_next_move_left = True

    if x < delay:
        x += 1
    while player.get_health() <= 0:
        soundtrack.stop()
        back = 0
        death_screen.draw()
        death_image = death_font.render(death_text, 0, (128, 0, 128))
        window.blit(death_image, (200, 450))
        score_image = score_font.render(score_text + str(score), 0, (128, 0, 128))
        window.blit(score_image, (200, 500))
        pygame.display.flip()
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
                    player.dmg(-1)
                if event.key == K_r:
                    player.dmg(-3)
                    back = 0
                    score = 0
                    friendly_bullets.clear()
                    enemy_bullets.clear()
                    enemies = [[], [], [], []]
                    background_images = {'back1.png', 'back2.png', 'back3.png'}
                    soundtrack.play(-1)

    if is_boss_fight:
        for boss in bosses:
            if boss.get_health() == 0:
                bosses.remove(boss)
        if not bosses:
            difficult += 1
            is_boss_fight = False
            back = 0
            friendly_bullets.clear()
            enemy_bullets.clear()
            enemies = [[], [], [], []]
            score += 200
            player.dmg(-1)
            background_images = {'back1.png', 'back2.png', 'back3.png'}

    score_image = score_font.render(score_text + str(score), 0, red)
    health_text = hp_text[:player.get_health()]
    hp_image = hp_font.render(health_text, 0, red)
    window.blit(score_image, (0, 800))
    window.blit(hp_image, (1400, 800))
    pygame.display.flip()
    pygame.time.Clock().tick(120)

pygame.quit()