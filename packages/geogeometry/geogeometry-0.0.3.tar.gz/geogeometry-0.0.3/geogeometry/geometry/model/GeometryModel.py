from typing import Union, List, Optional, TYPE_CHECKING

import numpy as np

from geogeometry.geometry.model.components.GeometryModelPlotter import GeometryModelPlotter
from geogeometry.geometry.shared.BaseGeometry import BaseGeometry
from geogeometry.geometry.model.components.GeometryModelProperties import GeometryModelProperties

if TYPE_CHECKING:
    from pyvista import Plotter


class GeometryModel(BaseGeometry, GeometryModelProperties):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

        self.plotter: GeometryModelPlotter = GeometryModelPlotter(self)

    def __len__(self) -> int:
        total = 0
        total += len(self.getTriangulations())
        total += len(self.getPolylines())
        return total

    def __str__(self) -> str:
        txt = (f"GeometryModel(name={self.getName()}, "
               f"triangulations={len(self.getTriangulations())}, "
               f"polylines={len(self.getPolylines())})")
        return txt

    def translate(self, translation_vector: Union[List, np.ndarray]) -> None: ...
    def calculateLimits(self) -> None: ...
    def calculateCentroid(self) -> None: ...

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        self.plotter.addToPyvistaPlotter(plotter=plotter, **kwargs)

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        self.plotter.plot3d(screenshot=screenshot, filepath=filepath, **kwargs)
