from __future__ import annotations
import pygame
import sys
from typing import Any


class gamemap:
    """The type of game map.
    """
    _vertices: dict[Any, _Vertex]


class _Vertex:
    """The type of single game map square.

    Instance Attributes:
    - item: soldier on this square.
    - neighbour: The square that are adjacent to this square.
    - special_area: The special area that control function.
    - line: which line it is in.
    - possible_move: tell which square in this square can move to.
    """
    item: Any
    neighbours: dict[str, _Vertex]
    special_area: Any
    line: int  # not necessary for now.
    possible_move: _Vertex


