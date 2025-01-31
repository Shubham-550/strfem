from dataclasses import dataclass


@dataclass()
class LoadCase:
    id: int
    name: str

    def __str__(self) -> str:
        return f"Load Case #{self.id} ({self.name})"
