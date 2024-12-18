import os
from typing import Optional, TYPE_CHECKING

from geogeometry.geo_io.readers.CsvReader import CsvReader
from geogeometry.geo_io.readers.RhinoReader import RhinoReader
from geogeometry.geo_io.readers.StlReader import StlReader
from geogeometry.geo_io.readers.DxfReader import DxfReader

if TYPE_CHECKING:
    from geogeometry.geometry.model.GeometryModelsCollection import GeometryModelsCollection


class CadReader(object):

    @staticmethod
    def readFile(filepath: str, **kwargs) -> Optional['GeometryModelsCollection']:

        if not os.path.isfile(filepath):
            raise ValueError(f"File '{filepath}' not found.")

        extension = filepath.split('.')[-1].lower()

        if extension == 'dxf':
            return DxfReader.readFile(filepath)
        elif extension == '3dm':
            return RhinoReader.readFile(filepath)
        elif extension == 'stl':
            return StlReader.readFile(filepath)
        elif extension == 'csv':
            return CsvReader.readFile(filepath, **kwargs)
        else:
            raise ValueError(f"File extension '.{extension}' not supported.")
