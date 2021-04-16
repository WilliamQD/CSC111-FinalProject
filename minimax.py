"""This Python module contains the Minimax_tree class.

Copyright and Usage Information
===============================

This program is provided solely for the personal and private use of teachers and TAs
checking and grading the CSC111 project at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Alex Lin, Steven Liu, Haitao Zeng, William Zhang.
"""
from __future__ import annotations
import random
from map_graph import Map

from typing import Any, List
from card import miniguner, charger, sniper, rocketer, doctor, ninja, \
    fireball, lightening, mine, autogun, Card


class Minimax_tree:
    """The decision tree which ai will use.
    """
    subtree: list[Minimax_tree]
    item: List  # stored what it have.
    situation: Map  # store actual map.
    memory: Any  # store the decition ai make.
    ai_score: float
    player_score: float

    def __init__(self, item: List[Any]):
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
                        player_score += self.situation.get_vertex((x, y)).item.weight \
                                        * self.situation.get_vertex((x, y)).weight
                    elif self.situation.get_vertex((x, y)).item.direction == 'left':
                        ai_score += self.situation.get_vertex((x, y)).item.weight \
                                    * self.situation.get_vertex((x, y)).weight
        return ai_score - player_score

    def highest_row_score_calculate(self) -> int:

        result = []
        for y in range(1, 7):
            player_score = 0
            ai_score = 0
            for x in range(1, 11):
                if self.situation.get_vertex((x, y)).item is not None:
                    if self.situation.get_vertex((x, y)).item.direction == 'right':
                        player_score += self.situation.get_vertex((x, y)).item.weight
                    elif self.situation.get_vertex((x, y)).item.direction == 'left':
                        ai_score += self.situation.get_vertex((x, y)).item.weight
            result.append(player_score - ai_score)

        highest = max(result)
        return result.index(highest) + 1

    def add_subtree(self, move: Card):

        if type(move) is lightening or type(move) is fireball:
            new_situation = Map()
        else:
            # Obtain a new map with the move executed (card being placed on that location)
            copy_map = self.situation.self_copy()
            copy_map.get_vertex(move.location).item = move
            new_situation = copy_map

        # Create a new subtree branch with the item being the new card
        # and the score of the new map
        new_subtree = Minimax_tree([])
        new_subtree.get_map(new_situation)
        curr_score = new_subtree.score_calculate()
        new_subtree.item = [move, curr_score]
        self.subtree.append(new_subtree)

    def get_all_possible_action(self) -> list[Card]:
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
            # elif i == 7:
            #     for j in possible_magic_location:
            #         result.append(fireball(j, 'left'))
            # elif i == 8:
            #     for j in possible_magic_location:
            #         result.append(lightening(j, 'left'))
            elif i == 9:
                for j in possible_other_location:
                    result.append(mine(j, 'left'))
            elif i == 10:
                for j in possible_other_location:
                    result.append(autogun(j, 'left'))
        return result

    def action_randomly(self) -> Card:
        return random.choice(self.get_all_possible_action())

    def action_by_minimax(self, is_ai_turn: bool, depth: int = 1):
        value = self.min_max(is_ai_turn, depth)
        row_score = self.highest_row_score_calculate()
        correct_row_cards = []
        for subtree in self.subtree:
            if subtree.item[0].location[1] == row_score:
                correct_row_cards.append(subtree.item)
        max = correct_row_cards[0][1]
        selected_card = correct_row_cards[0][0]
        for cards in correct_row_cards:
            if cards[1] > max:
                max = cards[1]
                selected_card = cards[0]
        if selected_card.location[1] == row_score:
            return selected_card
        print("not suppose to be here")
        return random.choice(self.get_all_possible_action())

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
