from dataclasses import dataclass, field
from strfem.str_line import Line


@dataclass()
class LineLoadConcentrated:
    """
    Represents a concentrated load applied to one or more structural lines.

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
    Fx: float = 0
    Fy: float = 0
    Fz: float = 0
    Mx: float = 0
    My: float = 0
    Mz: float = 0
    applied_to: dict[int, float | list[float]] = field(default_factory=dict)

    def apply(self, line: Line, xloc: list[float] | float = 0) -> None:
        """
        Applies the load to a specific structural line at the given location.

        Args:
            line (Str_line): The structural line to which the load is applied.
            locx (list[float] | float): The location along the line where the load is applied. Default is 0.
        """
        xloc = [xloc] if isinstance(xloc, float) else xloc
        self.applied_to.update({line.id: xloc})

    def remove(self, line: Line) -> None:
        """
        Removes the load from a specific structural line.

        Args:
            line (Str_line): The structural line from which the load is removed.
        """
        self.applied_to.pop(line.id)

    def __str__(self) -> str:
        """
        Prints a detailed description of the line load, including:
        - Forces and moments in each direction.
        - The lines to which the load is applied and their respective locations.
        """

        formatted_lines = ",".join(
            f"\n                    #{line_id} @ {xloc} m"
            for line_id, xloc in self.applied_to.items()
        )

        return (
            f"Line Load Concentrated #{self.id} \n"
            f"  Load Case #{self.load_case_id} \n"
            f"  Fx = {self.Fx:.2f} N \n"
            f"  Fy = {self.Fy:.2f} N \n"
            f"  Fz = {self.Fz:.2f} N \n"
            f"  Mx = {self.Mx:.2f} Nm \n"
            f"  My = {self.My:.2f} Nm \n"
            f"  Mz = {self.Mz:.2f} Nm \n"
            f"  Applied to lines: {formatted_lines if self.applied_to else 'Unassigned'} \n"
        )


def main() -> None:
    line_load1 = LineLoadConcentrated(1, 2, Fx=2343, Mx=1234)
    line_load2 = LineLoadConcentrated(2, 2, Fx=2343, Mx=1234)
    line_load3 = LineLoadConcentrated(3, 2, Fx=2343, Mx=1234)
    print(line_load1)
    print(line_load2)
    print(line_load3)


if __name__ == "__main__":
    main()
