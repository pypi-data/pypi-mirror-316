from typing import Optional, Union, List, Callable

import numpy as np
import trimesh


class TriangulationProperties(object):

    def __init__(self):

        self.nodes: Optional[np.ndarray] = None
        self.faces: Optional[np.ndarray] = None
        self.markers: Optional[np.ndarray] = None

        self.trimesh_t: Optional[trimesh.base.Trimesh] = None

    def _checkPossibleTrimesh(self):
        if self.getNodes() is not None and self.getFaces() is not None:
            self.trimesh_t = trimesh.Trimesh(vertices=self.getNodes(), faces=self.getFaces(), process=True)
            self.nodes = None
            self.faces = None

    def setNodes(self, nodes: Union[List, np.ndarray]) -> None:
        if self.trimesh_t is not None:
            raise ValueError("Triangulation already set.")

        if isinstance(nodes, list):
            nodes = np.array(nodes)
        self.nodes = nodes

        self._checkPossibleTrimesh()

    def setFaces(self, faces: Union[List[int], np.ndarray[int]]) -> None:
        if self.trimesh_t is not None:
            raise ValueError("Triangulation already set.")

        if isinstance(faces, list):
            faces = np.array(faces).astype(int)
        self.faces = faces

        self._checkPossibleTrimesh()

    def setMarkers(self, markers: Union[List[int], np.ndarray[int]]) -> None:
        if isinstance(markers, list):
            markers = np.array(markers).astype(int)
        self.markers = markers

    def setTrimesh(self, trimesh_t: trimesh.base.Trimesh) -> None:
        self.trimesh_t = trimesh_t

    def getNodes(self) -> Optional[np.ndarray]:
        if self.trimesh_t is not None:
            return np.asarray(self.trimesh_t.vertices)
        else:
            return self.nodes

    def getFaces(self) -> Optional[np.ndarray]:
        if self.trimesh_t is not None:
            return np.asarray(self.trimesh_t.faces)
        else:
            return self.faces

    def getMarkers(self) -> Optional[np.ndarray]:
        return self.markers

    def getTrimesh(self) -> Optional[trimesh.base.Trimesh]:
        return self.trimesh_t
