import pygame
import sys
import random
from pygame.colordict import THECOLORS
from map_graph import Map, Square
from typing import Any, Optional
from card import miniguner, charger, sniper, rocketer, doctor, ninja, \
    fireball, lightening, mine, autogun, Card
from minimax import Minimax_tree

pygame.init()  # initialize pygame
size = (640, 480)  # set the window size
screen = pygame.display.set_mode(size)  # set up the screen
color = THECOLORS['white']  # set up the color

clock = pygame.time.Clock()  # set up the clock to show when the game is end.
term = 1  # The number of turn
money = 500  # The money of player
my_hp = 100  # The hp of player's basement
enemy_hp = 100  # The hp of player

clicked_map = False  # is the map clicked?
clicked_card = False  # is the card clicked?
decition_act = False  # is the action begin?
turn_end = False  # is the turn end?
marked_square = None  # the square which the card player clicked.
selected_card = None  # the card which the player clicked
attention1 = False  # Attention that show if the player's money is enough to buy the selected card.

ai = Minimax_tree([])  # Initialize minimax algorithm

game_map_graph = Map()  # set up a map which the game will use
game_map_graph.__init__()  # initialize the game_map_graph. More information go to map_graph.py

magic_map_graph = Map()  # set up a map which the magic will use
magic_map_graph.__init__()  # initialize the magic_map_graph. More information go to map_graph.py

width, height = screen.get_size()  # get the screen size
square_size = (width / 12, height / 9)  # get a square size.

line_group = {}  # a group to control the show of deletable line.
card_group = {}  # a group to control the show of deletable card on map.
player_card_group = {}  # a group to control the cards player have
color_group = {}  # a group to control the line color.
text_group = {}  # same as color group.

# 加载地图图片
image_background = pygame.image.load('Resources/background.png')  # 加载背景图片（自制地图）
image_background_suitable = pygame.transform.scale(image_background, (int(square_size[0] * 10),
                                                                      int(square_size[1] * 6)))

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
    screen.blit(image_background_suitable, square_size)
    for x in player_card_group:
        if player_card_group[x] is not None:
            location = player_card_group[x].get_real_location()
            screen.blit(player_card_group[x].images[player_card_group[x].display_mode], location)
            draw_text(screen, str(player_card_group[x].value),
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


def enclose_selected_card(c: Optional[Card], is_display: bool = True) -> None:
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
            player_card_group[key] = ninja(location)
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
    draw_text(surface, 'Round ' + str(term), (width // 2, 0))  # display round
    # display if the player can make action
    draw_text(surface, 'Your Turn', (int(width - 1.5 * square_size[0]), int(square_size[1] // 2)))
    draw_text(surface, 'Money: ' + str(money), (0, int(square_size[1] // 2)))  # display the money
    # display hp of player's basement
    draw_text(surface, 'HP: ' + str(my_hp), (0, int(square_size[1] * 5.5)), text_size=20)
    draw_text(surface, 'Hp: ' + str(enemy_hp),
              (int(square_size[0] * 11), int(square_size[1] * 5.5)), text_size=20)  # display hp


def refresh_visual_image(c: Card) -> None:
    """refresh visual image by input.
    """
    global clicked_map, turn_end, clicked_card, decition_act, selected_card, money
    if decition_act is True:

        (x, y) = pygame.mouse.get_pos()
        local_x = int(x // square_size[0])
        local_y = int(y // square_size[1])
        # is put in 3 square in front of basement on map on x?
        situation_1 = square_size[0] < pygame.mouse.get_pos()[0] < square_size[0] * 4
        # is it put in the game_map_graph on y?
        situation_2 = square_size[1] <= pygame.mouse.get_pos()[1] <= square_size[1] * 7
        # is the selected_square empty?
        situation_3 = game_map_graph.get_vertex((local_x, local_y)).item is None
        # is selected_card a magic?
        situation_4 = type(c) is fireball or type(c) is lightening
        #
        situation_5 = square_size[0] < pygame.mouse.get_pos()[0] < square_size[0] * 11

        if situation_4 is False and situation_1 is False and situation_2 is True:
            print('You put the card out of range! Reput the card')
            decition_act = False
            clicked_map = False
            return None

        if situation_4 is False and situation_3 is False:
            print('You put the card on a square which already have one. Reput the card')
            decition_act = False
            clicked_map = False
            return None

        clicked_map = False
        turn_end = True
        clicked_card = False

        if situation_1 and situation_2 and situation_3 and not situation_4:
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
            elif type(c) is ninja:
                game_map_graph.get_vertex((local_x, local_y)).item = ninja((local_x, local_y),
                                                                           'right')
            elif type(c) is mine:
                game_map_graph.get_vertex((local_x, local_y)).item = mine((local_x, local_y),
                                                                          'right')
            elif type(c) is autogun:
                game_map_graph.get_vertex((local_x, local_y)).item = autogun((local_x, local_y),
                                                                             'right')
            remove_from_player_group(player_card_group, c.location[0] // 2 + 1)
            game_map_graph.get_vertex((local_x, local_y)).item.get_real_location()

        elif situation_4 and situation_5:
            if type(c) is fireball:
                magic_map_graph.get_vertex((local_x, local_y)).item = fireball((local_x, local_y),
                                                                               'right')
            elif type(c) is lightening:
                magic_map_graph.get_vertex((local_x, local_y)).item = lightening((local_x, local_y),
                                                                                 'right')
            remove_from_player_group(player_card_group, c.location[0] // 2 + 1)

        all_magic_explode()
        clear_all_dead_body()
        selected_card = None
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
                player_card_group[key] = ninja(location)
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
                if type(mark) is mine and mark.direction == 'right':
                    acc += 1
    print(money)
    money += acc * 10
    print(money)


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
    global enemy_hp, my_hp
    for x in range(1, 11):
        for y in range(1, 7):
            if game_map_graph.get_vertex((x, y)).item is not None \
                    and type(game_map_graph.get_vertex((x, y)).item) is not mine:
                mark2 = game_map_graph.get_vertex((x, y)).item
                if x != 10 and x != 1:
                    game_map_graph.attack(mark2.location)
                elif x == 10 and mark2.direction == 'right':
                    enemy_hp = enemy_hp - mark2.attack
                elif x == 1 and mark2.direction == 'left':
                    my_hp = my_hp - mark2.attack


def all_magic_explode() -> None:
    """Make all magic on map applied.
    """
    for x in range(1, 11):
        for y in range(1, 7):
            if type(magic_map_graph.get_vertex((x, y)).item) == fireball:
                magic = magic_map_graph.get_vertex((x, y)).item
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

                if loc is not None:
                    if game_map_graph.get_vertex(loc).item is not None:
                        game_map_graph.get_vertex(loc).item.hp -= magic.attack
                if loc1 is not None:
                    if game_map_graph.get_vertex(loc1).item is not None:
                        game_map_graph.get_vertex(loc1).item.hp -= magic.attack
                if loc2 is not None:
                    if game_map_graph.get_vertex(loc2).item is not None:
                        game_map_graph.get_vertex(loc2).item.hp -= magic.attack
                if loc3 is not None:
                    if game_map_graph.get_vertex(loc3).item is not None:
                        game_map_graph.get_vertex(loc3).item.hp -= magic.attack
                if loc4 is not None:
                    if game_map_graph.get_vertex(loc4).item is not None:
                        game_map_graph.get_vertex(loc4).item.hp -= magic.attack
                magic_map_graph.get_vertex((x, y)).item = None

            elif type(magic_map_graph.get_vertex((x, y)).item) == lightening:
                magic = magic_map_graph.get_vertex((x, y)).item
                loc = magic.location
                if game_map_graph.get_vertex(loc).item is not None:
                    game_map_graph.get_vertex(loc).item.hp -= magic.attack
                magic_map_graph.get_vertex((x, y)).item = None


def test_emery_move_working() -> None:
    game_map_graph.get_vertex((8, 2)).item = miniguner((8, 2), 'left')
    game_map_graph.get_vertex((7, 3)).item = autogun((7, 3), 'left')


def clear_all_dead_body() -> None:
    """delete whose hp <= 0
    """
    for x in range(1, 11):
        for y in range(1, 7):
            if game_map_graph.get_vertex((x, y)).item is not None:
                mark2 = game_map_graph.get_vertex((x, y)).item
                if mark2.hp <= 0:
                    game_map_graph.get_vertex((x, y)).item = None


def win_or_lose() -> Optional[bool]:
    """The situation of which side win.
    """
    if my_hp <= 0 and enemy_hp > 0:
        return False
    elif enemy_hp <= 0 and my_hp > 0:
        return True
    elif enemy_hp <= 0 and my_hp <= 0:
        return my_hp >= enemy_hp
    else:
        return None


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


def card_click(event: pygame.event.Event) -> Optional[Card]:
    """Return which card is clicked.
    """
    global money, attention1, clicked_card
    mouse_x = event.pos[0]
    square_x = (mouse_x // square_size[0]) // 2 + 1
    mark = player_card_group[int(square_x)]
    if selected_card is None:
        if money < mark.value:
            print('You have not enough money! Auto go to next round')
            attention1 = True
            clicked_card = False
            return None
        elif money >= mark.value:
            money = money - mark.value
            clicked_card = True
            return mark


################################################################
# part5: ai operation
################################################################
def ai_action() -> None:
    """The function which ai make its action
    """
    global game_map_graph, ai
    ai.get_map(game_map_graph.self_copy())
    c = ai.action_by_minimax(True, 1)
    print(c, c.location)
    if type(c) is fireball or type(c) is lightening:
        magic_map_graph.get_vertex(c.location).item = c
    else:
        game_map_graph.get_vertex(c.location).item = c
    ai = Minimax_tree([])


################################################################
# part4: main game process
################################################################

while True:  # The main process of the game.
    clock.tick(60)  # Run 60 times a second.
    if turn_end is True:
        ai_action()
        term += 1
        money_increase()
        make_all_soldier_move(turn_end)
        make_all_card_attack()
        clear_all_dead_body()
        if win_or_lose() is True:
            draw_text(screen, 'YOU WIN', (width // 3, height // 2), text_size=110)
            pygame.display.flip()
            pygame.time.wait(5000)
            sys.exit()
        elif win_or_lose() is False:
            draw_text(screen, 'YOU LOSE', (width // 3, height // 2), text_size=110)
            pygame.display.flip()
            pygame.time.wait(5000)
            sys.exit()
        turn_end = False
    for event in pygame.event.get():  # get what happen
        if event.type == pygame.QUIT:  # if exit is clicked
            sys.exit()  # system quit
        elif event.type == pygame.MOUSEBUTTONDOWN:  # click the map
            if square_size[0] < pygame.mouse.get_pos()[0] < square_size[0] * 11 \
                    and square_size[1] < pygame.mouse.get_pos()[1] < square_size[1] * 7:
                marked_square = graph_click(game_map_graph, event)
                clicked_map = True
                if clicked_card is True:
                    decition_act = True
                else:
                    clicked_map = False
            elif square_size[1] * 7 < pygame.mouse.get_pos()[1]:
                selected_card = card_click(event)
                if selected_card is not None:
                    enclose_selected_card(selected_card, clicked_card)
    screen.fill(color)  # fill the screen with color
    add_card_to_player_group_random()
    draw_all_visual_line()
    text_data_visualize(screen)
    if selected_card is not None:
        refresh_visual_image(selected_card)
        add_card_to_player_group_random()
    enclose_selected_card(selected_card, is_display=clicked_card)
    if attention1 is True:
        turn_end = True
        attention1 = False
    draw_all_image()
    draw_cards_in_map()
    draw_bone_map(screen)
    draw_all_visual_line()
    pygame.display.flip()  # refresh the screen with new screen blit.

pygame.quit()
