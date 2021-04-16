from __future__ import annotations

import copy

from card import *
from graph import Graph
from typing import Any, Union


class Square:
    """a vertex that describe the square.
    Instance Attributes:
        - item: A card or subclass of card stand on this square
        - kind: A string represents what kind of landform this square is
        - neighbours: The vertices (squares) that are adjacent to this vertex (square).
        - location: A tuple represents location of this square on the map
    Preconditions:
        - kind in {'volcano', 'forest', 'mountain', 'riven', 'grass land'}
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - 1 <= location[0] <= 10
        - 1 <= location[1] <= 6
    """
    item: Any
    kind: Union[None, str]
    neighbours: dict[Square, bool]  # 在edge中增加bool属性以判断能否行走
    location: tuple
    weight: float

    def __init__(self, location: tuple, item: Any, kind: Union[None, str]) -> None:
        """Initialize a new vertex with the given item and kind.
        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'volcano', 'forest', 'mountain', 'riven', 'grass land'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = {}
        self.location = location
        if self.kind == 'volcano' or self.kind == 'river':
            self.weight = 0.8 * self.location[0]
        elif self.kind == 'forest' or self.kind == 'mountain':
            self.weight = 1.2 * self.location[0]
        else:
            self.weight = 1 * self.location[0]


class Map(Graph):
    """a graph that describe the map.
    The map is 6 * 10
    Instance attributes:
        - A collection of the squares contained in this map.
        Maps item to Square object.
    """
    _vertices: dict[Any, Square]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        special_location = {'volcano': {(5, 1), (6, 1), (7, 1)},
                            'forest': {(2, 3), (2, 4), (2, 5), (3, 4), (4, 2), (4, 3),
                                       (5, 3), (9, 1), (9, 3), (9, 4), (10, 1), (10, 3)},
                            'river': {(4, 6), (5, 6), (6, 4), (6, 5), (6, 6), (7, 3), (7, 4)},
                            'mountain': {(2, 1), (3, 1), (3, 2), (3, 5), (3, 6),
                                         (7, 5), (7, 6), (8, 5), (8, 6)}
                            }
        super().__init__()
        for x in range(1, 11):
            for y in range(1, 7):
                location = (x, y)
                kind_of_field = 'grass land'
                for key in special_location:
                    if location in special_location[key]:
                        kind_of_field = key

                self._vertices[location] = Square(location, None, kind_of_field)

        for y in range(1, 7):
            for x in range(1, 11):
                if x != 10:
                    self.add_edge((x, y), (x + 1, y), is_pass=True)

        for y in range(1, 7):
            for x in range(1, 11):
                if y != 6:
                    self.add_edge((x, y), (x, y + 1))

    def self_copy(self) -> Map:
        """return a copy of self.
        """
        copy_map = Map()
        for x in range(1, 11):
            for y in range(1, 7):
                if self.get_vertex((x, y)).item is not None:
                    copy_map.get_vertex((x, y)).item = self.get_vertex((x, y)).item
        return copy_map

    # 此函数为自定义，功能为判定是否可以通过
    def is_passable(self, location1: Any, location2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.
        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if location1 in self._vertices and location2 in self._vertices:
            v1 = self._vertices[location1]
            for v2 in v1.neighbours:
                if v2.location == location2:
                    return v2.neighbours[v1] is True
        return False

    def adjacent(self, location1: Any, location2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.
        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if location1 in self._vertices and location2 in self._vertices:
            v1 = self._vertices[location1]
            return any(v2.location == location2 for v2 in v1.neighbours)
        else:
            return False

    def print_graph(self) -> None:
        """Test if the vertex of the graph initialize well.
        """
        lst = []
        for x in range(1, 7):
            for y in range(1, 11):
                lst.append([self._vertices[(y, x)].location, self._vertices[(y, x)].kind])
            print(lst)
            lst = []

    def get_vertex(self, location: tuple) -> Square:
        """ get a vertex by its location
        """
        return self._vertices[location]

    def make_move(self, soldier_loc: tuple) -> None:
        """Make the given soldier move.
        Precondition:
            - soldier.item is not None
        """
        curr_x = soldier_loc[0]
        curr_y = soldier_loc[1]
        new_square = None

        if self._vertices[soldier_loc].item.buffs['mobility'] is False:
            self._vertices[soldier_loc].item.buffs['mobility'] = True
            return

        if self._vertices[soldier_loc].item.buffs['burn'] is True:
            self._vertices[soldier_loc].item.hp = int(self._vertices[soldier_loc].item.hp
                                                      * (1 - 0.1))

        if self._vertices[soldier_loc].item.direction == 'right':
            if 1 <= curr_x < 10 \
                    and 1 <= curr_y <= 6:
                # Find the new square where the soldier would be
                new_location = curr_x + 1, curr_y

                # Check whether the new_square has any soldier on it
                if self._vertices[new_location].item is None:
                    # Update the new location of soldier,
                    # and update the item on squares
                    self._vertices[soldier_loc].item.location = new_location
                    self._vertices[new_location].item, self._vertices[soldier_loc].item = \
                        self._vertices[soldier_loc].item, None
                    new_square = self._vertices[new_location]
        else:
            if 1 < curr_x <= 10 \
                    and 1 <= curr_y <= 6:
                new_location = curr_x - 1, curr_y

                if self._vertices[new_location].item is None:
                    self._vertices[soldier_loc].item.location = new_location
                    self._vertices[new_location].item, self._vertices[soldier_loc].item = \
                        self._vertices[soldier_loc].item, None
                    new_square = self._vertices[new_location]

        if new_square.kind == 'volcano':
            new_square.item.buffs = {'attack buff': 1.0, 'defend buff': 1.0,
                                     'mobility': True, 'burn': True}
        elif new_square.kind == 'forest':
            new_square.item.buffs = {'attack buff': 1.25, 'defend buff': 1.0,
                                     'mobility': True, 'burn': False}
        elif new_square.kind == 'mountain':
            new_square.item.buffs = {'attack buff': 1.0, 'defend buff': 0.75,
                                     'mobility': True, 'burn': False}
        elif new_square.kind == 'river':
            new_square.item.buffs = {'attack buff': 1.0, 'defend buff': 1.0,
                                     'mobility': False, 'burn': False}
        else:
            new_square.item.buffs = {'attack buff': 1.0, 'defend buff': 1.0,
                                     'mobility': True, 'burn': False}

    def attack(self, card_loc: tuple) -> None:
        """Make the given card on that location attack if enemy is in his/her attack range.
        """
        # 判断是否有敌人在攻击范围内（必须是敌人：用direction来判断）
        curr_square = self.get_vertex(card_loc)
        card = self.get_vertex(card_loc).item
        target = None  # it would be a card or subclass of card

        # Finding the lowest hp ally in range (only for doctor)
        if type(card) is doctor:
            for neighbour in curr_square.neighbours:
                if neighbour.item is not None \
                        and card_loc[0] - card.range <= neighbour.location[0] \
                        <= card_loc[0] + card.range \
                        and neighbour.item.direction == card.direction:
                    # Finding the lowest hp percentage ally
                    if target is None or \
                            (neighbour.item.hp / neighbour.item.max_hp < target.hp / target.max_hp):
                        target = neighbour.item
        else:
            for neighbour in curr_square.neighbours:
                if neighbour.item is not None \
                        and card_loc[0] < neighbour.location[0] <= card_loc[0] + card.range \
                        and neighbour.item.direction != card.direction \
                        and card.direction == 'right':
                    # Finding the closest enemy
                    if target is None or neighbour.location[0] < target.location[0]:
                        target = neighbour.item
                elif neighbour.item is not None \
                        and card_loc[0] - card.range <= neighbour.location[0] < card_loc[0] \
                        and neighbour.item.direction != card.direction \
                        and card.direction == 'left':
                    if target is None or neighbour.location[0] > target.location[0]:
                        target = neighbour.item
        # Attack
        if target is not None and type(target) is not int:
            card.make_attack(target)
