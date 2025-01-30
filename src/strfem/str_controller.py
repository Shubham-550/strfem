import numpy as np
import numpy.typing as npt

from typing import Optional
from dataclasses import dataclass, field

from strfem.str_node import Node
from strfem.str_line import Line
from strfem.str_support import Support
from strfem.log import setup_controller_logging


@dataclass()
class Controller:
    precision: int = 6

    def __post_init__(self) -> None:
        self.node_id = 0
        self.line_id = 0
        self.support_id = 0

        self.nodes: list[Node] = []
        self.lines: list[Line] = []
        self.supports: list[Support] = []

        self.epsilon = 10 ** (-self.precision)
        self.node_lookup: dict[tuple[float], Node] = {}
        self.line_lookup: dict[tuple[Node, Node], Line] = {}

        # Setup logging
        self.logger = setup_controller_logging()

    # HH: Node

    def add_node(self, coord: npt.ArrayLike = np.empty(3, dtype=float)) -> Node:
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
    ) -> Optional[Line]:
        """
        Adds a line between two nodes if it doesn't already exist.

        Args:
            node1: First node
            node2: Second node

        Returns:
            Line object
        """

        try:
            # Validate node inputs
            if (node1 is None) or (node2 is None):
                raise ValueError(
                    "Both node1 and node2 must be provided to create a line."
                )

            # Check for self-connection
            if node1 == node2:
                self.logger.error(
                    f"Line cannot connect a node to itself (Node ID: {node1.id})"
                )
                return None

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

    # HH: Support Definitions
    def add_support(
        self,
        name: str = "support",
        kux: float = 0,
        kuy: float = 0,
        kuz: float = 0,
        krx: float = 0,
        kry: float = 0,
        krz: float = 0,
    ) -> Support:
        self.support_id += 1
        support = Support(self.support_id, name, kux, kuy, kuz, krx, kry, krz)
        self.supports.append(support)
        return support

    def add_support_fixed(self, label: str) -> Support:
        self.support_id += 1
        support = Support(
            self.support_id,
            label,
            kux=Support.ku_rigid,
            kuy=Support.ku_rigid,
            kuz=Support.ku_rigid,
            krx=Support.kr_rigid,
            kry=Support.kr_rigid,
            krz=Support.kr_rigid,
        )
        self.supports.append(support)
        return support

    def add_support_pinned(self, label: str) -> Support:
        self.support_id += 1
        support = Support(
            self.support_id,
            label,
            kux=Support.ku_rigid,
            kuy=Support.ku_rigid,
            kuz=Support.ku_rigid,
            krx=Support.kr_free,
            kry=Support.kr_free,
            krz=Support.kr_free,
        )
        self.supports.append(support)
        return support

    def add_support_roller(self, label: str) -> Support:
        self.support_id += 1
        support = Support(
            self.support_id,
            label,
            kux=Support.ku_free,
            kuy=Support.ku_free,
            kuz=Support.ku_rigid,
            krx=Support.kr_free,
            kry=Support.kr_free,
            krz=Support.kr_free,
        )
        self.supports.append(support)
        return support

    def apply_support(self, node: Node, support: Support) -> None:
        node.assign_support(support)

    def remove_support(self, node: Node) -> None:
        node.assign_support(None)

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
            ("Support", self.supports),
        ]

        for section_name, section_items in sections:
            output.append(f"\n{separator}\n")
            output.append(f"{section_name}:\n")
            for item in section_items:
                output.append(str(item))

        output.append(f"\n{separator}\n")

        return "\n".join(output)
