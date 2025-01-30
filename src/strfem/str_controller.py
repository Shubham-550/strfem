import numpy as np
import numpy.typing as npt

from dataclasses import dataclass

from strfem.log import setup_controller_logging
from strfem.str_node import Node
from strfem.str_line import Line
from strfem.str_support import Support
from strfem.str_section import Section
from strfem.str_material import Material


@dataclass()
class Controller:
    precision: int = 6

    def __post_init__(self) -> None:
        self.node_id: int = 0
        self.line_id: int = 0
        self.support_id: int = 0
        self.section_id: int = 0
        self.material_id: int = 0

        self.nodes: list[Node] = []
        self.lines: list[Line] = []
        self.supports: list[Support] = []
        self.sections: list[Section] = []
        self.materials: list[Material] = []

        self.epsilon: float = 10 ** (-self.precision)
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

    def add_line(self, node1: Node | None = None, node2: Node | None = None) -> Line:
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

            # TODO: Handle None returns in Line creation
            # Check for self-connection
            if node1 == node2:
                self.logger.error(
                    f"Line cannot connect a node to itself (Node ID: {node1.id})"
                )
                return Line(-1, node1, node2)

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

    # HH: Section Definitions

    def add_section(self, name, Ax, Ix, Iy, Iz) -> Section:
        self.section_id += 1
        section = Section(self.section_id, name, Ax, Ix, Iy, Iz)
        self.sections.append(section)
        return section

    def add_section_rect(self, name, dy, dz) -> Section:
        """
        Args:
        dy = dimension parallel to Y-axis and perpendicula to Z-axis
             dimension || to Y-axis and _|_ to Z-axis
             width

        dz = dimension parallel to Z-axis and perpendicula to Y-axis
             dimension || to Z-axis and _|_ to Y-axis
             height


        Ax = dy * dz
        Iy = dz * (dy^3) / 12
        Iz = dy * (dz^3) / 12
        Ix = Iy + Iz
        """

        self.section_id += 1

        # Calculate the section parameter for rectangle
        Ax = dy * dz
        Iy = dy * (dz**3) / 12
        Iz = dz * (dy**3) / 12
        Ix = Iy + Iz

        section = Section(self.section_id, name, Ax, Ix, Iy, Iz)
        self.sections.append(section)
        return section

    def add_section_circ(self, name: str, dia: float) -> Section:
        """
        Args:
        dia = diameter of circle in YZ plane

        Ax = ( pi * dia^2  ) / 4
        Iy = dia^4 / 64
        Iz = Iy
        Ix = 2 * Iy
        """

        self.section_id += 1

        # Calculate the section parameter for circle
        Ax = np.pi * dia * dia / 4
        Iy = dia**4 / 64
        Iz = Iy
        Ix = 2 * Iy

        section = Section(self.section_id, name, Ax, Ix, Iy, Iz)
        self.sections.append(section)
        return section

    def add_section_tri(self, name: str, dy: float, dz: float) -> Section:
        """
        Args:
        dy = dimension parallel to Y-axis and perpendicula to Z-axis
             dimension || to Y-axis and _|_ to Z-axis
             base of the triange

        dz = dimension parallel to Z-axis and perpendicula to Y-axis
             dimension || to Z-axis and _|_ to Y-axis
             height of the triangle

        Ax = 0.5 * dy * dz
        Iy = dz * (dy^3) / 12
        Iz = dy * (dz^3) / 12
        Ix = Iy + Iz
        """

        self.section_id += 1

        # Calculate the section parameter for triangle
        Ax = 0.5 * dy * dz
        Iy = dz * (dy**3) / 36
        Iz = dy * dz * (dy**2 - dy * dz + dz**2) / 12
        Ix = Iy + Iz

        section = Section(self.section_id, name, Ax, Ix, Iy, Iz)
        self.sections.append(section)
        return section

    # TODO: def add_section_I(self, h, tw, wfb, tfb, wft, tft)

    # TODO: find the polar MOI for arbitary shape

    def apply_section(self, line, section) -> None:
        line.assign_section(section)

    def remove_section(self, line) -> None:
        line.assign_section(None)

    # HH: Material Properties

    def add_material(self, name, E, G, nu) -> Material:
        self.material_id += 1

        material = Material(self.material_id, name, E, G, nu)
        self.materials.append(material)
        return material

    def apply_material(self, line, material) -> None:
        line.assign_material(material)

    def remove_material(self, line) -> None:
        line.assign_material(None)

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
            ("Section", self.sections),
            ("Material", self.materials),
        ]

        for section_name, section_items in sections:
            output.append(f"\n{separator}\n")
            output.append(f"{section_name}:\n")
            for item in section_items:
                output.append(str(item))

        output.append(f"\n{separator}\n")

        return "\n".join(output)
