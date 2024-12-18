import copy
from abc import ABC, abstractmethod
from typing import Union, List, TypeVar, Optional, TYPE_CHECKING

import gzip
import lzma
import pickle

from geogeometry.geometry.shared.BaseGeometryProperties import BaseGeometryProperties

if TYPE_CHECKING:
    import pyvista as pv

T = TypeVar('T')


class BaseGeometry(ABC, BaseGeometryProperties):

    def __init__(self, name: Optional[str] = None):
        super().__init__(name=name)

    def copy(self):
        copy_p = copy.deepcopy(self)
        copy_p.setId(_id=id(copy_p))
        return copy_p

    @abstractmethod
    def addToPyvistaPlotter(self, plotter: 'pv.Plotter', **kwargs) -> None: ...

    @abstractmethod
    def plot3d(self, screenshot: bool = False, filepath: Optional[str] = None, **kwargs) -> None: ...

    # IO
    def save(self, savepath: str) -> None:
        if '.pkl.gz' in savepath:
            pickle.dump(self, gzip.open(savepath, 'wb'), pickle.HIGHEST_PROTOCOL)
        elif 'pkl.xz' in savepath:
            pickle.dump(self, lzma.open(savepath, 'wb'), pickle.HIGHEST_PROTOCOL)
        else:
            pickle.dump(self, open(savepath, 'wb'), pickle.HIGHEST_PROTOCOL)

        print(f'{self.__class__.__name__} instance saved at: "' + savepath + '"')

    @staticmethod
    def load(load_path) -> T:
        if '.pkl.gz' in load_path:
            return pickle.load(gzip.open(load_path, 'rb'))
        elif 'pkl.xz' in load_path:
            return pickle.load(lzma.open(load_path, 'rb'))
        else:
            return pickle.load(open(load_path, 'rb'))
