from abc import ABC, abstractmethod
from typing import Optional

import pyvista as pv


class BasePlotter(ABC):

    @abstractmethod
    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None: ...

    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None:
        plotter = pv.Plotter(off_screen=screenshot)

        self.addToPyvistaPlotter(plotter=plotter, **kwargs)

        plotter.add_axes()

        if screenshot:
            if filepath is None:
                raise ValueError("Screenshot requested without filepath.")
            plotter.screenshot(filepath)  # Save the plot to an image file

        if not screenshot:
            plotter.show()
