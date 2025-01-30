from typing import ClassVar
from dataclasses import dataclass

from strfem.str_node import Node
from strfem.str_section import Section
from strfem.str_material import Material


@dataclass()
class Line:
    """
    Structural line element

    Args:
        id: Unique identifier for the line
        node1: start node of the line
        node2: end node of the line

    Examples:
        >>>node1 = Node(1, [1, 2, 3])
        >>>node2 = Node(2, [4, 5, 6])
        >>>line1 = Line(1, node1, node2)
        >>>line1.to_string()
        Line #1 (1 -> 2)

    """

    epsilon: ClassVar[float] = 1e-6  # Small threshold for numerical comparisons

    id: int
    node1: Node
    node2: Node

    def __post_init__(self) -> None:
        self.section: Section | None = None
        self.material: Material | None = None

    def assign_section(self, section: Section | None) -> None:
        self.section = section

    def assign_material(self, material: Material | None) -> None:
        self.material = material

    def __str__(self) -> str:
        """
        Generate a comprehensive string representation of the line element.

        Returns:
            Detailed formatted string with line properties and coordinates
        """
        node1_coord = f"[{self.node1.x:.2f}, {self.node1.y:.2f}, {self.node1.z:.2f}]"
        node2_coord = f"[{self.node2.x:.2f}, {self.node2.y:.2f}, {self.node2.z:.2f}]"

        return (
            f"Line Details:\n"
            f"  ID:          #{self.id}\n"
            f"  Nodes:       {self.node1.id} -> {self.node2.id}\n"
            f"  Coordinates: {node1_coord} -> {node2_coord}\n"
            f"  Section:     {self.section.name if self.section else 'Unassigned'}\n"
            f"  Material:    {self.material.name if self.material else 'Unassigned'}"
        )


def main():
    node1 = Node(1, [1, 2, 3])
    node2 = Node(2, [4, 5, 6])
    node3 = Node(3, [7, 8, 9])
    node4 = Node(4, [10, 11, 12])

    line1 = Line(1, node1, node2)
    line2 = Line(2, node2, node3)
    line3 = Line(3, node3, node4)

    print(line1)
    print(line2)
    print(line3)


if __name__ == "__main__":
    main()
