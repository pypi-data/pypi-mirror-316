from typing import TYPE_CHECKING, Optional

from geogeometry.geometry.operations.Angles import Angles

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


class VectorQuerier(object):

    def __init__(self, vector: 'Vector'):
        self.vector = vector

    def calculateAngleWithVector(self, other_vector: 'Vector') -> float:
        return Angles.calculateAngleBetweenPositionVectors(v1=self.vector.getNormalizedVector(),
                                                           v2=other_vector.getNormalizedVector())
