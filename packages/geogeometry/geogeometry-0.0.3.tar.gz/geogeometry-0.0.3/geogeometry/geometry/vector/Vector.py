from typing import Optional, Callable, List, Union, TYPE_CHECKING

import numpy as np

from geogeometry.geometry.shared.BaseGeometry import BaseGeometry

from geogeometry.geometry.vector.components.VectorMetrics import VectorMetrics
from geogeometry.geometry.vector.components.VectorProperties import VectorProperties
from geogeometry.geometry.vector.components.VectorQuerier import VectorQuerier
from geogeometry.geometry.vector.components.VectorTransformer import VectorTransformer

if TYPE_CHECKING:
    from pyvista import Plotter


def nodesToVector(func: Callable[..., List[np.ndarray]]) -> Callable[..., 'Vector']:
    def inner(vector: 'Vector', *args, **kwargs) -> 'Vector':
        nodes = func(vector, *args, **kwargs)
        return Vector(origin=nodes[0], tip=nodes[1])

    return inner


class Vector(BaseGeometry, VectorProperties):

    def __init__(self,
                 tip: Union[List, np.ndarray],
                 origin: Optional[Union[List, np.ndarray]] = None,
                 name: Optional[str] = None):
        super().__init__(name=name)

        if isinstance(tip, list):
            tip = np.array(tip)

        if origin is None:
            origin = np.zeros(tip.shape[0])

        self.setOrigin(origin=origin)
        self.setTip(tip=tip)

        self.metrics: VectorMetrics = VectorMetrics(self)
        self.querier: VectorQuerier = VectorQuerier(self)
        self.transformer: VectorTransformer = VectorTransformer(self)

        self.metrics.calculateMetrics()

    def __eq__(self, other_vector: 'Vector') -> bool:
        diff = self.getNodes() - other_vector.getNodes()
        if np.linalg.norm(diff):
            return False
        return True

    def __str__(self) -> str:
        txt = f"Vector(origin={self.getOrigin()}, tip={self.getTip()})"
        return txt

    def createNormalizedVector(self, n: np.ndarray) -> None:
        self.setNormalizedVector(normalized_vector=Vector(tip=n))

    # QUERIER
    def calculateAngleWithVector(self, other_vector: 'Vector') -> float:
        return self.querier.calculateAngleWithVector(other_vector=other_vector)

    # TRANSFORMATIONS
    def reverse(self) -> None:
        self.transformer.reverse()

    def rotateByRotationMatrix(self, rotation_matrix: np.ndarray) -> None:
        self.transformer.rotateByRotationMatrix(rotation_matrix=rotation_matrix)

    def addToPyvistaPlotter(self, plotter: 'Plotter', **kwargs) -> None: ...
    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None: ...
