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
    item: Any  # 存放单个决策步骤[card, score]
    situation: Map  # 存放实际情况的地图
    memory: Any  # 存放预测结果
    ai_score: float
    player_score: float

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

    def get_all_possible_action(self) -> list[card]:
        result = []
        possible_card = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        possible_magic_location = []
        possible_other_location = []
        for x in range(1, 11):
            for y in range(1, 7):
                possible_magic_location.append((x, y))
        for x in range(8, 11):
            for y in range(1, 7):
                if self.situation.get_vertex((x, y)).item is None:
                    possible_other_location.append((x, y))
        for i in possible_card:
            if i == 1:
                for j in possible_other_location:
                    result.append(miniguner(j, 'left'))
            elif i == 2:
                for j in possible_other_location:
                    result.append(charger(j, 'left'))
            elif i == 3:
                for j in possible_other_location:
                    result.append(sniper(j, 'left'))
            elif i == 4:
                for j in possible_other_location:
                    result.append(rocketer(j, 'left'))
            elif i == 5:
                for j in possible_other_location:
                    result.append(doctor(j, 'left'))
            elif i == 6:
                for j in possible_other_location:
                    result.append(ninja(j, 'left'))
            elif i == 7:
                for j in possible_magic_location:
                    result.append(fireball(j, 'left'))
            elif i == 8:
                for j in possible_magic_location:
                    result.append(lightening(j, 'left'))
            elif i == 9:
                for j in possible_other_location:
                    result.append(mine(j, 'left'))
            elif i == 10:
                for j in possible_other_location:
                    result.append(autogun(j, 'left'))
            return result

    def action_randomly(self) -> card:
        return random.choice(self.get_all_possible_action())

    def action_by_minimax(self, depth: int = 1):
        if self.subtree is None:
            return None
        for x in self.subtree:
            x.action_by_minimax(depth=depth - 1)

