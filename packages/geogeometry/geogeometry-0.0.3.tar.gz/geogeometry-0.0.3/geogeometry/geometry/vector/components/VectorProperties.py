from typing import Optional, TYPE_CHECKING, Literal, Union, List

import numpy as np

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


class VectorProperties(object):

    def __init__(self):

        self.origin: Optional[np.ndarray] = None
        self.tip: Optional[np.ndarray] = None

        self.nodes: np.array = np.full((2, 3), np.nan)

        self.length: Optional[float] = None

        self.is_unitary: Optional[bool] = None
        self.is_position_vector: Optional[bool] = None  # origin=(0,0,0)

        self.normalized_vector: Optional['Vector'] = None

        self.dip: Optional[float] = None
        self.dipdir: Optional[float] = None

    def setOrigin(self, origin: Union[List, np.ndarray]) -> None:
        if isinstance(origin, list):
            origin = np.array(origin)
        self.origin = origin
        self.nodes[0] = origin

    def setTip(self, tip: Union[List, np.ndarray]) -> None:
        if isinstance(tip, list):
            tip = np.array(tip)
        self.tip = tip
        self.nodes[1] = tip

    def setNodes(self, nodes: Union[List, np.ndarray]) -> None:
        if len(nodes) != 2:
            raise ValueError("Trying to define an explicit vector without 2 nodes.")
        self.setOrigin(origin=nodes[0])
        self.setTip(tip=nodes[1])

    def setLength(self, length: float) -> None:
        self.length = length

    def setIsUnitary(self, is_unitary: bool) -> None:
        self.is_unitary = is_unitary

    def setIsPositionVector(self, is_position_vector: bool) -> None:
        self.is_position_vector = is_position_vector

    def setNormalizedVector(self, normalized_vector: 'Vector') -> None:
        self.normalized_vector = normalized_vector

    def setDip(self, dip: float) -> None:
        self.dip = dip

    def setDipdir(self, dipdir: float) -> None:
        self.dipdir = dipdir

    def getOrigin(self) -> np.ndarray:
        return self.origin

    def getTip(self) -> np.ndarray:
        return self.tip

    def getNodes(self) -> np.ndarray:
        return self.nodes

    def getLength(self) -> float:
        return self.length

    def isUnitary(self) -> bool:
        return self.is_unitary

    def isPositionVector(self) -> bool:
        return self.is_position_vector

    def getNormalizedVector(self) -> 'Vector':
        return self.normalized_vector

    def getDip(self) -> float:
        return self.dip

    def getDipdir(self) -> float:
        return self.dipdir
