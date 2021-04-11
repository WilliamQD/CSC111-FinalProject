from __future__ import annotations
from graph import Graph
from typing import Any, Union


class Square:
    """a vertex that describe the square.
    """
    item: Any
    kind: Union[None, str]
    neighbours: dict[Square, bool]  # 在edge中增加bool属性以判断能否行走
    location: tuple

    def __init__(self, location: tuple, item: Any, kind: Union[None, str]) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = {}
        self.location = location


class Map(Graph):
    """a graph that describe the map.
    The map is 6 * 10

    Instance attributes:
        - ...
    """
    _vertices: dict[Any, Square]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        super().__init__()
        for x in range(1, 11):
            for y in range(1, 7):
                location = (x, y)
                self._vertices[location] = Square(location, None, None)

        for y in range(1, 7):
            for x in range(1, 11):
                if x != 10:
                    self.add_edge((x, y), (x + 1, y), is_pass=True)

        for y in range(1, 7):
            for x in range(1, 11):
                if y != 6:
                    self.add_edge((x, y), (x, y + 1))

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
                lst.append(self._vertices[(y, x)].location)
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

        if self._vertices[soldier_loc].item.direction == 'right':
            if 1 <= curr_x < 10 \
                    and 1 <= curr_y <= 6:
                # Update the new location of soldier
                self._vertices[soldier_loc].item.location = (curr_x + 1, curr_y)
                new_location = curr_x + 1, curr_y

                # Check whether the new_square has any soldier on it
                if self._vertices[new_location].item is None:
                    # Find the new square where the soldier would be,
                    # and update the item on squares
                    self._vertices[new_location].item, self._vertices[soldier_loc].item = \
                        self._vertices[soldier_loc].item, None
        else:
            if 1 < curr_x <= 10 \
                    and 1 <= curr_y <= 6:
                # Update the new location of soldier
                self._vertices[soldier_loc].item.location = (curr_x - 1, curr_y)
                new_location = curr_x - 1, curr_y

                if self._vertices[new_location].item is None:
                    self._vertices[new_location].item, self._vertices[soldier_loc].item = \
                        self._vertices[soldier_loc].item, None
