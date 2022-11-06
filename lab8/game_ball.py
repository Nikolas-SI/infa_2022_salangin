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

def new_ball():
    global x, y, r, v_x, v_y, color
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    v_x = randint(-20, 20)
    v_y = randint(-20, 20)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r, v_x, v_y, color

def click_in_ball(event,x,y,r):
    event.x = event.pos[0]
    event.y = event.pos[1]
    if (event.x - x)*2 + (event.y - y)**2 < r**2:
        return True
    else:
        return False

def new_ball_position(x, y, r, v_x, v_y, color):
    x += v_x
    y += v_y
    if x + r >= 1000:
        x = 1000 - r
        v_x = -v_x
        x += v_x
    if y + r >= 600:
        y = 600 - r
        v_y = -v_y
        y += v_y
    if y - r <= 0:
        y = r
        v_y = -v_y
        y += v_y
    if x - r <= 0:
        x = r
        v_x = -v_x
        x += v_x
    # color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r, v_x, v_y, color

pygame.display.update()
clock = pygame.time.Clock()
finished = False

x1, y1, r1, v_x1, v_y1, color1 = new_ball()
x2, y2, r2, v_x2, v_y2, color2 = new_ball()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_in_ball(event, x1, y1, r1):
                count += 1
                print(count)
            if click_in_ball(event, x2, y2, r2):
                count += 1
                print(count)
            # else:
            #     finished = True
    x1, y1, r1, v_x1, v_y1, color1 = new_ball_position(x1, y1, r1, v_x1, v_y1, color1)
    x2, y2, r2, v_x2, v_y2, color2 = new_ball_position(x2, y2, r2, v_x2, v_y2, color2)
    pygame.display.update()
    screen.fill(BLACK)


pygame.quit()