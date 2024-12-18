from typing import TYPE_CHECKING, Optional

import numpy as np
import pyvista as pv

from geogeometry.geometry.shared.shared_components.BasePlotter import BasePlotter

if TYPE_CHECKING:
    from geogeometry.geometry.polyline.Polyline import Polyline


class PolylinePlotter(BasePlotter):

    def __init__(self, polyline: 'Polyline'):
        self.polyline: 'Polyline' = polyline

    def _getPyVistaPolyline(self) -> pv.PolyData:
        lines = np.hstack([[len(self.polyline.getNodes())], np.arange(len(self.polyline.getNodes()))])
        return pv.PolyData(self.polyline.getNodes(), lines=lines)

    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None:
        plotter.add_mesh(self._getPyVistaPolyline(),
                         color=self.polyline.getColor(),
                         opacity=self.polyline.getOpacity(),
                         line_width=self.polyline.getLineWidth())
