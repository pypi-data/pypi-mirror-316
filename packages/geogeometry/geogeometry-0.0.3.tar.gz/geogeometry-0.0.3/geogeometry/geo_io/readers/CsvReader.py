import csv
from typing import Optional

from geogeometry.geometry.model.GeometryModel import GeometryModel
from geogeometry.geometry.model.GeometryModelsCollection import GeometryModelsCollection


class CsvReader(object):

    @staticmethod
    def readFile(filepath: str, xlabel: str, ylabel: str, zlabel: str) -> Optional[GeometryModelsCollection]:

        pts_name = filepath.split(".")[0]

        points = []

        with open(filepath, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)

            xindex, yindex, zindex = header.index(xlabel), header.index(ylabel), header.index(zlabel)

            for row in reader:
                pt = [row[xindex], row[yindex], row[zindex]]
                points += [[float(c) for c in pt]]

        model = GeometryModel(name=pts_name)
        model.addPoints(points=points)

        models_collection = GeometryModelsCollection()
        models_collection.addElement(model)

        return models_collection
