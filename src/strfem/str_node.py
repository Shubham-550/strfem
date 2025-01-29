import numpy as np
import numpy.typing as npt


class Node:
    def __init__(self, id: int, coord: npt.ArrayLike = [0, 0, 0]) -> None:
        """
        Structural node

        Args:
            id: Unique identifier of the Node
            coord: Coordinate of the node

        Example:
        >>>node1 = Node(1, [1, 2, 3])
        >>>node1.to_string()
        Node #1 at [ 1.00, 2.00, 3.00]
        """

        self.id = id
        self.coord = np.array(coord)

        # Decompose coordinates
        self.x = self.coord[0]
        self.y = self.coord[1]
        self.z = self.coord[2]

    def __str__(self) -> str:
        """Represent the string representation of the node

        Returns:
            Formatted string with node details
        """
        coord_str = f"[{self.x:5.2f},{self.y:5.2f},{self.z:5.2f}]"
        return f"Node #{self.id} at {coord_str}"


def main() -> None:
    node1 = Node(1, [1, 2, 3])
    node2 = Node(2, [4, 5, 6])

    print(node1)
    print(node2)


if __name__ == "__main__":
    main()
