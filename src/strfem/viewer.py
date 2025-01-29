import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from typing import Optional


class Viewer:
    def __init__(
        self,
        node_size: float = 0.1,
        line_width: float = 1.5,
        figsize: tuple[int, int] = (10, 8),
        theme: str = "default",
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

        self.node_size: float = node_size
        self.line_width: float = line_width

        # Enhanced figure configuration
        self.fig = plt.figure(figsize=figsize)
        # self.ax = plt.axes(projection="3d")
        self.ax = self.fig.add_subplot(projection="3d")

        # Visualization parameters
        self.node_color: str = "red"
        self.line_color: str = "blue"
        self.alpha: float = 0.7

    def render_node(
        self, node, color: Optional[str] = None, size: Optional[float] = None
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
            c=color or self.node_color,
            # s=size or self.node_size,
            alpha=self.alpha,
            edgecolors="black",
            linewidths=0.5,
        )

    def render_line(
        self, line, color: Optional[str] = None, width: Optional[float] = None
    ) -> None:
        """
        Render individual line with customizable appearance.

        Args:
            line: Line to render
            color: Line color
            width: Line width
        """
        coord = np.array([line.node1.coord, line.node2.coord]).T
        self.ax.plot(
            coord[0],
            coord[1],
            coord[2],
            color=color or self.line_color,
            linewidth=width or self.line_width,
            alpha=self.alpha,
        )

    def render(
        self,
        controller,
        title: str = "Structural Model",
        show_grid: bool = True,
        equal_aspect: bool = True,
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
