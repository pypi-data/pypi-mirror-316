from typing import Optional, Literal

import numpy as np


class BaseGeometryProperties(object):

    def __init__(self, name: Optional[str] = None):
        super().__init__()

        self.name: Optional[str] = name
        self.id: int = id(self)

        # Metrics
        self.dimensions: Optional[Literal[2, 3]] = None
        self.limits: Optional[np.ndarray] = None
        self.centroid: Optional[np.ndarray] = None

        # Plot properties
        self.color: str = 'red'
        self.opacity: float = 1.0

    def setName(self, name: str) -> None:
        self.name = name

    def setId(self, _id: int) -> None:
        self.id = _id

    def setDimensions(self, dimensions: Literal[2, 3]) -> None:
        self.dimensions = dimensions

    def setLimits(self, limits: np.ndarray) -> None:
        self.limits = limits

    def setCentroid(self, centroid: np.ndarray) -> None:
        self.centroid = centroid

    def setColor(self, color: str) -> None:
        self.color = color

    def setOpacity(self, opacity: float) -> None:
        self.opacity = opacity

    def getName(self) -> str:
        return self.name

    def getId(self) -> int:
        return self.id

    def getDimensions(self) -> Optional[Literal[2, 3]]:
        return self.dimensions

    def getLimits(self) -> Optional[np.ndarray]:
        return self.limits

    def getCentroid(self) -> Optional[np.ndarray]:
        return self.centroid

    def getColor(self) -> str:
        return self.color

    def getOpacity(self) -> float:
        return self.opacity

