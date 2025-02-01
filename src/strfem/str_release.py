from dataclasses import dataclass
from typing import ClassVar


@dataclass()
class Release:
    """
    Represents a structural release with configurable stiffness properties.

    Attributes:
        ku_free: Translational stiffness value for the free condition
        ku_rigid: Translational stiffness value for the rigid condition
        kr_free: Rotational stiffness value for the free condition
        kr_rigid: Rotational stiffness value for the rigid condition
        id: Unique identifier for the release
        name: Name of the release
        kux_start: Translational stiffness in the X-direction at the start of the release
        kuy_start: Translational stiffness in the Y-direction at the start of the release
        kuz_start: Translational stiffness in the Z-direction at the start of the release
        krx_start: Rotational stiffness about the X-axis at the start of the release
        kry_start: Rotational stiffness about the Y-axis at the start of the release
        krz_start: Rotational stiffness about the Z-axis at the start of the release
        kux_end: Translational stiffness in the X-direction at the end of the release
        kuy_end: Translational stiffness in the Y-direction at the end of the release
        kuz_end: Translational stiffness in the Z-direction at the end of the release
        krx_end: Rotational stiffness about the X-axis at the end of the release
        kry_end: Rotational stiffness about the Y-axis at the end of the release
        krz_end: Rotational stiffness about the Z-axis at the end of the release
    """

    # Class level constants for defining rigid and free conditions
    ku_free: ClassVar[float] = 1e-4
    ku_rigid: ClassVar[float] = 1e15
    kr_free: ClassVar[float] = 1e-4
    kr_rigid: ClassVar[float] = 1e15

    # Instance variables for stiffness values at the start and end of the release
    id: int
    name: str = "release"
    kux_start: float = ku_free
    kuy_start: float = ku_free
    kuz_start: float = ku_free
    krx_start: float = kr_free
    kry_start: float = kr_free
    krz_start: float = kr_free
    kux_end: float = ku_free
    kuy_end: float = ku_free
    kuz_end: float = ku_free
    krx_end: float = kr_free
    kry_end: float = kr_free
    krz_end: float = kr_free

    def __post_init__(self) -> None:
        """
        Post-initialization method to adjust stiffness values and compute the release status.

        Adjusts the stiffness values if they are zero, setting them to free values (ku_free or kr_free).
        Computes the stiffness arrays for start and end conditions, and computes the release status.
        """
        # Adjust stiffness values if they are zero
        for attr in [
            "kux_start",
            "kuy_start",
            "kuz_start",
            "kux_end",
            "kuy_end",
            "kuz_end",
        ]:
            if getattr(self, attr) == 0:
                setattr(self, attr, self.ku_free)

        for attr in [
            "krx_start",
            "kry_start",
            "krz_start",
            "krx_end",
            "kry_end",
            "krz_end",
        ]:
            if getattr(self, attr) == 0:
                setattr(self, attr, self.kr_free)

        # Compute stiffness arrays for start and end conditions
        self.stiffness_start: list[float] = [
            self.kux_start,
            self.kuy_start,
            self.kuz_start,
            self.krx_start,
            self.kry_start,
            self.krz_start,
        ]
        self.stiffness_end: list[float] = [
            self.kux_end,
            self.kuy_end,
            self.kuz_end,
            self.krx_end,
            self.kry_end,
            self.krz_end,
        ]

        # Compute release status
        self.status: list[str] = self._compute_release_status()
        self.status_start: list[str] = self.status[:6]
        self.status_end: list[str] = self.status[6:]

    def _compute_release_status(self) -> list[str]:
        """
        Compute the status for each degree of freedom (DOF) of the release,
        both at the start and end.

        Args:
            None

        Returns:
            list[str]: A list of status characters representing the degree of freedom statuses
                       ('f' for free, '_' for partially constrained, 'x' for rigid).
        """

        def get_status(k: float, is_translation: bool) -> str:
            """
            Determine the status ('f', '_', or 'x') based on the stiffness value.

            Args:
                k: Stiffness value for the degree of freedom
                is_translation: Boolean indicating whether the DOF is translational

            Returns:
                str: Status character ('f', '_', or 'x')
            """
            free_threshold = self.ku_free if is_translation else self.kr_free
            rigid_threshold = self.ku_rigid if is_translation else self.kr_rigid
            return "f" if k <= free_threshold else "x" if k >= rigid_threshold else "_"

        return [
            get_status(getattr(self, attr), is_translation)
            for attr, is_translation in [
                ("kux_start", True),
                ("kuy_start", True),
                ("kuz_start", True),
                ("krx_start", False),
                ("kry_start", False),
                ("krz_start", False),
                ("kux_end", True),
                ("kuy_end", True),
                ("kuz_end", True),
                ("krx_end", False),
                ("kry_end", False),
                ("krz_end", False),
            ]
        ]

    def __str__(self) -> str:
        """
        Return a formatted string displaying the release's stiffness status at the start and end.

        Returns:
            str: Formatted string containing the release's ID, name, and stiffness statuses.
        """
        status_str_start = (
            f"{''.join(self.status_start[:3])}, {''.join(self.status_start[3:])}"
        )
        status_str_end = (
            f"{''.join(self.status_end[:3])}, {''.join(self.status_end[3:])}"
        )
        return f"Release #{self.id} {self.name:<10}  S[{status_str_start}]  -->  E[{status_str_end}]"


def main() -> None:
    release1 = Release(
        1, "Pin", 1e15, 1e15, 1e15, 1e-4, 1e-4, 1e-4, 1e15, 1e15, 1e15, 1e-4, 1e-4, 1e-4
    )
    release2 = Release(
        2,
        "Rigid",
        1e15,
        1e15,
        1e15,
        1e-4,
        1e-4,
        1e-4,
        1e15,
        1e15,
        1e15,
        1e-4,
        1e-4,
        1e-4,
    )

    print(release1)
    print(release2)


if __name__ == "__main__":
    main()
