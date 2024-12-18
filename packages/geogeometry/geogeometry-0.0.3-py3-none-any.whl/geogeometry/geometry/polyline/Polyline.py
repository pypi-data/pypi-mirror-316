from typing import Union, List, Optional, TYPE_CHECKING, Iterable

import numpy as np

from geogeometry.geometry.polyline.components.PolylineTransformer import PolylineTransformer
from geogeometry.geometry.shared.BaseGeometry import BaseGeometry

from geogeometry.geometry.polyline.components.PolylinePlotter import PolylinePlotter
from geogeometry.geometry.polyline.components.PolylineProperties import PolylineProperties

from geogeometry.geometry.polyline.components.PolylineMetrics import PolylineMetrics
from geogeometry.geometry.polyline.components.PolylineQuerier import PolylineQuerier

if TYPE_CHECKING:
    from pyvista import Plotter


class Polyline(BaseGeometry, PolylineProperties):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

        self.metrics: PolylineMetrics = PolylineMetrics(self)
        self.querier: PolylineQuerier = PolylineQuerier(self)
        self.transformer: PolylineTransformer = PolylineTransformer(self)

        self.plotter: PolylinePlotter = PolylinePlotter(self)

    def __len__(self) -> int:
        if self.getNodes() is None:
            return 0
        return len(self.getNodes())

    def __iter__(self) -> Iterable[np.ndarray]:
        for n in self.getNodes():
            yield n

    def __str__(self) -> str:
        txt = f"Polyline(name={self.getName()}, nodes={len(self)}, closed={self.isClosed()})"
        return txt

    def setNodes(self, nodes: Union[List, np.ndarray]) -> None:
        super().setNodes(nodes=nodes)
        self.metrics.calculateMetrics()

    # QUERIES
    def getPointAtDistanceFromOrigin(self, distance: float) -> Optional[np.ndarray]:
        return self.querier.getPointAtDistanceFromOrigin(distance=distance)

    # TRANSFORMATIONS
    def translate(self, translation_vector: Union[List, np.ndarray]) -> None:
        self.transformer.translate(translation_vector=translation_vector)

    def rotateByRotationMatrix(self, rotation_matrix: np.ndarray) -> None:
        self.transformer.rotateByRotationMatrix(rotation_matrix=rotation_matrix)

    # PLOTS
    def addToPyvistaPlotter(self, plotter: 'Plotter', **kwargs) -> None:
        self.plotter.addToPyvistaPlotter(plotter=plotter, **kwargs)

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        self.plotter.plot3d(screenshot=screenshot, filepath=filepath, **kwargs)
