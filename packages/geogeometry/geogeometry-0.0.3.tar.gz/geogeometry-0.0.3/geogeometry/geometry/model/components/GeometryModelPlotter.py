from typing import TYPE_CHECKING, Optional

import pyvista as pv

from geogeometry.geometry.shared.shared_components.BasePlotter import BasePlotter

if TYPE_CHECKING:
    from geogeometry.geometry.model.GeometryModel import GeometryModel


class GeometryModelPlotter(BasePlotter):

    def __init__(self, model: 'GeometryModel'):
        self.model: 'GeometryModel' = model

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        if len(self.model.getPolylines()):
            self.model.getPolylines().addToPyvistaPlotter(plotter=plotter, **kwargs)

        if len(self.model.getTriangulations()):
            self.model.getTriangulations().addToPyvistaPlotter(plotter=plotter, **kwargs)

        if len(self.model.getPoints()):
            self.model.getPoints().addToPyvistaPlotter(plotter=plotter, **kwargs)

