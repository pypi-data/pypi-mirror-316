from typing import Union, List

import numpy as np

from geogeometry.geometry.operations.Rotations import Rotations


class ExplicitGeometryTransformer(object):

    def __init__(self, element):
        self.element = element

    def translate(self, translation_vector: Union[List, np.ndarray]) -> None:
        self.element.setNodes(nodes=self.element.getNodes() + translation_vector)

    def rotateByRotationMatrix(self, rotation_matrix: np.ndarray) -> None:
        rotated_nodes = Rotations.rotatePointsByRotationMatrix(points=self.element.getNodes(), rotation_matrix=rotation_matrix)
        self.element.setNodes(nodes=rotated_nodes)
