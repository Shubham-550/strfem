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
    line4 = controller.add_line(node1, node3)

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

    # Releases
    release1 = controller.add_release_pinned_rigid("Pin-Rigid2")
    release2 = controller.add_release_rigid_pinned("Rigid-Pin")
    release3 = controller.add_release_pinned_pinned("Pin-Pin")

    controller.apply_release(line1, release1)
    controller.apply_release(line2, release2)
    controller.apply_release(line3, release3)

    # Load Case
    load_case1 = controller.add_load_case("Dead Load")
    load_case2 = controller.add_load_case("Live Load")
    load_case3 = controller.add_load_case("Wind Load")

    # Nodal Loads
    nodal_load1 = controller.add_nodal_load(load_case1.id, *range(1, 7))
    nodal_load2 = controller.add_nodal_load(load_case1.id, *range(7, 13))
    nodal_load3 = controller.add_nodal_load(load_case1.id, *range(13, 19))

    controller.apply_nodal_load(nodal_load1, node1)
    controller.apply_nodal_load(nodal_load2, node2)
    controller.apply_nodal_load(nodal_load1, node1)
    controller.apply_nodal_load(nodal_load1, node4)
    controller.remove_nodal_load(nodal_load1, node4)

    # Concentrated Line Load
    line_load_conc1 = controller.add_line_load_conc(
        load_case2.id, 2000, 1000, 500, 400, 300, 500
    )
    line_load_conc2 = controller.add_line_load_conc(
        load_case2.id, 3000, 2000, 600, 500, 400, 600
    )
    line_load_conc3 = controller.add_line_load_conc(
        load_case2.id, 4000, 3000, 700, 600, 500, 700
    )

    controller.apply_line_load(line_load_conc1, line1, [0.4, 0.3])
    controller.apply_line_load(line_load_conc1, line2, 0.5)
    controller.apply_line_load(line_load_conc2, line2, 0.4)
    controller.apply_line_load(line_load_conc1, line3, 0.9)

    # # Distributed Line Load
    line_load_dist1 = controller.add_line_load_dist(
        load_case3.id, 10, *range(100, 1300, 100), applied_to={}
    )
    line_load_dist2 = controller.add_line_load_dist(
        load_case3.id, 20, *range(200, 1400, 100), applied_to={}
    )
    line_load_dist3 = controller.add_line_load_dist(
        load_case3.id, 30, *range(300, 1500, 100), applied_to={}
    )

    controller.apply_line_load(line_load_dist1, line1, [20, 50])
    controller.apply_line_load(line_load_dist2, line2, 20)
    controller.apply_line_load(line_load_dist3, line3, 30)
    controller.apply_line_load(line_load_dist1, line2, 40)

    print(controller)

    viewer.render(controller)


if __name__ == "__main__":
    main()
