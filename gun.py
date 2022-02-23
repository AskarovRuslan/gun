import pygame as pg
import numpy as np
from random import randint

SCREEN_SIZE = (1000, 800)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 150, 0)
MAROON = (128, 0, 0)
OLIVE = (0, 128, 128)
NAVY_BLUE = (0, 0, 128)
TARGET_COLORS = [RED, YELLOW, ORANGE]
DARK_YELLOW = (80, 60, 0)
EYES = (80, 0, 0)
FPS = 30
FONT_SIZE = 50

x = []
y = []
# SCREEN_SIZE[1] // 20 - изменений координат
a = 0
b = SCREEN_SIZE[1] // 2
for i in range(21):
    x.append(a)
    y.append(b)
    a = a + SCREEN_SIZE[0] // 20
    b = b + randint(-40, 40)
print(x)
print(y)
# pg.draw.line(screen, WHITE, (x[0], y[0]), (x[1], y[1]), 1)


# Считывание имени игрока
name_1 = input("Введите первого игрока: ")
name_2 = input("Введите второго игрока: ")

pg.init()

screen = pg.display.set_mode(SCREEN_SIZE)
SCREEN_SIZE = (SCREEN_SIZE[0], SCREEN_SIZE[1] - 100)
clock = pg.time.Clock()
screen.fill(BLACK)

pg.draw.line(screen, WHITE, (x[0], y[0]), (x[1], y[1]), 2)
pg.draw.line(screen, WHITE, (x[1], y[1]), (x[2], y[2]), 2)

font = pg.font.Font(None, FONT_SIZE)
g = 10  # ускорение свободного падения
number_of_targets = 5
counter = 0  # переменная для времени
score = 0  # счет


class Ball:
    def __init__(self, coord, v, t0):
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.coord = coord
        self.v = v
        self.r = 15
        self.live = True
        self.time = t0  # время когда заспавнили шарик

    def draw(self):
        pg.draw.circle(screen, self.color, self.coord, self.r)

    def move(self, t):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.coord с учетом скоростей self.v, силы гравитации, действующей на мяч,
        и стен по краям.
        """
        self.v = list(self.v)
        self.coord = list(self.coord)
        v_y = self.v[1] + g * (t - self.time) / FPS
        self.coord[0] = self.coord[0] + int(self.v[0])
        self.coord[1] = self.coord[1] + int(v_y)
        if self.coord[0] < self.r:
            self.coord[0] = self.r
            self.v[0] = (-1) * self.v[0]
        if self.coord[1] < self.r:
            self.coord[1] = self.r
            self.v[1] = (-1) * self.v[1]
        if self.coord[0] > SCREEN_SIZE[0] - self.r:
            self.coord[0] = SCREEN_SIZE[0] - self.r
            self.v[0] = (-1) * self.v[0]

    def hit_check(self, xy):
        (gun_x, gun_y) = xy
        (x, y) = self.coord
        distance = ((gun_x - x) ** 2 + (gun_y - y) ** 2) ** 0.5
        if distance <= (self.r + 5):
            self.live = False
            '''
            self.coords = list((randint(50, SCREEN_SIZE[0] - 50), randint(50, SCREEN_SIZE[1] - 50)))
            self.v = list((randint(0, 5), randint(0, 5)))
            self.color = TARGET_COLORS[randint(0, 2)]
            '''
            return 1
        else:
            return 0

    def __del__(self):
        del self


class Gun:
    def __init__(self, coord):
        # self.coord = (0, SCREEN_SIZE[1] // 2)
        self.coord = coord

        self.an = 0
        self.min_pow = 0
        self.max_pow = 10
        # self.power = randint(self.min_pow + 20, self.max_pow)
        self.power = 20
        # self.power = randint(10, 20)
        self.active = False

    def draw(self):
        end_pos = (
        int(self.coord[0] + self.power * 2 * np.cos(self.an)), int(self.coord[1] + self.power * 2 * np.sin(self.an)))
        pg.draw.line(screen, WHITE, self.coord, end_pos, 5)
        return end_pos

    def strike(self):
        v = (int(self.power * np.cos(self.an)), int(self.power * np.sin(self.an)))
        self.active = False
        return v

    def set_an(self, mouse_pos):
        """Прицеливание. Зависит от положения мыши."""
        self.an = np.arctan2(mouse_pos[1] - self.coord[1], mouse_pos[0] - self.coord[0])


class Target:
    def __init__(self):
        self.coords = list((randint(50, SCREEN_SIZE[0] - 50), randint(50, SCREEN_SIZE[1] - 50)))
        self.r = 30
        self.v = list((randint(0, 7), randint(0, 7)))
        self.color = TARGET_COLORS[randint(0, 2)]

    def draw(self):
        pg.draw.circle(screen, self.color, self.coords, self.r)
        pg.draw.circle(screen, WHITE, self.coords, self.r - 10)
        pg.draw.circle(screen, self.color, self.coords, self.r - 20)

    def hit_check(self, xy, ball_radius):
        (ball_x, ball_y) = xy
        (x, y) = self.coords
        distance = ((ball_x - x) ** 2 + (ball_y - y) ** 2) ** 0.5
        if distance <= (self.r + ball_radius):
            self.coords = list((randint(50, SCREEN_SIZE[0] - 50), randint(50, SCREEN_SIZE[1] - 50)))
            self.v = list((randint(0, 5), randint(0, 5)))
            self.color = TARGET_COLORS[randint(0, 2)]
            return 1
        else:
            return 0

    def move(self):
        for i in (0, 1):
            self.coords[i] = self.coords[i] + self.v[i]
        for i in (0, 1):
            if self.coords[i] < self.r:
                self.coords[i] = self.r
                self.v[i] = (-1) * self.v[i]
            elif self.coords[i] > SCREEN_SIZE[i] - self.r:
                self.coords[i] = SCREEN_SIZE[i] - self.r
                self.v[i] = (-1) * self.v[i]


def clock_and_score_renewal(time0, score0, score1):
    time_passed = int(time0 / FPS)
    if time_passed < 60:
        str_format_time = "Time: " + str(time_passed) + "s"
    else:
        str_format_time = "Time: " + str(time_passed // 60) + "m " + \
                          str(time_passed % 60) + "s"
    text_1 = font.render(name_1, True, WHITE)
    text_2 = font.render(name_2, True, WHITE)
    text2 = font.render(str_format_time, True, OLIVE)
    str_format_score = "Score: " + str(score0)
    str_format_score1 = "Score: " + str(score1)
    text3 = font.render(str_format_score, True, MAROON)
    text4 = font.render(str_format_score1, True, MAROON)
    pg.draw.rect(screen, WHITE, (0, SCREEN_SIZE[1], SCREEN_SIZE[0], 100))
    screen.blit(text2, (SCREEN_SIZE[0] * 6 // 23, SCREEN_SIZE[1] + 35))
    screen.blit(text3, (10, SCREEN_SIZE[1] + 35))
    screen.blit(text4, (SCREEN_SIZE[0] - 200, SCREEN_SIZE[1] + 35))

    screen.blit(text_1, (100, 100))
    screen.blit(text_2, (SCREEN_SIZE[0] - 200, 100))


def draw_background(color):
    screen.fill(BLACK)


target_list = list(Target() for q in range(number_of_targets))
gun_1 = Gun((x[2], y[2]))
gun_2 = Gun((x[18], y[18]))

pg.display.update()
finished = False
ball_list = []
ball_new_list = []

score_1 = 0
score_2 = 0

# font = pg.font.Font(None, 25)
# text_1 = font.render(name_1,True,WHITE)
# text_2 = font.render(name_2,True,WHITE)


player = 0
while not finished:
    clock.tick(FPS)
    counter += 1
    if counter % FPS == 0:
        EYES = (randint(0, 100), randint(0, 100), randint(0, 100))
    draw_background(EYES)
    '''
    for target in target_list:
        target.move()
        target.draw()
    '''
    gun_end = gun_1.draw()
    gun_end_2 = gun_2.draw()
    ball_new_list = []
    for ball in ball_list:
        ball.move(counter)
        # if ball.hit_check(gun_2.coord):
        #    score_1 += 1
        #    del ball
        score_1 += ball.hit_check(gun_2.coord)
        score_2 += ball.hit_check(gun_1.coord)

        '''
        for target in target_list:
            score += target.hit_check(ball.coord, ball.r)
        '''
        if ball.live:
            ball.draw()
            ball_new_list.append(ball)  # отсеивает мёртвые шары
    ball_list = ball_new_list
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEMOTION:
            if not player:
                gun_1.set_an(event.pos)
            else:
                gun_2.set_an(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if not player:
                ball_list.append(Ball(gun_end, gun_1.strike(), counter))
            else:
                ball_list.append(Ball(gun_end_2, gun_2.strike(), counter))
            player = (player + 1) % 2
    clock_and_score_renewal(counter, score_1, score_2)

    for i in range(20):
        pg.draw.line(screen, WHITE, (x[i], y[i]), (x[i + 1], y[i + 1]), 2)

    pg.display.update()

pg.quit()