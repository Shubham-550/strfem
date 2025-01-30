from dataclasses import dataclass


@dataclass()
class Section:
    """
    Cross-Seciton of the line

    Attributes:
        id: Unique identifier of the Section
        name: Name of the section
        Ax: Area of the plane normal to local x-axis
        Ix: MoI about local x-axis (Polar MoI)
        Iy: MoI about local y-axis (MoI about horizontal axis)
        Iz: MoI about local z-axis (MoI about vertical axis)
    """

    id: int
    name: str
    Ax: float
    Ix: float
    Iy: float
    Iz: float

    # TODO:add a list of local coordinates for rendering

    def __str__(self) -> str:
        return f"Section #{self.id} ({self.name})"
