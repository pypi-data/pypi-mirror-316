from typing import Literal, List, Any, Optional, Union

import pyvista as pv

from geogeometry.geometry.shared.BaseGeometry import BaseGeometry
from geogeometry.geometry.shared.BaseGeometryCollection import BaseGeometryCollection


class Figure3d(object):

    def __init__(self, engine: Literal['pyvista', 'paraview'] = 'pyvista'):

        self.engine: Literal['pyvista', 'paraview'] = engine

        self.plotter: Optional[Union[pv.Plotter]] = None
        self.elements: List[Union[BaseGeometry, BaseGeometryCollection]] = []

    def addElement(self, element: Any) -> None:
        self.elements += [element]

    def plot(self, screenshot: bool = False, filepath: Optional[str] = None):

        if self.plotter is None:
            if self.engine == 'pyvista':
                self.plotter = pv.Plotter(off_screen=screenshot)
            else:
                raise ValueError("Not yet implemented.")

        for e in self.elements:
            e.addToPyvistaPlotter(self.plotter)

        self.plotter.add_axes()

        if screenshot:
            if filepath is None:
                raise ValueError("Screenshot requested without filepath.")
            self.plotter.screenshot(filepath)  # Save the plot to an image file

        if not screenshot:
            self.plotter.show()
