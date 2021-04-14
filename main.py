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
money = 100  # 金钱
my_hp = 100  # 我方hp
enemy_hp = 100  # 敌方hp

clicked_map = False  # 是否点击到图
clicked_card = False  # 是否点击卡片
decition_act = False  # 是否算回合
turn_end = False  # 回合结束
marked_square = None  # 点击到的地图
selected_card = None  # 点击到的卡片

game_map_graph = Map()  # 设置地图
game_map_graph.__init__()  # 初始化6*10地图与连接

magic_map_graph = Map()  # 设置魔法地图
magic_map_graph.__init__()  # 初始化6*10地图与连接

width, height = screen.get_size()  # 获取屏幕大小
square_size = (width / 12, height / 9)  # 获取单个方块大小

line_group = {}  # 管理划线的字典 key为组名，value为线的list
card_group = {}  # 管理场上士兵的字典 key为location
player_card_group = {}  # 管理玩家手上的牌 key为数字，value为card
color_group = {}  # 管理场上线条颜色，key与其类型相对应
text_group = {}  # same as color group

# 加载地图图片
image_background = ...  # 加载背景图片（自制地图）


####################################################
# part1: draw text, line, image
####################################################
def draw_text(surface: pygame.Surface, text: str, pos: tuple[int, int],
              text_size: int = 22) -> None:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *upper-left corner* of the text.
    """
    font = pygame.font.SysFont('inconsolata', text_size)
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
            draw_text(screen, str(player_card_group[x].value * 2),
                      (location[0], location[1] + square_size[1] * 1.7))


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


def enclose_selected_card(c: Optional[card], is_display: bool = True) -> None:
    """set enclosed card.
    """
    if c is not None:
        loc = c.get_real_location()
        color_group['enclosed_card_1'] = THECOLORS['blue']
        color_group['enclosed_card_2'] = THECOLORS['blue']
        color_group['enclosed_card_3'] = THECOLORS['blue']
        color_group['enclosed_card_4'] = THECOLORS['blue']
        if is_display is True:
            line_group['enclosed_card_1'] = [loc, (loc[0] + 2 * square_size[0], loc[1])]
            line_group['enclosed_card_2'] = [loc, (loc[0], loc[1] + 2 * square_size[1])]
            line_group['enclosed_card_3'] = [(loc[0], loc[1] + 2 * square_size[1]),
                                             (loc[0] + 2 * square_size[0],
                                              loc[1] + 2 * square_size[1])]
            line_group['enclosed_card_4'] = [(loc[0] + 2 * square_size[0], loc[1]),
                                             (loc[0] + 2 * square_size[0],
                                              loc[1] + 2 * square_size[1])]
        else:
            if 'enclosed_card_1' in line_group and 'enclosed_card_2' in line_group \
                    and 'enclosed_card_3' in line_group and 'enclosed_card_4' in line_group:
                line_group.pop('enclosed_card_1')
                line_group.pop('enclosed_card_2')
                line_group.pop('enclosed_card_3')
                line_group.pop('enclosed_card_4')


def draw_cards_in_map() -> None:
    """draw all item in map
    """
    for x in range(1, 11):
        for y in range(1, 7):
            if game_map_graph.get_vertex((x, y)).item is not None:
                marked_card = game_map_graph.get_vertex((x, y)).item
                loc = marked_card.get_real_location()
                screen.blit(marked_card.images[marked_card.display_mode], loc)
                draw_text(screen, marked_card.direction + ' ' + str(marked_card.hp),
                          (loc[0] + square_size[0] * 0.1, loc[1] + 0.8 * square_size[1]),
                          text_size=15)


####################################################
# part1.1: set initialize data
####################################################
def set_init_player_card_random() -> None:
    """setup the card group randomly.
    """
    for key in range(1, 7):
        possible_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        chosen = random.choice(possible_choices)
        location = ((key - 1) * 2, 7.1)
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
    # 显示我方基地hp
    draw_text(surface, 'HP: ' + str(my_hp), (0, int(square_size[1] * 5.5)), text_size=20)
    draw_text(surface, 'Hp: ' + str(enemy_hp),
              (int(square_size[0] * 11), int(square_size[1] * 5.5)), text_size=20)  # 显示敌方基地hp


def refresh_visual_image(c: card) -> None:
    """refresh visual image by input.
    """
    global clicked_map, turn_end, clicked_card, decition_act
    if decition_act is True:
        clicked_map = False
        turn_end = True
        clicked_card = False
        (x, y) = pygame.mouse.get_pos()
        local_x = int(x // square_size[0])
        local_y = int(y // square_size[1])
        # 如果点击范围超出自己基地3格，放入无效且不会返还金币！
        # 除非是法术，否则如果放置位置item != None，放入无效且不会返还金币！
        situation_1 = square_size[0] < pygame.mouse.get_pos()[0] < square_size[0] * 4
        situation_2 = square_size[1] <= pygame.mouse.get_pos()[1] <= square_size[1] * 7
        situation_3 = game_map_graph.get_vertex((local_x, local_y)).item is None
        situation_4 = type(c) is fireball or type(c) is lightening
        if situation_1 and situation_2 and (situation_3 or situation_4):
            if type(c) is miniguner:
                game_map_graph.get_vertex((local_x, local_y)).item = miniguner((local_x, local_y),
                                                                               'right')
            elif type(c) is charger:
                game_map_graph.get_vertex((local_x, local_y)).item = charger((local_x, local_y),
                                                                             'right')
            elif type(c) is sniper:
                game_map_graph.get_vertex((local_x, local_y)).item = sniper((local_x, local_y),
                                                                            'right')
            elif type(c) is rocketer:
                game_map_graph.get_vertex((local_x, local_y)).item = rocketer((local_x, local_y),
                                                                              'right')
            elif type(c) is doctor:
                game_map_graph.get_vertex((local_x, local_y)).item = doctor((local_x, local_y),
                                                                            'right')
            elif type(c) is nijia:
                game_map_graph.get_vertex((local_x, local_y)).item = nijia((local_x, local_y),
                                                                           'right')
            elif type(c) is mine:
                game_map_graph.get_vertex((local_x, local_y)).item = mine((local_x, local_y),
                                                                          'right')
            elif type(c) is autogun:
                game_map_graph.get_vertex((local_x, local_y)).item = autogun((local_x, local_y),
                                                                             'right')
            elif type(c) is fireball:
                magic_map_graph.get_vertex((local_x, local_y)).item = fireball((local_x, local_y),
                                                                               'right')
            elif type(c) is lightening:
                magic_map_graph.get_vertex((local_x, local_y)).item = lightening((local_x, local_y),
                                                                                 'right')
            remove_from_player_group(player_card_group, c.location[0] // 2 + 1)
            game_map_graph.get_vertex((local_x, local_y)).item.get_real_location()
    decition_act = False


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
            possible_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            chosen = random.choice(possible_choices)
            location = ((key - 1) * 2, 7.1)
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


def money_increase() -> None:
    """Increase the money player have by numbers of mine
    """
    global money
    acc = 1
    for x in range(1, 11):
        for y in range(1, 7):
            if game_map_graph.get_vertex((x, y)).item is not None:
                mark = game_map_graph.get_vertex((x, y)).item
                if type(mark) is mine:
                    acc += 1
    money += acc * 10


def make_all_soldier_move(is_movable: bool = False) -> None:
    """make all soldier move.
    """
    if is_movable is True:
        right_visited = []
        left_visited = []
        for x in range(1, 11):
            for y in range(1, 7):
                if game_map_graph.get_vertex((11 - x, y)).item is not None \
                        and (12 - x, y) not in right_visited \
                        and game_map_graph.get_vertex((11 - x, y)).item.direction == 'right' \
                        and game_map_graph.get_vertex((11 - x, y)).item.type == 'soldier' \
                        and x != 1 \
                        and game_map_graph.get_vertex((12 - x, y)).item is None:
                    marked_card = game_map_graph.get_vertex((11 - x, y)).item
                    game_map_graph.make_move(marked_card.location)
                    right_visited.append((12 - x, y))
                elif game_map_graph.get_vertex((x, y)).item is not None \
                        and (x - 1, y) not in left_visited \
                        and game_map_graph.get_vertex((x, y)).item.direction != 'right' \
                        and game_map_graph.get_vertex((x, y)).item.type == 'soldier' \
                        and x != 1 \
                        and game_map_graph.get_vertex((x - 1, y)).item is None:
                    marked_card = game_map_graph.get_vertex((x, y)).item
                    game_map_graph.make_move(marked_card.location)
                    left_visited.append((x - 1, y))


def make_all_card_attack() -> None:
    """Make all card on screen attack.
    """
    global enemy_hp
    for x in range(1, 11):
        for y in range(1, 7):
            if game_map_graph.get_vertex((x, y)).item is not None:
                mark2 = game_map_graph.get_vertex((x, y)).item
                if x != 10:
                    game_map_graph.attack(mark2.location)
                else:
                    enemy_hp = enemy_hp - mark2.attack


def all_magic_explode() -> None:
    """Make all magic on map applied.
    """
    for x in range(1, 11):
        for y in range(1, 7):
            if type(magic_map_graph.get_vertex((x, y)).item) == fireball:
                magic = game_map_graph.get_vertex((x, y)).item
                loc = magic.location
                if loc[0] != 1:
                    loc1 = (loc[0] - 1, loc[1])
                else:
                    loc1 = None
                if loc[0] != 10:
                    loc2 = (loc[0] + 1, loc[1])
                else:
                    loc2 = None
                if loc[1] != 1:
                    loc3 = (loc[0], loc[1] - 1)
                else:
                    loc3 = None
                if loc[1] != 6:
                    loc4 = (loc[0], loc[1] + 1)
                else:
                    loc4 = None



            elif type(magic_map_graph.get_vertex((x, y)).item) == lightening:
                magic = game_map_graph.get_vertex((x, y)).item
                loc = magic.location
                if game_map_graph.get_vertex(loc) is None:
                    pass
                else:
                    game_map_graph.get_vertex(loc).item.hp -= magic.attack
                game_map_graph.get_vertex((x, y)).item = None


def test_emery_move_working() -> None:
    game_map_graph.get_vertex((8, 2)).item = miniguner((8, 2), 'left')
    game_map_graph.get_vertex((7, 3)).item = autogun((7, 3), 'left')


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


def card_click(event: pygame.event.Event) -> Optional[card]:
    """Return which card is clicked.
    """
    global money
    mouse_x = event.pos[0]
    square_x = (mouse_x // square_size[0]) // 2 + 1
    mark = player_card_group[int(square_x)]
    if money < mark.value:
        print('You have not enough money!')
        return None
    else:
        money = money - mark.value
        return mark


################################################################
# part4: main game process
################################################################
while True:  # 游戏主进程
    clock.tick(60)  # 每秒执行60次
    if turn_end is True:
        term += 1
        money_increase()
        make_all_soldier_move(turn_end)
        make_all_card_attack()
        turn_end = False
    for event in pygame.event.get():  # 获取事件
        if event.type == pygame.QUIT:  # 如果点击退出（右上角X）
            sys.exit()  # 系统退出
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 点击地图
            if square_size[0] < pygame.mouse.get_pos()[0] < square_size[0] * 11 \
                    and square_size[1] < pygame.mouse.get_pos()[1] < square_size[1] * 7:
                marked_square = graph_click(game_map_graph, event)
                clicked_map = True
                if clicked_card is True:
                    decition_act = True
                else:
                    clicked_map = False
            elif square_size[1] * 7 < pygame.mouse.get_pos()[1]:
                if card_click(event) is not None:
                    selected_card = card_click(event)
                    clicked_card = True
                    enclose_selected_card(selected_card, clicked_card)
    screen.fill(color)  # 填充颜色
    add_card_to_player_group_random()
    draw_all_visual_line()
    text_data_visualize(screen)
    if selected_card is not None:
        refresh_visual_image(selected_card)
        add_card_to_player_group_random()
        enclose_selected_card(selected_card, clicked_card)
    draw_all_image()
    draw_cards_in_map()
    draw_bone_map(screen)
    draw_all_visual_line()
    pygame.display.flip()  # 刷新显示

pygame.quit()
