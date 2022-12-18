import math
from random import choice
from random import randint
import pygame
import numpy as np
from sympy.core.evalf import rnd

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
g = 1

number_of_targets = 10
number_of_bombs = 10

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball
        Args:
        screen - экран
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 60

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна.
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += g
        if self.bottom_collision():
            self.vy = - self.vy
            self.vy += g
        elif self.sidewalk_collision():
            self.vx = -self.vx

    def bottom_collision(self):
        if self.y + self.r >= HEIGHT:
            return True

    def sidewalk_collision(self):
        if self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            return True
        if self.x - self.r <= 0:
            self.x = 0 + self.r
            return True

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** 0.5 <= self.r + obj.r


class Gun:
    def __init__(self, screen, x_start=40, y_start=450):
        self.screen = screen
        self.f2_power = 30
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.width = 7
        self.x_start = x_start
        self.y_start = y_start

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x_start, self.y_start)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = 2 * self.f2_power * math.cos(self.an)
        new_ball.vy = 2 * self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        delta_x = event.pos[0] - self.x_start
        delta_y = event.pos[1] - self.y_start
        h = (delta_y ** 2 + delta_x ** 2) ** 0.5
        if delta_x == 0:
            delta_x = 0.001
        if event:
            self.an = -math.acos(delta_x / h)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw_gun(self):
        x_end = self.x_start + self.f2_power * math.cos(self.an)
        y_end = self.y_start + self.f2_power * math.sin(self.an)
        pygame.draw.line(self.screen, self.color, (self.x_start, self.y_start), (x_end, y_end), self.width)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 10000:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Bomb():
    def __init__(self):
        self.x = randint(2, WIDTH)
        self.y = 0
        self.r = 5
        self.color = MAGENTA
        self.speed = randint(5, 20)
        self.live = 1

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        self.y += self.speed
        if self.y >= HEIGHT:
            self.live = 0

    def hittest_with_tank(self, obj):
        return not (self.x - obj.x - obj.length > self.r or self.x - obj.x < - self.r) and obj.y - self.y < self.r


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(0, 780)
        self.y = randint(0, 550)
        self.r = randint(2, 50)
        self.color = RED
        self.vx = randint(-20, 30)
        self.vy = randint(-20, 30)
        self.live = 1

    def hit(self, points=1):
        global score, max_score
        """Попадание шарика в цель."""
        self.points += points
        score += points
        if score > max_score:
            max_score = score

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx
            self.x += self.vx
        if self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -self.vy
            self.y += self.vy
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy
            self.y += self.vy
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx
            self.x += self.vx

    def hittest_with_tank(self, obj):
        global score
        if not (self.x - obj.x - obj.length > self.r or self.x - obj.x < - self.r) and obj.y - self.y < self.r:
            score -= 1


class Tank(Gun):
    def __init__(self, screen):
        super().__init__(screen)
        self.x = 0
        self.width = 10
        self.y = HEIGHT - self.width
        self.length = 30
        self.k_right_on = 0
        self.k_left_on = 0
        self.speed = 10
        self.x_start = self.x + self.length / 2
        self.y_start = self.y
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.width = 7

    def k_right_down(self):
        self.k_right_on = 1

    def k_left_down(self):
        self.k_left_on = 1

    def k_right_up(self):
        self.k_right_on = 0

    def k_left_up(self):
        self.k_left_on = 0

    def move(self):
        if self.x + self.length >= WIDTH:
            self.k_right_on = 0
        if self.x <= 0:
            self.k_left_on = 0
        if self.k_right_on:
            self.x += self.speed
            self.x_start += self.speed
        elif self.k_left_on:
            self.x -= self.speed
            self.x_start -= self.speed

    def draw_body(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.length, self.width))


pygame.init()
name = input("Your name: ")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f = pygame.font.SysFont('arial', 20)
score = 0
sc_text = f.render("счет: {}".format(score), 1, BLACK, (255, 255, 255))
pos = sc_text.get_rect(center=(30, 30))
bullet = 0
balls = []
targets = []
bombs = []
clock = pygame.time.Clock()
# gun = Gun(screen)
tank = Tank(screen)
for i in range(0, number_of_bombs):
    bombs.append(Bomb())
for i in range(0, number_of_targets):
    targets.append(Target())
finished = False
max_score = 0
sc = 0
while not finished:
    sc_text = f.render("счёт: {}".format(score), 1, BLACK, (255, 255, 255))
    screen.fill(WHITE)
    # gun.draw()
    tank.draw_body()
    tank.draw_gun()
    tank.move()
    screen.blit(sc_text, pos)
    for bomb in bombs:
        bomb.move()
        bomb.draw()
    for target in targets:
        target.move()
        target.draw()
    for b in balls:
        b.draw()
        b.live -= 1
        if not b.live:
            balls.remove(b)
    pygame.display.update()

    for target in targets:
        finished = target.hittest_with_tank(tank)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            tank.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                tank.k_right_down()
            if event.key == pygame.K_a:
                tank.k_left_down()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                tank.k_right_up()
            elif event.key == pygame.K_a:
                tank.k_left_up()

    for bomb in bombs:
        if bomb.hittest_with_tank(tank):
            bomb.live = 0
            score -= 1
            if score < 0:
                finished = True

    for bomb in bombs:
        if bomb.live == 0:
            bombs.remove(bomb)
            bombs.append(Bomb())

    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
    tank.power_up()
    if score < 0:
        finished = True


f = open('score.txt', 'a')
f.writelines(f"{name}: {max_score} \n")
pygame.quit()

