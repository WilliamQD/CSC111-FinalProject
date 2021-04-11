import pygame
import sys
import random
from pygame.colordict import THECOLORS
from map_graph import Map, Square
from typing import Any, Optional
from card import miniguner, charger, sniper, rocketer, doctor, nijia, \
    fireball, lightening, mine, autogun, card

pygame.init()  # 初始化pygame
size = (640, 480)  # 设置窗口
screen = pygame.display.set_mode(size)  # 显示窗口
color = THECOLORS['white']  # 设置颜色

speed = [5, 5]  # 设置移速（x， y）
clock = pygame.time.Clock()  # 设置时钟
term = 1  # 当前回合数
money = 0  # 金钱
my_hp = 100  # 我方hp
enemy_hp = 100  # 敌方hp

clicked_map = False  # 是否点击到图
clicked_card = False  # 是否点击卡片
turn_end = False  # 回合结束
marked_square = None  # 点击到的地图
selected_card = None  # 点击到的卡片

game_map_graph = Map()  # 设置地图
game_map_graph.__init__()  # 初始化6*10地图与连接

width, height = screen.get_size()  # 获取屏幕大小
square_size = (width / 12, height / 9)  # 获取单个方块大小

line_group = {}  # 管理划线的字典 key为组名，value为线的list
card_group = {}  # 管理场上士兵的字典 key为location
player_card_group = {}  # 管理玩家手上的牌 key为数字，value为card
color_group = {}  # 管理场上线条颜色，key与其类型相对应

# 加载地图图片
image_background = ...  # 加载背景图片（自制地图）

# 加载card信息
image_miniguner_info = ...
image_charger_info = ...
image_sniper_info = ...
image_rocketer_info = ...
image_doctor_info = ...
image_nijia_info = ...

# 加载地图信息
image_forest_info = ...
image_plain_info = ...
image_mountain_info = ...
image_river_info = ...
image_fire_info = ...


####################################################
# part1: draw text, line, image
####################################################
def draw_text(surface: pygame.Surface, text: str, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', 22)
    text_surface = font.render(text, True, THECOLORS['black'])
    t_width, t_height = text_surface.get_size()
    surface.blit(text_surface,
                 pygame.Rect(pos, (pos[0] + t_width, pos[1] + t_height)))


def draw_all_image() -> None:
    """draw the cards both in player_card_group and card_group.
    """
    for x in player_card_group:
        if player_card_group[x] is not None:
            location = player_card_group[x].get_real_location()
            screen.blit(player_card_group[x].images[player_card_group[x].display_mode], location)
    for y in card_group:
        if card_group[y] is not None:
            location = card_group[y].get_real_location()
            screen.blit(card_group[y].images[card_group[y].display_mode], location)


def draw_bone_map(surface: pygame.Surface) -> None:
    """draw the bone map with line.
    The map is in size of 6(+3) * 10(+2)
    """
    line_color = THECOLORS['grey']
    border_color = THECOLORS['black']
    for i in range(1, 8):
        if i == 1 or i == 7:
            pygame.draw.line(surface, border_color,
                             (0, square_size[1] * i), (width, square_size[1] * i))
        else:
            pygame.draw.line(surface, line_color, (square_size[0], square_size[1] * i),
                             (width - square_size[0], square_size[1] * i))

    for i in range(1, 12):
        pygame.draw.line(surface, line_color, (square_size[0] * i, square_size[1]),
                         (square_size[0] * i, square_size[1] * 7))


def draw_all_visual_line() -> None:
    """draw all line in line group.
    """
    for x in line_group:
        pygame.draw.line(screen, color_group[x], line_group[x][0], line_group[x][1])


def enclose_selected_card(c: card) -> None:
    """set enclosed card.
    """
    loc = c.get_real_location()
    color_group['enclosed_card_1'] = THECOLORS['blue']
    color_group['enclosed_card_2'] = THECOLORS['blue']
    color_group['enclosed_card_3'] = THECOLORS['blue']
    color_group['enclosed_card_4'] = THECOLORS['blue']
    line_group['enclosed_card_1'] = [loc, (loc[0] + 2 * square_size[0], loc[1])]
    line_group['enclosed_card_2'] = [loc, (loc[0], loc[1] + 2 * square_size[1])]
    line_group['enclosed_card_3'] = [(loc[0], loc[1] + 2 * square_size[1]),
                                     (loc[0] + 2 * square_size[0], loc[1] + 2 * square_size[1])]
    line_group['enclosed_card_4'] = [(loc[0] + 2 * square_size[0], loc[1]),
                                     (loc[0] + 2 * square_size[0], loc[1] + 2 * square_size[1])]


####################################################
# part1.1: set initialize data
####################################################
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


set_init_player_card_random()


####################################################
# part2: refresh and visualize surface, groups.
####################################################
def text_data_visualize(surface: pygame.Surface) -> None:
    """draw the text on the screen
    """
    draw_text(surface, 'Round ' + str(term), (width // 2, 0))  # 显示当前回合
    # 显示当前是否玩家行动回合
    draw_text(surface, 'Your Turn', (int(width - 1.5 * square_size[0]), int(square_size[1] // 2)))
    draw_text(surface, 'Money: ' + str(money), (0, int(square_size[1] // 2)))  # 显示金钱
    draw_text(surface, 'HP: ' + str(my_hp), (0, int(square_size[1] * 5.5)))  # 显示我方基地hp
    draw_text(surface, 'Hp: ' + str(enemy_hp),
              (int(square_size[0] * 11), int(square_size[1] * 5.5)))  # 显示敌方基地hp


def refresh_visual_image(is_card_clicked: bool, c: card) -> None:
    """refresh visual image by input.
    """
    global clicked_map, turn_end, clicked_card
    if is_card_clicked is True and clicked_map is True:
        clicked_map = False
        turn_end = True
        clicked_card = False
        (x, y) = pygame.mouse.get_pos()
        new_x = x // square_size[0] * square_size[0]
        new_y = y // square_size[1] * square_size[0]
        if square_size[0] < pygame.mouse.get_pos()[0] < square_size[0] * 11 \
                and square_size[1] < pygame.mouse.get_pos()[1] < square_size[1] * 7:
            card_group[term] = [c, (new_x, new_y)]
    draw_all_image()


###############################################
# part0: helper functions
###############################################
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


###############################################
# part3: click
###############################################
def graph_click(m: Map, event: pygame.event.Event) -> Square:
    """Return which square the player clicked.
    """
    (x, y) = event.pos
    new_x = x // square_size[0]
    new_y = y // square_size[0]
    return m.get_vertex((new_x, new_y))


def card_click(event: pygame.event.Event) -> card:
    """Return which card is clicked.
    """
    mouse_x = event.pos[0]
    square_x = (mouse_x // square_size[0]) // 2 + 1
    print(square_x)
    mark = player_card_group[int(square_x)]
    enclose_selected_card(mark)
    remove_from_player_group(player_card_group, int(square_x))
    return mark


################################################################
# part4: main game process
################################################################
while True:  # 游戏主进程
    clock.tick(60)  # 每秒执行60次
    if turn_end is True:
        term += 1
        turn_end = False
    for event in pygame.event.get():  # 获取事件
        if event.type == pygame.QUIT:  # 如果点击退出（右上角X）
            sys.exit()  # 系统退出
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 点击地图
            if square_size[0] < pygame.mouse.get_pos()[0] < square_size[0] * 11 \
                    and square_size[1] < pygame.mouse.get_pos()[1] < square_size[1] * 7:
                marked_square = graph_click(game_map_graph, event)
                clicked_map = True
            elif square_size[1] * 7 < pygame.mouse.get_pos()[1]:
                selected_card = card_click(event)
                clicked_card = True
    screen.fill(color)  # 填充颜色
    add_card_to_player_group_random()
    draw_all_visual_line()
    text_data_visualize(screen)
    refresh_visual_image(clicked_card, selected_card)
    draw_bone_map(screen)
    pygame.display.flip()  # 刷新显示

pygame.quit()
