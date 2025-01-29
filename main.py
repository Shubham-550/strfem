from src.strfem import Viewer, Controller


def main() -> None:
    controller = Controller()
    viewer = Viewer()

    node1 = controller.add_node([0, 0, 0])
    node2 = controller.add_node([0, 0, 5])
    node3 = controller.add_node([10, 0, 5])
    node4 = controller.add_node([10, 0, 0])

    line1 = controller.add_line(node1, node2)
    line2 = controller.add_line(node2, node3)
    line3 = controller.add_line(node3, node4)

    print(controller)

    viewer.render(controller)


if __name__ == "__main__":
    main()
