import numpy as np
import numpy.typing as npt

from typing import Optional
from dataclasses import dataclass, field

from strfem.str_support import Support


@dataclass()
class Node:
    """
    Structural node

    Args:
        id: Unique identifier of the Node
        coord: Coordinate of the node

    Example:
    >>>node1 = Node(1, [1, 2, 3])
    >>>node1.to_string()
    Node #1 (Free) at [ 1.00, 2.00, 3.00]
    """

    id: int
    coord: npt.ArrayLike = field(default_factory=lambda: np.empty(3, dtype=float))

    def __post_init__(self):
        # Decompose coordinates
        self.coord = np.array(self.coord)
        self.x, self.y, self.z = self.coord

        self.support: Optional[Support] = None

    def assign_support(self, support: Optional[Support]) -> None:
        """Assign a support condition to the node"""
        self.support = support

    def __str__(self) -> str:
        """Return a formatted string representation of the node."""
        coord_str = f"[{self.x:5.2f},{self.y:5.2f},{self.z:5.2f}]"
        support_status = self.support.name if self.support else "Free"
        return f"Node #{self.id} ({support_status}) at {coord_str}"

    def __hash__(self) -> int:
        return hash(self.id)  # Use the unique ID for hashing

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.id == other.id  # Compare based on ID
        return False


def main() -> None:
    node1 = Node(1, [1, 2, 3])
    node2 = Node(2, [4, 5, 6])

    print(node1)
    print(node2)


if __name__ == "__main__":
    main()
