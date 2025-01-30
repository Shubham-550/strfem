from dataclasses import dataclass


@dataclass()
class Material:
    id: int
    name: str
    E: float
    G: float
    nu: float

    def __str__(self):
        return f"Material #{self.id:<3} ({self.name:<10}) E ={self.E: 5.2e} Pa"
