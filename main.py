from src.strfem import Viewer, Controller


def main() -> None:
    controller = Controller()
    viewer = Viewer()

    # Nodes
    node1 = controller.add_node([0, 0, 0])
    node2 = controller.add_node([0, 0, 5])
    node3 = controller.add_node([10, 0, 5])
    node4 = controller.add_node([10, 0, 0])

    # Lines
    line1 = controller.add_line(node1, node2)
    line2 = controller.add_line(node2, node3)
    line3 = controller.add_line(node3, node4)

    # Supports
    support1 = controller.add_support("pinned1", 1e15, 1e15, 1e15, 1e-4, 1e-4, 1e-4)
    support2 = controller.add_support_fixed("fixed")
    support3 = controller.add_support_pinned("pinned2")
    support4 = controller.add_support_roller("roller")

    controller.apply_support(node1, support1)
    controller.apply_support(node2, support2)
    controller.apply_support(node3, support3)
    controller.apply_support(node4, support4)

    # Sections
    section1 = controller.add_section("I", 1, 2, 3, 4)
    section2 = controller.add_section_rect("300x200", 0.3, 0.2)

    controller.apply_section(line1, section1)
    controller.apply_section(line2, section2)

    # Materials
    material1 = controller.add_material("Steel", 200e9, 20e9, 0.3)
    material2 = controller.add_material("Aluminium", 70e9, 10e9, 0.2)

    controller.apply_material(line1, material1)
    controller.apply_material(line2, material2)

    print(controller)

    # viewer.render(controller)


if __name__ == "__main__":
    main()
