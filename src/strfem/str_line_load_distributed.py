from dataclasses import dataclass, field

from strfem.str_line import Line


@dataclass()
class LineLoadDistributed:
    """
    Represents a trapezoidal load applied to one or more structural lines.

    Attributes:
        id (int): Unique identifier for the line load.
        Fx (float): Force in the X direction (N). Default is 0.
        Fy (float): Force in the Y direction (N). Default is 0.
        Fz (float): Force in the Z direction (N). Default is 0.
        Mx (float): Moment about the X axis (Nm). Default is 0.
        My (float): Moment about the Y axis (Nm). Default is 0.
        Mz (float): Moment about the Z axis (Nm). Default is 0.
        applied_to (dict): A dictionary mapping line IDs (`int`) to load locations (`float`).

    Methods:
        apply(line: Str_line, locx: list[float] | float = 0):
            Applies the load to a specific line at a given location.

        remove(line: Str_line):
            Removes the load from a specific line.

        to_string():
            Prints a detailed description of the line load, including the forces, moments,
            and the lines to which the load is applied, with their respective locations.
    """

    id: int
    load_case_id: int
    xspan: float = 0

    # Load at the start
    Fx_start: float = 0
    Fy_start: float = 0
    Fz_start: float = 0
    Mx_start: float = 0
    My_start: float = 0
    Mz_start: float = 0

    # Load at the end
    Fx_end: float = 0
    Fy_end: float = 0
    Fz_end: float = 0
    Mx_end: float = 0
    My_end: float = 0
    Mz_end: float = 0

    applied_to: dict[int, list[float]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.xstart = 0
        self.xend = self.xstart + self.xspan

    def apply(self, line: Line, xloc: float | list[float] = 0.0) -> None:
        """
        Applies the load to a specific structural line at the given location.

        Args:
            line (Line): The structural line to which the load is applied.
            xloc (list[float] | float): The location along the line where the load is applied.
                                        Default is 0.0.
        """
        loc = (
            [float(xloc)]
            if isinstance(xloc, (int, float))
            else [float(val) for val in xloc]
        )
        self.applied_to[line.id] = loc

    def remove(self, line: Line) -> None:
        """
        Removes the load from a specific structural line.

        Args:
            line (Str_line): The structural line from which the load is removed.
        """
        self.applied_to.pop(line.id)

    def __str__(self) -> str:
        formatted_lines = []
        for line_id, xloc in self.applied_to.items():
            for x in xloc:
                formatted_lines.append(
                    f"\n                    #{line_id} @ {x:5.2f} m  -->  {x + self.xspan:5.2f} m"
                )

        formatted_lines_str = ",".join(formatted_lines)

        return (
            f"Line Load Distributed #{self.id} \n"
            f"      Load Case #{self.load_case_id} \n"
            f"      Fx = {self.Fx_start:.2f} N   -->  Fx = {self.Fx_end:.2f} N  \n"
            f"      Fy = {self.Fy_start:.2f} N   -->  Fy = {self.Fy_end:.2f} N  \n"
            f"      Fz = {self.Fz_start:.2f} N   -->  Fz = {self.Fz_end:.2f} N  \n"
            f"      Mx = {self.Mx_start:.2f} Nm  -->  Mx = {self.Mx_end:.2f} Nm \n"
            f"      My = {self.My_start:.2f} Nm  -->  My = {self.My_end:.2f} Nm \n"
            f"      Mz = {self.Mz_start:.2f} Nm  -->  Mz = {self.Mz_end:.2f} Nm \n"
            f"      Applied to Lines: {formatted_lines_str if self.applied_to else 'Unassigned'} \n"
        )


def main() -> None:
    line_load1 = LineLoadDistributed(0, 10, *range(100, 1300, 100), applied_to={})

    print(line_load1)


if __name__ == "__main__":
    main()
