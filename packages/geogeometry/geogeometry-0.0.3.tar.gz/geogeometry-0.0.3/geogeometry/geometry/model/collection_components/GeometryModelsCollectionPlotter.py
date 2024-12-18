from typing import TYPE_CHECKING

import pyvista as pv

from geogeometry.geometry.shared.shared_components.BasePlotter import BasePlotter

if TYPE_CHECKING:
    from geogeometry.geometry.model.GeometryModelsCollection import GeometryModelsCollection

class GeometryModelsCollectionPlotter(BasePlotter):

    def __init__(self, geometrymodels_collection: 'GeometryModelsCollection'):
        self.geometrymodels_collection: 'GeometryModelsCollection' = geometrymodels_collection

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        for m in self.geometrymodels_collection:
            m.addToPyvistaPlotter(plotter=plotter, **kwargs)