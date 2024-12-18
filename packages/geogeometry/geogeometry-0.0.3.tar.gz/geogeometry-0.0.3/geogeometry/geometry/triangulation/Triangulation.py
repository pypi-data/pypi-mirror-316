from typing import Optional, TYPE_CHECKING

from geogeometry.geometry.shared.BaseGeometry import BaseGeometry
from geogeometry.geometry.triangulation.components.TriangulationPlotter import TriangulationPlotter
from geogeometry.geometry.triangulation.components.TriangulationProperties import TriangulationProperties

if TYPE_CHECKING:
    from pyvista import Plotter


class Triangulation(BaseGeometry, TriangulationProperties):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

        self.plotter: TriangulationPlotter = TriangulationPlotter(self)

    def __len__(self) -> int:
        if self.getFaces() is None:
            return 0
        return len(self.getFaces())

    def __str__(self) -> str:
        txt = f"Triangle(name={self.getName()}, faces={len(self)})"
        return txt

    def addToPyvistaPlotter(self, plotter: 'Plotter', **kwargs) -> None:
        self.plotter.addToPyvistaPlotter(plotter=plotter)

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        self.plotter.plot3d(screenshot=screenshot, filepath=filepath)
