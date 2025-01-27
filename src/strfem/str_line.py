from strfem.str_node import Node


class Line:
    epsilon: float = 1e-6  # Small threshold for numerical comparisons

    def __init__(self, id: int, node1: Node, node2: Node) -> None:
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
        self.id = id
        self.node1 = node1
        self.node2 = node2

    def to_string(self) -> None:
        """Print the details of the line element."""
        print(f"Line #{self.id} ({self.node1.id} -> {self.node2.id})")


def main() -> None:
    node1 = Node(1, [1, 2, 3])
    node2 = Node(2, [4, 5, 6])
    node3 = Node(3, [7, 8, 9])
    node4 = Node(4, [10, 11, 12])

    line1 = Line(1, node1, node2)
    line2 = Line(2, node2, node3)
    line3 = Line(3, node3, node4)

    line1.to_string()
    line2.to_string()
    line3.to_string()


if __name__ == "__main__":
    main()
