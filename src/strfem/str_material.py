from dataclasses import dataclass


@dataclass()
class Material:
    """
    Material of the line
    Default values are for Steal (E = 200 GPa, G = 75 GPa, Poisson's ratio = 0.3)

    Attributes:
        id: Unique Identifier of the Material
        name: Namme of the material
        E: Youngs Modulus of Elasticity
        G: Shear Modulus
        nu: Poisson's ratio
    """

    id: int
    name: str = "Steel"
    E: float = 200e9
    G: float = 75e9
    nu: float = 0.3

    def __str__(self):
        return f"Material #{self.id:<3} ({self.name:<10}) E ={self.E: 5.2e} Pa"
