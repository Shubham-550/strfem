from dataclasses import dataclass, field
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

    # Computed fields
    stiffness: list[float] = field(init=False)
    status: list[str] = field(init=False)

    def __post_init__(self):
        # Normalize zero stiffness values
        self.kux = self.ku_free if self.kux == 0 else self.kux
        self.kuy = self.ku_free if self.kuy == 0 else self.kuy
        self.kuz = self.ku_free if self.kuz == 0 else self.kuz
        self.krx = self.kr_free if self.krx == 0 else self.krx
        self.kry = self.kr_free if self.kry == 0 else self.kry
        self.krz = self.kr_free if self.krz == 0 else self.krz

        # Compute stiffness array
        self.stiffness = [self.kux, self.kuy, self.kuz, self.krx, self.kry, self.krz]

        # Compute support status
        self.status = self._compute_support_status()

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

            if k <= free_threshold:
                return "f"  # Free
            elif k >= rigid_threshold:
                return "x"  # Fixed
            else:
                return "_"  # Partially constrained

        # Compute status for translation and rotation DOFs
        translation_status = [
            get_status(self.kux, True),
            get_status(self.kuy, True),
            get_status(self.kuz, True),
        ]

        rotation_status = [
            get_status(self.krx, False),
            get_status(self.kry, False),
            get_status(self.krz, False),
        ]

        return translation_status + rotation_status

    def is_free(self, stiffness, free_threshold, rigid_threshold):
        """
        Determines if the stiffness value represents a free or fixed support.

        Args:
            stiffness (float): The stiffness value to evaluate.
            free_threshold (float): Threshold below which the support is considered free.

        Returns:
            str: "f" if free, "x" if fixed.
        """
        if stiffness <= free_threshold:
            return "f"
        elif stiffness >= rigid_threshold:
            return "x"
        else:
            return "_"

    def __str__(self) -> str:
        """
        Prints the status of the support's stiffness properties as free or fixed.
        """

        status_str = "".join(self.status[:3]) + "," + "".join(self.status[3:])
        return f"Supports #{self.id} {self.name} [{status_str}]"
