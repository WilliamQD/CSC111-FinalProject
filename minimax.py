from __future__ import annotations
import random
from map_graph import Map

from typing import Any, Optional
from card import miniguner, charger, sniper, rocketer, doctor, ninja, \
    fireball, lightening, mine, autogun, card


class Minimax_tree:
    """The decition tree which ai will use.
    """
    decition_mode: int  # 0: 使用士兵， 1： 使用法术， 2： 使用建筑， 3： 单纯随机
    subtree: list[Minimax_tree]
    item: Any  # 存放单个决策步骤(card, location)
    situation: Map  # 存放实际情况的地图

    def __init__(self):
       self.decition_mode = 3

    def get_map(self, m: Map) -> None:
        self.situation = m

    def score_calculate(self):
        ...

    def make_decition_mode(self):
        ...

    def add_subtree(self):
        ...

    def action_randomly(self) -> card:
        possible_card = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        chosen = random.choice(possible_card)
        possible_location = []
        if chosen == 7 or chosen == 8:
            for x in range(1, 11):
                for y in range(1, 7):
                    if self.situation.get_vertex((x, y)).item is None:
                        possible_location.append((x, y))
        else:
            for x in range(8, 11):
                for y in range(1, 7):
                    if self.situation.get_vertex((x, y)).item is None:
                        possible_location.append((x, y))

        location = random.choice(possible_location)

        if chosen == 1:
            return miniguner(location, 'left')
        elif chosen == 2:
            return charger(location, 'left')
        elif chosen == 3:
            return sniper(location, 'left')
        elif chosen == 4:
            return rocketer(location, 'left')
        elif chosen == 5:
            return doctor(location, 'left')
        elif chosen == 6:
            return ninja(location, 'left')
        elif chosen == 7:
            return fireball(location, 'left')
        elif chosen == 8:
            return lightening(location, 'left')
        elif chosen == 9:
            return mine(location, 'left')
        elif chosen == 10:
            return autogun(location, 'left')

    def action_by_minimax(self, depth: int = 1):
        for x in self.subtree:
            x.item
