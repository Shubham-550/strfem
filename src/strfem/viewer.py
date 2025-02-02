import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import numpy.typing as npt

from strfem.log import setup_controller_logging


class Viewer:
    # Local Axis colours
    x_axis_color: str = "b"
    y_axis_color: str = "g"
    z_axis_color: str = "r"

    # Arrow props
    arrow_len: float = 0.5
    arrow_tip_size: float = 0.25
    arrow_width: float = 0.1

    local_axis_thickness: float = 2

    def __init__(
        self,
        node_size: float = 20,
        line_width: float = 1.5,
        figsize: tuple[int, int] = (10, 8),
        theme: str = "ggplot",
    ) -> None:
        """
        Initialize 3D visualization viewer.

        Args:
            node_size: Size of nodes in scatter plot
            line_width: Width of line elements
            figsize: Figure size (width, height)
            theme: Matplotlib style theme
        """

        plt.style.use(theme)

        self.node_size = node_size
        self.line_width = line_width

        self.fig = plt.figure(figsize=figsize)
        # self.ax = plt.axes(projection="3d")
        self.ax = self.fig.add_subplot(projection="3d")

        # Visualization parameters
        self.node_color: str = "magenta"
        self.line_color: str = "black"
        self.alpha: float = 0.7

        self.logger = setup_controller_logging()

    def render_node(
        self, node, color: str | None = None, size: float | None = None
    ) -> None:
        """
        Render individual node with customizable appearance.

        Args:
            node: Node to render
            color: Node color
            size: Node size
        """
        self.ax.scatter(
            node.x,
            node.y,
            node.z,
            s=size or self.node_size,
            c=color or self.node_color,
            alpha=self.alpha,
            edgecolors="black",
            linewidths=0.5,
        )

    def render_line(
        self, line, color: str | None = None, width: float | None = None
    ) -> None:
        """
        Render individual line with customizable appearance.

        Args:
            line: Line to render
            color: Line color
            width: Line width
        """
        # x, y, z = np.array([line.node1.coord, line.node2.coord]).T

        x, y, z = np.column_stack((line.node1.coord, line.node2.coord))
        self.logger.info(f"{x = } | {y = } | {z = }")

        self.ax.plot(
            x,
            y,
            z,
            color=color or self.line_color,
            linewidth=width or self.line_width,
            alpha=self.alpha,
        )

    def plot_arrow(
        self,
        origin: npt.NDArray[np.float64],
        vec: npt.NDArray[np.float64],
        color: str,
        thickness: float,
    ):
        arrow_end: npt.NDArray[np.float64] = origin + vec * self.arrow_len

        x, y, z = np.column_stack((origin, arrow_end))
        self.logger.info(f"{origin = } | {vec = }")
        self.logger.info(f"{x = } | {y = } | {z = }")

        self.ax.plot(
            x,
            y,
            z,
            color=color or self.line_color,
            linewidth=thickness,
            alpha=self.alpha,
        )

    def render(
        self,
        controller,
        title: str = "Structural Model",
        show_grid: bool = False,
        equal_aspect: bool = False,
    ) -> None:
        """
        Render complete structural model.

        Args:
            controller: Model controller
            title: Plot title
            show_grid: Display grid lines
            equal_aspect: Use equal aspect ratio
        """
        # Render nodes and lines
        for node in controller.nodes:
            self.render_node(node)

        for line in controller.lines:
            self.render_line(line)
            self.plot_arrow(
                line.CG, line.vx, Viewer.x_axis_color, Viewer.local_axis_thickness
            )
            self.plot_arrow(
                line.CG, line.vy, Viewer.y_axis_color, Viewer.local_axis_thickness
            )
            self.plot_arrow(
                line.CG, line.vz, Viewer.z_axis_color, Viewer.local_axis_thickness
            )

        # Styling and labeling
        self.ax.set_title(title, fontsize=15, fontweight="bold")
        self.ax.set_xlabel("X", fontsize=10)
        self.ax.set_ylabel("Y", fontsize=10)
        self.ax.set_zlabel("Z", fontsize=10)  # type: ignore

        # Optional grid
        if show_grid:
            self.ax.grid(True, linestyle="--", linewidth=0.5)

        # Set equal aspect ratio
        if equal_aspect:
            self.ax.set_box_aspect((1, 1, 1))  # type:ignore

        self.ax.set_aspect("equal", adjustable="box")
        # Tight layout
        plt.tight_layout()

        # Show plot
        plt.show()

    # def save_figure(
    #     self, filename: str = "structural_model.png", dpi: int = 300
    # ) -> None:
    #     """
    #     Save rendered figure.
    #
    #     Args:
    #         filename: Output filename
    #         dpi: Resolution of saved image
    #     """
    #     plt.savefig(filename, dpi=dpi, bbox_inches="tight")
    #     plt.close(self.fig)
