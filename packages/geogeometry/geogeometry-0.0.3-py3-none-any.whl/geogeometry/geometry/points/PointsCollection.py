from typing import Optional, TYPE_CHECKING, Union, List

import numpy as np

from geogeometry.geometry.points.collection_components.PointsCollectionPlotter import PointsCollectionPlotter
from geogeometry.geometry.shared.BaseGeometryCollection import BaseGeometryCollection

if TYPE_CHECKING:
    import pyvista as pv


class PointsCollection(BaseGeometryCollection[np.ndarray]):

    def __init__(self, name: Optional[str] = None, points: Optional[Union[List, np.ndarray]] = None):
        super().__init__(name=name)

        if points is not None:
            self.setPoints(points=points)

        self.plotter: PointsCollectionPlotter = PointsCollectionPlotter(self)

    def setPoints(self, points: Union[List, np.ndarray]) -> None:
        if isinstance(points, list):
            points = np.array(points)
        self.elements = points

    def getPoints(self) -> Union[List, np.ndarray]:
        return self.elements

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        self.plotter.addToPyvistaPlotter(plotter=plotter, **kwargs)

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        self.plotter.plot3d(screenshot=screenshot, filepath=filepath, **kwargs)
