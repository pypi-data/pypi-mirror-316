import copy
from typing import TYPE_CHECKING, Tuple

import numpy as np

from geogeometry.geometry.operations.Angles import Angles
from geogeometry.geometry.shared.shared_components.ExplicitGeometryMetrics import ExplicitGeometryMetrics

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


class VectorMetrics(ExplicitGeometryMetrics):

    def __init__(self, vector: 'Vector'):
        super().__init__(element=vector)
        self.vector: 'Vector' = vector

    def calculateMetrics(self) -> None:
        super().calculateMetrics()

        self.calculateLength()
        self.calculateNormalizedVector()
        self.calculateDipDipdir()

        self.vector.setIsPositionVector(is_position_vector=(np.sum(self.vector.getOrigin()) == 0.))

    def calculateLength(self) -> None:
        diff = self.vector.getTip() - self.vector.getOrigin()
        length = np.linalg.norm(diff)
        self.vector.setLength(length=length)

        self.vector.setIsUnitary(is_unitary=(length == 1.))

    def calculateNormalizedVector(self) -> None:

        if self.vector.isUnitary():
            self.vector.setNormalizedVector(normalized_vector=self.vector.copy())
            return

        pos = self.vector.getTip() - self.vector.getOrigin()
        norm = np.linalg.norm(pos)
        if norm == 0.:
            raise ValueError("Origin as vector.")

        self.vector.createNormalizedVector(n=pos/norm)

    def calculateDipDipdir(self) -> None:

        if self.vector.getNormalizedVector() is None:
            self.calculateNormalizedVector()

        norm_vector = self.vector.getNormalizedVector()

        dipdir = None
        if norm_vector.getOrigin().shape[0] == 2:
            dip = 90.
        else:
            if abs(norm_vector.getTip()[2]) == 1.:
                dip, dipdir = 0, 0
            else:
                dip = Angles.calculateAngleBetweenVectorAndAxis(v=norm_vector, axis_id='z')
                if dip > 90.:
                    reversed_normal = norm_vector.copy()
                    reversed_normal.reverse()
                    dip = Angles.calculateAngleBetweenVectorAndAxis(v=reversed_normal, axis_id='z')

        if dipdir is None:
            dipdir = Angles.calculateAngleFromThreePoints([0., 1.], [0., 0.], norm_vector.getTip()[:2])

        if norm_vector.getTip()[0] < 0.:
            dipdir = 360. - dipdir

        self.vector.setDip(dip=round(dip, 2))
        self.vector.setDipdir(dipdir=round(dipdir, 2))
