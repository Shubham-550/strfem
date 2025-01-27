from src.strfem import *


def main() -> None:
    controller = Controller()

    node1 = controller.add_node([0, 0, 0])
    node2 = controller.add_node([0, 0, 5])
    node3 = controller.add_node([10, 0, 5])
    node4 = controller.add_node([10, 0, 0])

    line1 = controller.add_line(node1, node2)
    line2 = controller.add_line(node2, node3)
    line3 = controller.add_line(node3, node4)

    controller.to_string()


if __name__ == "__main__":
    main()
