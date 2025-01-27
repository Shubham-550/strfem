import numpy as np
import numpy.typing as npt

from typing import Optional

from .str_node import Node
from .str_line import Line


class Controller:
    def __init__(self) -> None:
        self.node_id = 0
        self.line_id = 0
        self.nodes: list[Node] = []
        self.lines: list[Line] = []

        self.epsilon = 1e-6
        self.node_lookup: dict[tuple[float], Node] = {}
        self.line_lookup: dict[tuple[Node, ...], Line] = {}

    # HH: Node
    def add_node(self, coord: npt.ArrayLike = [0, 0, 0]) -> Node:
        """
        Add a node if it doesn't already exist.

        Args:
            coord: coordinate of the node

        Returns:
            New node or existing node if a duplicate was found
        """

        coord = np.array(coord)

        # Check for duplicate nodes
        coord_tuple = tuple(coord)
        if coord_tuple in self.node_lookup:
            return self.node_lookup[coord_tuple]

        self.node_id += 1
        id = self.node_id
        node = Node(id, coord)

        self.nodes.append(node)
        self.node_lookup[coord_tuple] = node
        return node

    # HH: Line
    def add_line(
        self, node1: Optional[Node] = None, node2: Optional[Node] = None
    ) -> Line:
        """
        Adds a line between two nodes if it doesn't already exist.

        Args:
            node1: First node of the line (default is None).
            node2: Second node of the line (default is None).

        Returns:
            New line or the existing line if a duplicate was found.
        """

        if (node1 is None) or (node2 is None):
            raise ValueError("Both node1 and node2 must be provided to create a line.")

        # Check for duplicate lines
        node_pair = tuple((node1, node2))
        if node_pair in self.line_lookup:
            return self.line_lookup[node_pair]

        self.line_id += 1
        id = self.line_id
        line = Line(id, node1, node2)

        self.lines.append(line)
        self.line_lookup[node_pair] = line
        return line

    # HH: Reporting
    def to_string(self) -> None:
        """
        Displays all the nodes, lines, supports, etc.

        Args: nil

        Returns: None
        """
        separator = "=" * 50
        print(f"Model has {len(self.nodes)} nodes and {len(self.lines)} lines.")

        print(f"\n{separator}\n")
        print("Nodes:\n")
        for node in self.nodes:
            node.to_string()

        print(f"\n{separator}\n")
        print("Lines:\n")
        for line in self.lines:
            line.to_string()
