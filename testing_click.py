import os, pygame
from pygame.locals import *
from sys import exit
from random import *
__author__ = {'name': 'Hongten',
              'mail': 'hongtenzone@foxmail.com',
              'Version': '1.0'}
if not pygame.font:
    print('Warning, Can not found font!')
pygame.init()
screen = pygame.display.set_mode((255, 255), 0, 32)
screen.fill((255, 255, 255))
font = pygame.font.SysFont('inconsolata', 22)
text = font.render('Cliked Me please!!!', True, (34, 252, 43))
mouse_x, mouse_y = 0, 0
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed(num_buttons=3)
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index == 0:
                        print('Pressed LEFT Button!')
                    elif index == 1:
                        print('The mouse wheel Pressed!')
                    elif index == 2:
                        print('Pressed RIGHT Button!')
        elif event.type == MOUSEMOTION:
            # return the X and Y position of the mouse cursor
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
    screen.fill((mouse_x, mouse_y, 0))
    screen.blit(text, (40, 100))
    pygame.display.update()
