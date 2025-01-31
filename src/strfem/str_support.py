from dataclasses import dataclass
from typing import ClassVar


@dataclass()
class Support:
    """
    Represents a structural support with configurable stiffness properties.

    Attributes:
        id: Unique identifier for the support
        name: Support name
        stiffness: Translational and rotational stiffness values
    """

    # Class level constants
    ku_rigid: ClassVar[float] = 1e15
    ku_free: ClassVar[float] = 1e-4
    kr_rigid: ClassVar[float] = 1e15
    kr_free: ClassVar[float] = 1e-4

    # Instance Variables
    id: int
    name: str = "support"
    kux: float = ku_free
    kuy: float = ku_free
    kuz: float = ku_free
    krx: float = kr_free
    kry: float = kr_free
    krz: float = kr_free

    def __post_init__(self):
        for attr in ["kux", "kuy", "kuz"]:
            if getattr(self, attr) == 0:
                setattr(self, attr, self.ku_free)

        for attr in ["krx", "kry", "krz"]:
            if getattr(self, attr) == 0:
                setattr(self, attr, self.kr_free)

        # Compute stiffness array
        self.stiffness: list[float] = [
            self.kux,
            self.kuy,
            self.kuz,
            self.krx,
            self.kry,
            self.krz,
        ]

        # Compute support status
        self.status: list[str] = self._compute_support_status()

    def _compute_support_status(self) -> list[str]:
        """
        Compute support status for each degree of freedom.

        Returns:
            List of support status characters
        """

        def get_status(k: float, is_translation: bool) -> str:
            """
            Determine support status for a single degree of freedom.

            Args:
                k: Stiffness value
                is_translation: Whether it's a translational DOF

            Returns:
                Support status character
            """
            free_threshold = self.ku_free if is_translation else self.kr_free
            rigid_threshold = self.ku_rigid if is_translation else self.kr_rigid

            return "f" if k <= free_threshold else "x" if k >= rigid_threshold else "_"

        return [
            get_status(getattr(self, attr), is_translation)
            for attr, is_translation in [
                ("kux", True),
                ("kuy", True),
                ("kuz", True),
                ("krx", False),
                ("kry", False),
                ("krz", False),
            ]
        ]

    def __str__(self) -> str:
        """
        Prints the status of the support's stiffness properties as free or fixed.
        """

        status_str = "".join(self.status[:3]) + "," + "".join(self.status[3:])
        return f"Support #{self.id} {self.name:<10} [{status_str}]"


def main() -> None:
    support1 = Support(1, "Pin", 1e15, 1e15, 1e15, 1e-4, 1e-4, 1e-4)
    support2 = Support(2, "Rigid", 1e15, 1e15, 1e15, 1e-4, 1e-4, 1e-4)

    print(support1)
    print(support2)


if __name__ == "__main__":
    main()
