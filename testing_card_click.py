import pygame
import random
import sys
from pygame.colordict import THECOLORS
from typing import Any, Optional
from card import miniguner, charger, sniper, rocketer, doctor, nijia, \
    fireball, lightening, mine, autogun, card

player_card_group = {}

pygame.init()  # 初始化pygame
size = (640, 480)  # 设置窗口
screen = pygame.display.set_mode(size)  # 显示窗口
color = THECOLORS['white']  # 设置颜色
width, height = screen.get_size()  # 获取屏幕大小
square_size = (width / 12, height / 9)  # 获取单个方块大小
clock = pygame.time.Clock()  # 设置时钟


def set_init_player_card_random() -> None:
    """setup the card group randomly.
    """
    for key in range(1, 7):
        possible_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        chosen = random.choice(possible_choices)
        location = ((key - 1) * 2, 7)
        if chosen == 1:
            player_card_group[key] = miniguner(location)
        elif chosen == 2:
            player_card_group[key] = charger(location)
        elif chosen == 3:
            player_card_group[key] = sniper(location)
        elif chosen == 4:
            player_card_group[key] = rocketer(location)
        elif chosen == 5:
            player_card_group[key] = doctor(location)
        elif chosen == 6:
            player_card_group[key] = nijia(location)
        elif chosen == 7:
            player_card_group[key] = fireball(location)
        elif chosen == 8:
            player_card_group[key] = lightening(location)
        elif chosen == 9:
            player_card_group[key] = mine(location)
        elif chosen == 10:
            player_card_group[key] = autogun(location)


def remove_from_player_group(group: dict, key: int) -> None:
    """Set the element to None in the player group by key.
    """
    if key in group:
        group[key] = 'Hello world'


def add_card_to_player_group_random() -> None:
    """Add a card to a group.
    """
    for key in player_card_group:
        if player_card_group[key] == 'Hello world':
            print('action begin')
            possible_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            chosen = random.choice(possible_choices)
            location = (key * 2, 7)
            if chosen == 1:
                player_card_group[key] = miniguner(location)
            elif chosen == 2:
                player_card_group[key] = charger(location)
            elif chosen == 3:
                player_card_group[key] = sniper(location)
            elif chosen == 4:
                player_card_group[key] = rocketer(location)
            elif chosen == 5:
                player_card_group[key] = doctor(location)
            elif chosen == 6:
                player_card_group[key] = nijia(location)
            elif chosen == 7:
                player_card_group[key] = fireball(location)
            elif chosen == 8:
                player_card_group[key] = lightening(location)
            elif chosen == 9:
                player_card_group[key] = mine(location)
            elif chosen == 10:
                player_card_group[key] = autogun(location)
            print(player_card_group[key], player_card_group[key].location)


def card_click(event: pygame.event.Event) -> card:
    """Return which card is clicked.
    """
    x = event.pos[0]
    square_x = (x // square_size[0]) // 2 + 1
    print(square_x)
    mark = player_card_group[int(square_x)]
    remove_from_player_group(player_card_group, int(square_x))
    return mark


def draw_all_image() -> None:
    """draw the cards both in player_card_group and card_group.
    """
    for x in player_card_group:

        location = player_card_group[x].get_real_location()
        screen.blit(player_card_group[x].images[player_card_group[x].display_mode], location)


set_init_player_card_random()

while True:  # 游戏主进程
    clock.tick(60)  # 每秒执行60次
    for event in pygame.event.get():  # 获取事件
        if event.type == pygame.QUIT:  # 如果点击退出（右上角X）
            sys.exit()  # 系统退出
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_card = card_click(event)
            print(selected_card)
            clicked_card = True
    screen.fill(color)  # 填充颜色
    add_card_to_player_group_random()

    draw_all_image()
    pygame.display.flip()  # 刷新显示
