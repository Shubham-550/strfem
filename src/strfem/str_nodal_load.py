from dataclasses import dataclass, field

from strfem.str_node import Node


@dataclass
class NodalLoad:
    id: int
    load_case_id: int
    Fx: float = 0
    Fy: float = 0
    Fz: float = 0
    Mx: float = 0
    My: float = 0
    Mz: float = 0
    applied_to: set[int] = field(default_factory=set)

    def apply(self, node: Node) -> None:
        self.applied_to.add(node.id)

    def remove(self, node: Node) -> None:
        self.applied_to.remove(node.id)

    def __str__(self) -> str:
        return (
            f"Nodal Load #{self.id} \n"
            f"      Load Case #{self.load_case_id} \n"
            f"      Fx = {self.Fx:.2f} N \n"
            f"      Fy = {self.Fy:.2f} N \n"
            f"      Fz = {self.Fz:.2f} N \n"
            f"      Mx = {self.Mx:.2f} Nm \n"
            f"      My = {self.My:.2f} Nm \n"
            f"      Mz = {self.Mz:.2f} Nm \n"
            f"      Applied to Node: {self.applied_to if self.applied_to else 'Unassigned'} \n"
        )


def main() -> None:
    nodal_load1 = NodalLoad(0, 1, 2, 3, 4, 5, 6)
    nodal_load1.apply(Node(1, [0, 0, 0]))
    nodal_load1.apply(Node(2, [0, 5, 5]))
    nodal_load1.apply(Node(3, [7, 8, 9]))
    print(nodal_load1)


if __name__ == "__main__":
    main()
