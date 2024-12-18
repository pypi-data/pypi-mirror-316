from typing import Optional, TYPE_CHECKING, Union, List

import numpy as np

from geogeometry.geometry.points.PointsCollection import PointsCollection
from geogeometry.geometry.polyline.PolylinesCollection import PolylinesCollection
from geogeometry.geometry.triangulation.TriangulationsCollection import TriangulationsCollection

if TYPE_CHECKING:
    from geogeometry.geometry.polyline.Polyline import Polyline
    from geogeometry.geometry.triangulation.Triangulation import Triangulation


class GeometryModelProperties(object):

    def __init__(self):
        super().__init__()
        self.triangulations: TriangulationsCollection = TriangulationsCollection()
        self.polylines: PolylinesCollection = PolylinesCollection()
        self.points: PointsCollection = PointsCollection()

    def getTriangulations(self) -> Optional[TriangulationsCollection]:
        return self.triangulations

    def getPolylines(self) -> Optional[PolylinesCollection]:
        return self.polylines

    def getPoints(self) -> Optional[PointsCollection]:
        return self.points

    def addTriangulation(self, triangulation: 'Triangulation') -> None:
        self.triangulations.addElement(triangulation)

    def addPolyline(self, polyline: 'Polyline') -> None:
        self.polylines.addElement(polyline)

    def addPoints(self, points: Union[List, np.ndarray]) -> None:
        self.points.setPoints(points)
