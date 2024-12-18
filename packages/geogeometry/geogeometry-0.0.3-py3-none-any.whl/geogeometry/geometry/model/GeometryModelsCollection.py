from typing import Optional, TYPE_CHECKING

from geogeometry.geometry.model.collection_components.GeometryModelsCollectionPlotter import GeometryModelsCollectionPlotter
from geogeometry.geometry.shared.BaseGeometryCollection import BaseGeometryCollection
from geogeometry.geometry.polyline.PolylinesCollection import PolylinesCollection
from geogeometry.geometry.triangulation.TriangulationsCollection import TriangulationsCollection

if TYPE_CHECKING:
    from geogeometry.geometry.model.GeometryModel import GeometryModel


class GeometryModelsCollection(BaseGeometryCollection['GeometryModel']):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

        self.plotter: GeometryModelsCollectionPlotter = GeometryModelsCollectionPlotter(self)

    def __str__(self) -> str:
        txt = f"GeometryModelsCollection(name={self.getName()}, models={len(self)})"
        return txt

    def deleteEmptyModels(self) -> None:

        empty_models = [e for e in self if not len(e)]
        for m in empty_models:
            self.deleteElement(identifier=m.getName())

    def getAllTriangulations(self) -> TriangulationsCollection:
        all_triangulations = TriangulationsCollection()

        for m in self:
            for t in m.getTriangulations():
                all_triangulations.addElement(t)

        return all_triangulations

    def getAllPolylines(self) -> PolylinesCollection:
        all_polylines = PolylinesCollection()

        for m in self:
            for p in m.getPolylines():
                all_polylines.addElement(p)

        return all_polylines

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        self.plotter.addToPyvistaPlotter(plotter=plotter, **kwargs)

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        self.plotter.plot3d(screenshot=screenshot, filepath=filepath, **kwargs)
