from typing import Optional, Union, List, Literal

import numpy as np


class PolylineProperties(object):

    def __init__(self):

        self.nodes: Optional[np.ndarray] = None
        self.segments: Optional[np.ndarray] = None

        self.closed: Optional[bool] = None
        self.length: Optional[float] = None

        self.mid_point: Optional[np.ndarray] = None

        # 2D properties
        self.area: Optional[float] = None

        # Plot properties
        self.line_width: float = 2.

    def setNodes(self, nodes: Union[List, np.ndarray]) -> None:
        self.nodes = np.array(nodes)
        self.segments = [[j, j + 1] for j, n in enumerate(self.nodes[:-1])]

    def setClosed(self, closed: bool) -> None:
        self.closed = closed

    def setLength(self, length: float) -> None:
        self.length = length

    def setMidPoint(self, mid_point: np.ndarray) -> None:
        self.mid_point = mid_point

    def setArea(self, area: float) -> None:
        self.area = area

    def setLineWidth(self, line_width: float) -> None:
        self.line_width = line_width

    def getNodes(self) -> Optional[np.ndarray]:
        return self.nodes

    def getSegments(self) -> Optional[np.ndarray]:
        return self.segments

    def isClosed(self) -> Optional[bool]:
        return self.closed

    def getLength(self) -> Optional[float]:
        return self.length

    def getMidPoints(self) -> Optional[np.ndarray]:
        return self.mid_point

    def getArea(self) -> Optional[float]:
        return self.area

    def getLineWidth(self) -> float:
        return self.line_width
