"""This Python module contains the whole game created by pygame.
"""

import sys
import random
from typing import Optional
import pygame
from pygame.colordict import THECOLORS
from card import miniguner, charger, sniper, rocketer, doctor, ninja, \
    fireball, lightening, mine, autogun, Card
from minimax import Minimax_tree
from map_graph import Map, Square

pygame.init()  # initialize pygame
SIZE = (640, 480)  # set the window size
SCREEN = pygame.display.set_mode(SIZE)  # set up the screen
COLOR = THECOLORS['white']  # set up the color

CLOCK = pygame.time.Clock()  # set up the clock to show when the game is end.
TERM = 1  # The number of turn
MONEY = 100  # The money of player
MY_HP = 100  # The hp of player's basement
ENEMY_HP = 100  # The hp of player

CLICKED_MAP = False  # is the map clicked?
CLICKED_CARD = False  # is the card clicked?
DECISION_ACT = False  # is the action begin?
TURN_END = False  # is the turn end?
MARKED_SQUARE = None  # the square which the card player clicked.
SELECTED_CARD = None  # the card which the player clicked
ATTENTION1 = False  # Attention that show if the player's money is enough to buy the selected card.

AI = Minimax_tree([])  # Initialize minimax algorithm

GAME_MAP_GRAPH = Map()  # set up a map which the game will use
GAME_MAP_GRAPH.__init__()  # initialize the game_map_graph. More information go to map_graph.py

MAGIC_MAP_GRAPH = Map()  # set up a map which the magic will use
MAGIC_MAP_GRAPH.__init__()  # initialize the magic_map_graph. More information go to map_graph.py

WIDTH, HEIGHT = SCREEN.get_size()  # get the screen size
SQUARE_SIZE = (WIDTH / 12, HEIGHT / 9)  # get a square size.

LINE_GROUP = {}  # a group to control the show of deletable line.
CARD_GROUP = {}  # a group to control the show of deletable card on map.
PLAYER_CARD_GROUP = {}  # a group to control the cards player have
COLOR_GROUP = {}  # a group to control the line color.
TEXT_GROUP = {}  # same as color group.

# 加载地图图片
IMAGE_BACKGROUND = pygame.image.load('Resources/background2.png')  # 加载背景图片（自制地图）
IMAGE_BACKGROUND_SUITABLE = pygame.transform.scale(IMAGE_BACKGROUND, (int(SQUARE_SIZE[0] * 10),
                                                                      int(SQUARE_SIZE[1] * 6)))


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
    """Draw the cards of both players (PLAYER_CARD_GROUP and card_group).
    """
    SCREEN.blit(IMAGE_BACKGROUND_SUITABLE, SQUARE_SIZE)
    for x in PLAYER_CARD_GROUP:
        if PLAYER_CARD_GROUP[x] is not None:
            location = PLAYER_CARD_GROUP[x].get_real_location()
            SCREEN.blit(PLAYER_CARD_GROUP[x].images[PLAYER_CARD_GROUP[x].display_mode], location)
            draw_text(SCREEN, str(PLAYER_CARD_GROUP[x].value),
                      (location[0], location[1] + SQUARE_SIZE[1] * 1.7))


def draw_bone_map(surface: pygame.Surface) -> None:
    """Draw the bone map with line (drawing a map).
    The map is in size of 6(+3) * 10(+2)
    """
    line_color = THECOLORS['grey']
    border_color = THECOLORS['black']
    for i in range(1, 8):
        if i in {1, 7}:
            pygame.draw.line(surface, border_color,
                             (0, SQUARE_SIZE[1] * i), (WIDTH, SQUARE_SIZE[1] * i))
        else:
            pygame.draw.line(surface, line_color, (SQUARE_SIZE[0], SQUARE_SIZE[1] * i),
                             (WIDTH - SQUARE_SIZE[0], SQUARE_SIZE[1] * i))

    for i in range(1, 12):
        pygame.draw.line(surface, line_color, (SQUARE_SIZE[0] * i, SQUARE_SIZE[1]),
                         (SQUARE_SIZE[0] * i, SQUARE_SIZE[1] * 7))


def draw_all_visual_line() -> None:
    """Draw all line in line_group.
    These lines in line_group will make up a box director
    which occur when player selected his/her card in the store.
    """
    for x in LINE_GROUP:
        pygame.draw.line(SCREEN, COLOR_GROUP[x], LINE_GROUP[x][0], LINE_GROUP[x][1])


def enclose_selected_card(c: Optional[Card], is_display: bool = True) -> None:
    """Set enclosed card, the card had been selected in store,
    and it will be enclosed by the box director created by draw_all_visual_line function.
    """
    if c is not None:
        loc = c.get_real_location()
        COLOR_GROUP['enclosed_card_1'] = THECOLORS['blue']
        COLOR_GROUP['enclosed_card_2'] = THECOLORS['blue']
        COLOR_GROUP['enclosed_card_3'] = THECOLORS['blue']
        COLOR_GROUP['enclosed_card_4'] = THECOLORS['blue']
        if is_display is True:
            LINE_GROUP['enclosed_card_1'] = [loc, (loc[0] + 2 * SQUARE_SIZE[0], loc[1])]
            LINE_GROUP['enclosed_card_2'] = [loc, (loc[0], loc[1] + 2 * SQUARE_SIZE[1])]
            LINE_GROUP['enclosed_card_3'] = [(loc[0], loc[1] + 2 * SQUARE_SIZE[1]),
                                             (loc[0] + 2 * SQUARE_SIZE[0],
                                              loc[1] + 2 * SQUARE_SIZE[1])]
            LINE_GROUP['enclosed_card_4'] = [(loc[0] + 2 * SQUARE_SIZE[0], loc[1]),
                                             (loc[0] + 2 * SQUARE_SIZE[0],
                                              loc[1] + 2 * SQUARE_SIZE[1])]
    else:
        if 'enclosed_card_1' in LINE_GROUP and 'enclosed_card_2' in LINE_GROUP \
                and 'enclosed_card_3' in LINE_GROUP and 'enclosed_card_4' in LINE_GROUP:
            LINE_GROUP.pop('enclosed_card_1')
            LINE_GROUP.pop('enclosed_card_2')
            LINE_GROUP.pop('enclosed_card_3')
            LINE_GROUP.pop('enclosed_card_4')


def draw_cards_in_map() -> None:
    """Draw all item in map.
    """
    for x in range(1, 11):
        for y in range(1, 7):
            if GAME_MAP_GRAPH.get_vertex((x, y)).item is not None:
                marked_card = GAME_MAP_GRAPH.get_vertex((x, y)).item
                loc = marked_card.get_real_location()
                SCREEN.blit(marked_card.images[marked_card.display_mode], loc)
                draw_text(SCREEN, marked_card.direction + ' ' + str(marked_card.hp),
                          (loc[0] + SQUARE_SIZE[0] * 0.1, loc[1] + 0.8 * SQUARE_SIZE[1]),
                          text_size=15)


####################################################
# part1.1: set initialize data
####################################################
def set_init_player_card_random() -> None:
    """Setup the card group randomly.
    """
    for key in range(1, 7):
        possible_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        chosen = random.choice(possible_choices)
        location = ((key - 1) * 2, 7.1)
        if chosen == 1:
            PLAYER_CARD_GROUP[key] = miniguner(location)
        elif chosen == 2:
            PLAYER_CARD_GROUP[key] = charger(location)
        elif chosen == 3:
            PLAYER_CARD_GROUP[key] = sniper(location)
        elif chosen == 4:
            PLAYER_CARD_GROUP[key] = rocketer(location)
        elif chosen == 5:
            PLAYER_CARD_GROUP[key] = doctor(location)
        elif chosen == 6:
            PLAYER_CARD_GROUP[key] = ninja(location)
        elif chosen == 7:
            PLAYER_CARD_GROUP[key] = fireball(location)
        elif chosen == 8:
            PLAYER_CARD_GROUP[key] = lightening(location)
        elif chosen == 9:
            PLAYER_CARD_GROUP[key] = mine(location)
        elif chosen == 10:
            PLAYER_CARD_GROUP[key] = autogun(location)


set_init_player_card_random()


####################################################
# part2: refresh and visualize surface, groups.
####################################################
def text_data_visualize(surface: pygame.Surface) -> None:
    """Draw the text, such as the direction of the cards,
    the hp of the cards, and the hp of basements on the screen.
    """
    draw_text(surface, 'Round ' + str(TERM), (WIDTH // 2, 0))  # display round
    # display if the player can make action
    draw_text(surface, 'Your Turn', (int(WIDTH - 1.5 * SQUARE_SIZE[0]), int(SQUARE_SIZE[1] // 2)))
    draw_text(surface, 'Money: ' + str(MONEY), (0, int(SQUARE_SIZE[1] // 2)))  # display the money
    # display hp of player's basement
    draw_text(surface, 'HP: ' + str(MY_HP), (0, int(SQUARE_SIZE[1] * 5.5)), text_size=20)
    draw_text(surface, 'Hp: ' + str(ENEMY_HP),
              (int(SQUARE_SIZE[0] * 11), int(SQUARE_SIZE[1] * 5.5)), text_size=20)  # display hp


def refresh_visual_image(c: Card) -> None:
    """Refresh visual image by input.
    """
    global CLICKED_MAP, TURN_END, CLICKED_CARD, DECISION_ACT, SELECTED_CARD, MONEY
    if DECISION_ACT is True:

        (x, y) = pygame.mouse.get_pos()
        local_x = int(x // SQUARE_SIZE[0])
        local_y = int(y // SQUARE_SIZE[1])
        # is put in 3 square in front of basement on map on x?
        situation_1 = SQUARE_SIZE[0] < pygame.mouse.get_pos()[0] < SQUARE_SIZE[0] * 4
        # is it put in the game_map_graph on y?
        situation_2 = SQUARE_SIZE[1] <= pygame.mouse.get_pos()[1] <= SQUARE_SIZE[1] * 7
        # is the selected_square empty?
        situation_3 = GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item is None
        # is selected_card a magic?
        situation_4 = isinstance(c, (fireball, lightening))
        #
        situation_5 = SQUARE_SIZE[0] < pygame.mouse.get_pos()[0] < SQUARE_SIZE[0] * 11

        if situation_4 is False and situation_1 is False and situation_2 is True:
            print('You put the card out of range! Reput the card')
            DECISION_ACT = False
            CLICKED_MAP = False
            return None

        if situation_4 is False and situation_3 is False:
            print('You put the card on a square which already have one. Reput the card')
            DECISION_ACT = False
            CLICKED_MAP = False
            return None

        CLICKED_MAP = False
        TURN_END = True
        CLICKED_CARD = False

        if situation_1 and situation_2 and situation_3 and not situation_4:
            if isinstance(c, miniguner):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = miniguner((local_x, local_y),
                                                                               'right')
            elif isinstance(c, charger):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = charger((local_x, local_y),
                                                                             'right')
            elif isinstance(c, sniper):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = sniper((local_x, local_y),
                                                                            'right')
            elif isinstance(c, rocketer):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = rocketer((local_x, local_y),
                                                                              'right')
            elif isinstance(c, doctor):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = doctor((local_x, local_y),
                                                                            'right')
            elif isinstance(c, ninja):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = ninja((local_x, local_y),
                                                                           'right')
            elif isinstance(c, mine):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = mine((local_x, local_y),
                                                                          'right')
            elif isinstance(c, autogun):
                GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item = autogun((local_x, local_y),
                                                                             'right')
            remove_from_player_group(PLAYER_CARD_GROUP, c.location[0] // 2 + 1)
            GAME_MAP_GRAPH.get_vertex((local_x, local_y)).item.get_real_location()

        elif situation_4 and situation_5:
            if isinstance(c, fireball):
                MAGIC_MAP_GRAPH.get_vertex((local_x, local_y)).item = fireball((local_x, local_y),
                                                                               'right')
            elif isinstance(c, lightening):
                MAGIC_MAP_GRAPH.get_vertex((local_x, local_y)).item = lightening((local_x, local_y),
                                                                                 'right')
            remove_from_player_group(PLAYER_CARD_GROUP, c.location[0] // 2 + 1)

        all_magic_explode()
        clear_all_dead_body()
        SELECTED_CARD = None
    DECISION_ACT = False


###############################################
# part0: helper functions
###############################################
def remove_from_player_group(group: dict, key: int) -> None:
    """Set the element to None in the player group by key.
    """
    if key in group:
        group[key] = 'Hello world'


def add_card_to_player_group_random() -> None:
    """Add a card to PLAYER_CARD_GROUP.
    """
    for key in PLAYER_CARD_GROUP:
        if PLAYER_CARD_GROUP[key] == 'Hello world':
            possible_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            chosen = random.choice(possible_choices)
            location = ((key - 1) * 2, 7.1)
            if chosen == 1:
                PLAYER_CARD_GROUP[key] = miniguner(location)
            elif chosen == 2:
                PLAYER_CARD_GROUP[key] = charger(location)
            elif chosen == 3:
                PLAYER_CARD_GROUP[key] = sniper(location)
            elif chosen == 4:
                PLAYER_CARD_GROUP[key] = rocketer(location)
            elif chosen == 5:
                PLAYER_CARD_GROUP[key] = doctor(location)
            elif chosen == 6:
                PLAYER_CARD_GROUP[key] = ninja(location)
            elif chosen == 7:
                PLAYER_CARD_GROUP[key] = fireball(location)
            elif chosen == 8:
                PLAYER_CARD_GROUP[key] = lightening(location)
            elif chosen == 9:
                PLAYER_CARD_GROUP[key] = mine(location)
            elif chosen == 10:
                PLAYER_CARD_GROUP[key] = autogun(location)


def money_increase() -> None:
    """Increase the money player have by the total numbers of mine.
    """
    global MONEY
    acc = 1
    for x in range(1, 11):
        for y in range(1, 7):
            if GAME_MAP_GRAPH.get_vertex((x, y)).item is not None:
                mark = GAME_MAP_GRAPH.get_vertex((x, y)).item
                if isinstance(mark, mine) and mark.direction == 'right':
                    acc += 1
    MONEY += acc * 10


def make_all_soldier_move(is_movable: bool = False) -> None:
    """Make all soldier on the map move.
    NOTE: the soldier achieved the end of the row
    (location[1] == 1 or location[1] == 6 depended on the direction of the card)
    will not make move.
    """
    if is_movable is True:
        right_visited = []
        left_visited = []
        for x in range(1, 11):
            for y in range(1, 7):
                if GAME_MAP_GRAPH.get_vertex((11 - x, y)).item is not None \
                        and (12 - x, y) not in right_visited \
                        and GAME_MAP_GRAPH.get_vertex((11 - x, y)).item.direction == 'right' \
                        and GAME_MAP_GRAPH.get_vertex((11 - x, y)).item.type == 'soldier' \
                        and x != 1 \
                        and GAME_MAP_GRAPH.get_vertex((12 - x, y)).item is None:
                    marked_card = GAME_MAP_GRAPH.get_vertex((11 - x, y)).item
                    GAME_MAP_GRAPH.make_move(marked_card.location)
                    right_visited.append((12 - x, y))
                elif GAME_MAP_GRAPH.get_vertex((x, y)).item is not None \
                        and (x - 1, y) not in left_visited \
                        and GAME_MAP_GRAPH.get_vertex((x, y)).item.direction != 'right' \
                        and GAME_MAP_GRAPH.get_vertex((x, y)).item.type == 'soldier' \
                        and x != 1 \
                        and GAME_MAP_GRAPH.get_vertex((x - 1, y)).item is None:
                    marked_card = GAME_MAP_GRAPH.get_vertex((x, y)).item
                    GAME_MAP_GRAPH.make_move(marked_card.location)
                    left_visited.append((x - 1, y))


def make_all_card_attack() -> None:
    """Make all card on screen attack.
    """
    global ENEMY_HP, MY_HP
    for x in range(1, 11):
        for y in range(1, 7):
            if GAME_MAP_GRAPH.get_vertex((x, y)).item is not None \
                    and not isinstance(GAME_MAP_GRAPH.get_vertex((x, y)).item, mine):
                mark2 = GAME_MAP_GRAPH.get_vertex((x, y)).item
                if x not in {10, 1}:
                    GAME_MAP_GRAPH.attack(mark2.location)
                elif x == 10 and mark2.direction == 'right':
                    ENEMY_HP = ENEMY_HP - mark2.attack
                elif x == 1 and mark2.direction == 'left':
                    MY_HP = MY_HP - mark2.attack


def all_magic_explode() -> None:
    """Make all magic on map applied.
    """
    for x in range(1, 11):
        for y in range(1, 7):
            if isinstance(MAGIC_MAP_GRAPH.get_vertex((x, y)).item, fireball):
                magic = MAGIC_MAP_GRAPH.get_vertex((x, y)).item
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
                    if GAME_MAP_GRAPH.get_vertex(loc).item is not None:
                        GAME_MAP_GRAPH.get_vertex(loc).item.hp -= magic.attack
                if loc1 is not None:
                    if GAME_MAP_GRAPH.get_vertex(loc1).item is not None:
                        GAME_MAP_GRAPH.get_vertex(loc1).item.hp -= magic.attack
                if loc2 is not None:
                    if GAME_MAP_GRAPH.get_vertex(loc2).item is not None:
                        GAME_MAP_GRAPH.get_vertex(loc2).item.hp -= magic.attack
                if loc3 is not None:
                    if GAME_MAP_GRAPH.get_vertex(loc3).item is not None:
                        GAME_MAP_GRAPH.get_vertex(loc3).item.hp -= magic.attack
                if loc4 is not None:
                    if GAME_MAP_GRAPH.get_vertex(loc4).item is not None:
                        GAME_MAP_GRAPH.get_vertex(loc4).item.hp -= magic.attack
                MAGIC_MAP_GRAPH.get_vertex((x, y)).item = None

            elif isinstance(MAGIC_MAP_GRAPH.get_vertex((x, y)).item, lightening):
                magic = MAGIC_MAP_GRAPH.get_vertex((x, y)).item
                loc = magic.location
                if GAME_MAP_GRAPH.get_vertex(loc).item is not None:
                    GAME_MAP_GRAPH.get_vertex(loc).item.hp -= magic.attack
                MAGIC_MAP_GRAPH.get_vertex((x, y)).item = None


# def test_every_move_working() -> None:
#     """Testing
#     """
#     GAME_MAP_GRAPH.get_vertex((8, 2)).item = miniguner((8, 2), 'left')
#     GAME_MAP_GRAPH.get_vertex((7, 3)).item = autogun((7, 3), 'left')


def clear_all_dead_body() -> None:
    """Delete all cards which have hp <= 0
    """
    for x in range(1, 11):
        for y in range(1, 7):
            if GAME_MAP_GRAPH.get_vertex((x, y)).item is not None:
                mark2 = GAME_MAP_GRAPH.get_vertex((x, y)).item
                if mark2.hp <= 0:
                    GAME_MAP_GRAPH.get_vertex((x, y)).item = None


def win_or_lose() -> Optional[bool]:
    """Return True if player win, and return False if enemy win.
    Otherwise, return None.
    """
    if MY_HP <= 0 < ENEMY_HP:
        return False
    elif ENEMY_HP <= 0 < MY_HP:
        return True
    elif ENEMY_HP <= 0 and MY_HP <= 0:
        return MY_HP >= ENEMY_HP
    else:
        return None


###############################################
# part3: click
###############################################
def graph_click(m: Map, event: pygame.event.Event) -> Square:
    """Return which square the player clicked.
    """
    (x, y) = event.pos
    new_x = x // SQUARE_SIZE[0]
    new_y = y // SQUARE_SIZE[0]
    return m.get_vertex((new_x, new_y))


def card_click(event: pygame.event.Event) -> Optional[Card]:
    """Return which card is clicked.
    """
    global MONEY, ATTENTION1, CLICKED_CARD
    mouse_x = event.pos[0]
    square_x = (mouse_x // SQUARE_SIZE[0]) // 2 + 1
    mark = PLAYER_CARD_GROUP[int(square_x)]
    if SELECTED_CARD is None:
        if MONEY < mark.value:
            print('You have not enough money! Auto go to next round')
            ATTENTION1 = True
            CLICKED_CARD = False
            return None
        elif MONEY >= mark.value:
            MONEY = MONEY - mark.value
            CLICKED_CARD = True
            return mark


################################################################
# part5: ai operation
################################################################
def ai_action(difficulty: int = 1) -> None:
    """The function which ai make its action

    Difficulty is an integer between 1 and 5, inclusive, the higher the difficulty, the less
    -random the AI acts, which means it is more likely to make good choices following the AI
    min-max algorithm (a difficulty of 5 means it completely follows the AI algorithm, whereas
    1 means it acts completely random).
    """
    if difficulty == 1:
        random_scale = 1
    elif difficulty == 2:
        random_scale = 0.75
    elif difficulty == 3:
        random_scale = 0.5
    elif difficulty == 4:
        random_scale = 0.25
    else:
        random_scale = 0

    global GAME_MAP_GRAPH, AI
    AI.get_map(GAME_MAP_GRAPH.self_copy())
    if random.random() <= random_scale:
        c = AI.action_randomly()
    else:
        # Change the depth of the minimax algorithm here, between 1 and 3 inclusive
        # (advice on not choosing 3 since it takes very very long)
        c = AI.action_by_minimax(True, 1)
    if isinstance(c, (fireball, lightening)):
        MAGIC_MAP_GRAPH.get_vertex(c.location).item = c
    else:
        GAME_MAP_GRAPH.get_vertex(c.location).item = c
    AI = Minimax_tree([])


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E9999', 'E1101', 'R0916', 'R1702', 'R0915',
                    'E9998', 'E1136', 'E9997', 'R1710'],
        'extra-imports': ['pygame', 'sys', 'random', 'map_graph', 'typing', 'card', 'minimax']
    })
################################################################
# part4: main game process
################################################################

while True:  # The main process of the game.
    CLOCK.tick(60)  # Run 60 times a second.
    if TURN_END is True:
        ai_action()
        TERM += 1
        money_increase()
        make_all_soldier_move(TURN_END)
        make_all_card_attack()
        clear_all_dead_body()
        if win_or_lose() is True:
            draw_text(SCREEN, 'YOU WIN', (WIDTH // 3, HEIGHT // 2), text_size=110)
            pygame.display.flip()
            pygame.time.wait(5000)
            sys.exit()
        elif win_or_lose() is False:
            draw_text(SCREEN, 'YOU LOSE', (WIDTH // 3, HEIGHT // 2), text_size=110)
            pygame.display.flip()
            pygame.time.wait(5000)
            sys.exit()
        TURN_END = False
    for curr_event in pygame.event.get():  # get what happen
        if curr_event.type == pygame.QUIT:  # if exit is clicked
            sys.exit()  # system quit
        elif curr_event.type == pygame.MOUSEBUTTONDOWN:  # click the map
            if SQUARE_SIZE[0] < pygame.mouse.get_pos()[0] < SQUARE_SIZE[0] * 11 \
                    and SQUARE_SIZE[1] < pygame.mouse.get_pos()[1] < SQUARE_SIZE[1] * 7:
                MARKED_SQUARE = graph_click(GAME_MAP_GRAPH, curr_event)
                CLICKED_MAP = True
                if CLICKED_CARD is True:
                    DECISION_ACT = True
                else:
                    CLICKED_MAP = False
            elif SQUARE_SIZE[1] * 7 < pygame.mouse.get_pos()[1] and SELECTED_CARD is None:
                SELECTED_CARD = card_click(curr_event)
                if SELECTED_CARD is not None:
                    enclose_selected_card(SELECTED_CARD, CLICKED_CARD)
    SCREEN.fill(COLOR)  # fill the screen with color
    add_card_to_player_group_random()
    draw_all_visual_line()
    text_data_visualize(SCREEN)
    if SELECTED_CARD is not None:
        refresh_visual_image(SELECTED_CARD)
        add_card_to_player_group_random()
    enclose_selected_card(SELECTED_CARD, is_display=CLICKED_CARD)
    if ATTENTION1 is True:
        TURN_END = True
        ATTENTION1 = False
    draw_all_image()
    draw_cards_in_map()
    draw_bone_map(SCREEN)
    draw_all_visual_line()
    pygame.display.flip()  # refresh the screen with new screen blit.

pygame.quit()
