import numpy as np
import numpy.typing as npt

from typing import Optional

from strfem.str_node import Node
from strfem.str_line import Line
from strfem.log import setup_controller_logging


class Controller:
    def __init__(self, precision: int = 6) -> None:
        self.node_id = 0
        self.line_id = 0
        self.nodes: list[Node] = []
        self.lines: list[Line] = []

        self.precision: int = precision

        self.epsilon = 10 ** (-precision)
        self.node_lookup: dict[tuple[float], Node] = {}
        self.line_lookup: dict[tuple[Node, Node], Line] = {}

        # Setup logging
        self.logger = setup_controller_logging()

    # HH: Node

    def add_node(self, coord: npt.ArrayLike = [0, 0, 0]) -> Node:
        """
        Add a node if it doesn't already exist.

        Args:
            coord: Coordinate of the node

        Returns:
            Node object
        """

        try:
            if np.size(coord) != 3:
                raise ValueError("Coordinates must have exactly three values.")

            # Round coordinates to specified precision.
            coord = np.round(np.array(coord, dtype=float), decimals=self.precision)

            # Check for existing node
            coord_tuple = tuple(coord)
            if coord_tuple in self.node_lookup:
                return self.node_lookup[coord_tuple]

            # Create new node
            self.node_id += 1
            node = Node(self.node_id, coord)

            self.nodes.append(node)
            self.node_lookup[coord_tuple] = node

            self.logger.info(f"Created new node at {coord} with ID {self.node_id}")
            return node

        except Exception as e:
            self.logger.error(f"Node creation failed: {e}")
            raise

    # HH: Line

    def add_line(
        self, node1: Optional[Node] = None, node2: Optional[Node] = None
    ) -> Line:
        """
        Adds a line between two nodes if it doesn't already exist.

        Args:
            node1: First node
            node2: Second node

        Returns:
            Line object
        """

        try:
            if (node1 is None) or (node2 is None):
                raise ValueError(
                    "Both node1 and node2 must be provided to create a line."
                )

            if node1 == node2:
                raise ValueError("Line cannot connect a node to itself")

            # Check for existing lines
            sorted_nodes = sorted([node1, node2], key=lambda n: n.id)
            node_pair = (sorted_nodes[0], sorted_nodes[1])
            if node_pair in self.line_lookup:
                return self.line_lookup[node_pair]

            self.line_id += 1
            line = Line(self.line_id, node1, node2)

            self.lines.append(line)
            self.line_lookup[node_pair] = line

            self.logger.info(
                f"Created new line between nodes {node1.id} and {node2.id}"
            )
            return line

        except Exception as e:
            self.logger.error(f"Line creation failed: {e}")
            raise

    # HH: Reporting

    def __str__(self) -> str:
        """
        Returns a string representation of the model's components.

        Returns:
            Formatted string with model details
        """
        separator = "=" * 50
        output = []

        output.append(f"\n{separator}\n")

        output.append(f"Model Summary:")
        output.append(f"Total Nodes: {len(self.nodes)}")
        output.append(f"Total Lines: {len(self.lines)}")

        sections = [
            ("Nodes", self.nodes),
            ("Lines", self.lines),
        ]

        for section_name, section_items in sections:
            output.append(f"\n{separator}\n")
            output.append(f"{section_name}:\n")
            for item in section_items:
                output.append(str(item))

        output.append(f"\n{separator}\n")

        return "\n".join(output)
