from typing import Optional, TYPE_CHECKING

from geogeometry.geometry.shared.BaseGeometryCollection import BaseGeometryCollection
from geogeometry.geometry.triangulation.collection_components.TriangulationsCollectionPlotter import \
    TriangulationsCollectionPlotter

if TYPE_CHECKING:
    from geogeometry.geometry.triangulation.Triangulation import Triangulation
    import pyvista as pv


class TriangulationsCollection(BaseGeometryCollection['Triangulation']):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

        self.plotter: TriangulationsCollectionPlotter = TriangulationsCollectionPlotter(self)

    def __str__(self) -> str:
        txt = f"TriangulationsCollection(name={self.getName()}, triangulations={len(self)})"
        return txt

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        self.plotter.addToPyvistaPlotter(plotter=plotter, **kwargs)

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        self.plotter.plot3d(screenshot=screenshot, filepath=filepath, **kwargs)
