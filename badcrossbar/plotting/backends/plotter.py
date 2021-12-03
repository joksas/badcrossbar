from abc import ABC, abstractmethod
from enum import IntEnum, auto


class Shape(IntEnum):
    LINE = auto()
    SEMICIRCLE = auto()
    CLOSE = auto()


class Plotter(ABC):
    @abstractmethod
    def path(self, vertex_coords: list[tuple[float, float]], vertex_types: list[Shape]) -> None:
        """Draws a path."""
