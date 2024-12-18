from typing import Optional, TYPE_CHECKING

from geogeometry.geometry.polyline.collection_components.PolylinesCollectionPlotter import PolylinesCollectionPlotter
from geogeometry.geometry.shared.BaseGeometryCollection import BaseGeometryCollection

if TYPE_CHECKING:
    from geogeometry.geometry.polyline.Polyline import Polyline
    import pyvista as pv
    from geogeometry.graphics.Figure3d import Figure3d


class PolylinesCollection(BaseGeometryCollection['Polyline']):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

        self.plotter: PolylinesCollectionPlotter = PolylinesCollectionPlotter(self)

    def __str__(self) -> str:
        txt = f"PolylinesCollection(name={self.getName()}, polylines={len(self)})"
        return txt

    def addToFigure3d(self, figure_3d: 'Figure3d') -> None:
        figure_3d.addElement(self)

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        self.plotter.addToPyvistaPlotter(plotter=plotter, **kwargs)

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        self.plotter.plot3d(screenshot=screenshot, filepath=filepath, **kwargs)
