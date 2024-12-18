from typing import TYPE_CHECKING

import pyvista as pv

from geogeometry.geometry.shared.shared_components.BasePlotter import BasePlotter

if TYPE_CHECKING:
    from geogeometry.geometry.triangulation.TriangulationsCollection import TriangulationsCollection


class TriangulationsCollectionPlotter(BasePlotter):

    def __init__(self, triangulations_collection: 'TriangulationsCollection'):
        self.triangulations_collection: 'TriangulationsCollection' = triangulations_collection

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        for t in self.triangulations_collection:
            t.addToPyvistaPlotter(plotter)
