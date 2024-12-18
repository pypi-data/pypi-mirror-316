import math
from typing import Union, List, TYPE_CHECKING

import numpy as np

from geogeometry.geometry.operations.Angles import Angles

if TYPE_CHECKING:
    from geogeometry.geometry.vector.Vector import Vector


class Rotations(object):

    @staticmethod
    def calculate2dRotationMatrix(angle: float) -> np.ndarray:
        """
        Return anti-clockwise 2d rotation matrix.
        :param angle: (float) radians
        :return: 2D rotation matrix
        """
        rot_m = [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ]

        return np.array(rot_m)

    @staticmethod
    def calculateXRotationMatrix(angle: float) -> np.ndarray:
        """
        Returns anti-clockwise x-axis rotation matrix for 'angle'.
        :param angle: radians.
        :return: Rotation Matrix.
        """
        rot_x = [
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]
        ]
        return np.array(rot_x)

    @staticmethod
    def calculateYRotationMatrix(angle):
        """
        Returns anti-clockwise y-axis rotation matrix for 'angle'.
        :param angle: radians.
        :return: Rotation Matrix.
        """
        rot_y = [
            [math.cos(angle), 0, -math.sin(angle)],
            [0, 1, 0],
            [math.sin(angle), 0, math.cos(angle)]
        ]
        return np.array(rot_y)

    @staticmethod
    def calculateZRotationMatrix(angle: float) -> np.ndarray:
        """
        Returns anti-clockwise z-axis rotation matrix for 'angle'.
        :param angle: radians.
        :return: Rotation Matrix.
        """
        rot_z = [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ]
        return np.array(rot_z)

    @staticmethod
    def rotate2dPositionVector(vector: 'Vector', angle: float) -> np.ndarray:
        """
        Rotates position 'vector' (origin=(0,0,0)) anti-clockwise by 'angle'.
        vector: (x, y)
        angle: float (radians)
        """
        if (vector.getDimensions() == 3) or (not vector.isPositionVector()):
            raise ValueError("Vector must be 2D and positional.")

        rot_matrix = Rotations.calculate2dRotationMatrix(angle=angle)

        return rot_matrix.dot(vector.getTip())

    @staticmethod
    def rotatePointsByRotationMatrix(points: Union[List, np.ndarray], rotation_matrix: np.ndarray) -> np.ndarray:
        """
        Rotates 'points' by previously defined 'rotation_matrix'.
        :param points:
        :param rotation_matrix:
        :return:
        """
        if isinstance(points, list):
            points = np.array(points)
        return rotation_matrix.dot(points.T).T

    @staticmethod
    def calculateRotationMatrixFromVectors(v0: 'Vector', v1: 'Vector') -> np.ndarray:

        if v0.getNormalizedVector() == v1.getNormalizedVector():
            return np.identity(3)

        angle = v0.calculateAngleWithVector(other_vector=v1)
        if abs(angle) == 180.:
            return -np.identity(3)

        pos0, pos1 = v0.getNormalizedVector().getTip(), v1.getNormalizedVector().getTip()

        # Rotation axis
        v = np.cross(pos0, pos1)
        v /= np.linalg.norm(v)

        s = np.linalg.norm(v)
        c = np.dot(pos0, pos1)
        I = np.eye(3)

        vx = np.array([[0, -v[2], v[1]],
                       [v[2], 0, -v[0]],
                       [-v[1], v[0], 0]])

        v2 = np.matmul(vx, vx)

        R = I + vx + v2 * ((1. - c) / (s ** 2))

        if np.linalg.det(R) < 0:
            R[:, 0] = -R[:, 0]  # Flip one column to ensure a valid right-handed system

        return np.array(R)
