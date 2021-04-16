from __future__ import annotations
import random
from map_graph import Map

from typing import Any, Optional, List
from card import miniguner, charger, sniper, rocketer, doctor, ninja, \
    fireball, lightening, mine, autogun, card


class Minimax_tree:
    """The decision tree which ai will use.
    """
    decition_mode: int  # 0: 使用士兵， 1： 使用法术， 2： 使用建筑， 3： 单纯随机
    subtree: list[Minimax_tree]
    item: List  # 存放单个决策步骤[card, score]
    situation: Map  # 存放实际情况的地图
    memory: Any  # 存放预测结果
    ai_score: float
    player_score: float

    def __init__(self, item: List[Any]):
        self.decition_mode = 3
        self.item = item
        self.subtree = []

    def get_map(self, m: Map) -> None:
        self.situation = m

    def score_calculate(self) -> float:
        """calculate the current score of the game based on how many units left for one side and
        how many healths left

        A score of negative means Player2 is winning, a score of positive means Player1 is winning.
        """
        player_score = 0
        ai_score = 0
        for x in range(1, 11):
            for y in range(1, 7):
                if self.situation.get_vertex((x, y)).item is not None:
                    if self.situation.get_vertex((x, y)).item.direction == 'right':
                        player_score += self.situation.get_vertex((x, y)).item.weight
                    elif self.situation.get_vertex((x, y)).item.direction == 'left':
                        ai_score += self.situation.get_vertex((x, y)).item.weight
        return ai_score - player_score

    def add_subtree(self, move: card):

        # Obtain a new map with the move executed (card being placed on that location)
        self.situation.get_vertex(move.location).item = move
        new_situation = self.situation
        self.situation.get_vertex(move.location).item = None

        # Create a new subtree branch with the item being the new card
        # and the score of the new map
        new_subtree = Minimax_tree([])
        new_subtree.get_map(new_situation)
        curr_score = new_subtree.score_calculate()
        new_subtree.item = [move, curr_score]
        self.subtree.append(new_subtree)

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

    def action_by_minimax(self, is_ai_turn: bool, depth: int = 1):

        value = self.min_max(is_ai_turn, depth)
        for subtree in self.subtree:
            # If the subtree has the given score of value, then return that action in that subtree
            if subtree.item[1] == value:
                return subtree.item[0]

    def min_max(self, is_ai_turn: bool, depth: int) -> float:

        if depth == 0:
            return self.score_calculate()
        # is_ai_turn should be true when the depth is odd, ex: 1, 3, 5
        if is_ai_turn:
            for move in self.get_all_possible_action():
                self.add_subtree(move)
            max_num = -99999999.0
            for subtree in self.subtree:
                eva = subtree.min_max(False, depth=depth - 1)
                max_num = max(max_num, eva)
            return max_num
        else:
            for move in self.get_all_possible_action():
                self.add_subtree(move)
            min_num = 99999999.0
            for subtree in self.subtree:
                eva = subtree.min_max(True, depth=depth - 1)
                min_num = min(min_num, eva)
            return min_num
