import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
screen = pygame.display.set_mode((1000, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

count = 0


def new_rect():
    """Рисует прямоугольник и возвращает его координаты и скорости"""
    x = randint(20, 400)
    y = randint(20, 400)
    a = 100
    b = 50
    color = COLORS[randint(0, 5)]
    rect(screen, color, (x, y, a, b))
    v_x = 2
    v_y = 2
    return x, y, a, b, v_x, v_y


def new_rect_position(x, y, a, b, v_x, v_y):
    """ Возвращает новые координаты прямоугольника при движении и рисует его.
    x, y - координаты левого верхнего угла прямоугольника
    a, b - длина и ширина
    v_x, v_y - проекции скорости на оси
    """
    x += v_x
    y += v_y
    if x + a >= 1000:
        x = 1000 - a
        v_x = - v_x
        x += v_x
        v_y = randint(-40, 40)
    if y + b >= 600:
        y = 600 - b
        v_y = - v_y
        y += v_y
        v_x = randint(-40, 40)
    if x <= 0:
        x = 0
        v_x = -v_x
        x += v_x
    if y <= 0:
        y = 0
        v_y = -v_y
        y += v_y
    color = COLORS[randint(0, 5)]
    rect(screen, color, (x, y, a, b))
    return x, y, a, b, v_x, v_y


def click_in_rect(eve, x, y, a, b):
    """ Проверяет попал ли игрок в прямоугольник.
    eve - событие из модуля pygame
    x, y - координаты левого верхнего угла прямоугольника
    a, b - длина и ширина
    """
    eve.x = eve.pos[0]
    eve.y = eve.pos[1]
    if x+a > eve.x > x and y < eve.y < y + b:
        return True
    else:
        return False


def new_ball():
    """Рисует круг и возвращает его координаты, скорости и цвет"""
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    v_x = randint(-20, 20)
    v_y = randint(-20, 20)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r, v_x, v_y, color


def click_in_ball(eve, x, y, r):
    """ Проверяет попал ли игрок в круг.
    eve - событие из модуля pygame
    x, y - координаты центра круга
    r - радиус круга
    """
    eve.x = eve.pos[0]
    eve.y = eve.pos[1]
    if (eve.x - x) * 2 + (eve.y - y) ** 2 < r ** 2:
        return True
    else:
        return False


def new_ball_position(x, y, r, v_x, v_y, color):
    """ Возвращает новые координаты круга при движении и рисует его.
    x, y - координаты центра круга
    r - радиус круга
    v_x, v_y - проекции скорости на оси
    color -  color - цвет, заданный в формате, подходящем для pygame.Color
    """
    x += v_x
    y += v_y
    if x + r >= 1000:
        x = 1000 - r
        v_x = -v_x
        x += v_x
        v_y = randint(-20, 20)
    if y + r >= 600:
        y = 600 - r
        v_y = -v_y
        y += v_y
        v_x = randint(-20, 20)
    if y - r <= 0:
        y = r
        v_y = -v_y
        y += v_y
        v_x = randint(-20, 20)
    if x - r <= 0:
        x = r
        v_x = -v_x
        x += v_x
        v_y = randint(-20, 20)
    # color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r, v_x, v_y, color


pygame.display.update()
clock = pygame.time.Clock()
finished = False

rect_x1, rect_y1, rect_a1, rect_b1, v_rect_x1, v_rect_y1 = new_rect()
x1, y1, r1, v_x1, v_y1, color1 = new_ball()
x2, y2, r2, v_x2, v_y2, color2 = new_ball()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if count == -1:
                finished = True
            else:
                if click_in_ball(event, x1, y1, r1):
                    count += 1
                elif click_in_ball(event, x2, y2, r2):
                    count += 1
                elif click_in_rect(event, rect_x1, rect_y1, rect_a1, rect_b1):
                    count += 5
                else:
                    count -= 1
                print(count)

    rect_x1, rect_y1, rect_a1, rect_b1, v_rect_x1, v_rect_y1 = new_rect_position(rect_x1, rect_y1, rect_a1, rect_b1,
                                                                                 v_rect_x1, v_rect_y1)
    x1, y1, r1, v_x1, v_y1, color1 = new_ball_position(x1, y1, r1, v_x1, v_y1, color1)
    x2, y2, r2, v_x2, v_y2, color2 = new_ball_position(x2, y2, r2, v_x2, v_y2, color2)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
