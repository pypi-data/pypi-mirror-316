# def readStlFile(self, **kwargs):
from typing import Optional

import numpy as np
import trimesh

from geogeometry.geometry.model.GeometryModel import GeometryModel
from geogeometry.geometry.triangulation.Triangulation import Triangulation
from geogeometry.geometry.model.GeometryModelsCollection import GeometryModelsCollection


class StlReader(object):

    @staticmethod
    def readFile(filepath: str) -> Optional[GeometryModelsCollection]:

        mesh = trimesh.load(filepath)
        t_name = filepath.split(".")[0]

        t = Triangulation(name=t_name)
        t.setNodes(nodes=np.asarray(mesh.vertices))
        t.setFaces(faces=np.asarray(mesh.faces))

        model = GeometryModel(name=t_name)
        model.addTriangulation(t)

        models_collection = GeometryModelsCollection()
        models_collection.addElement(model)

        return models_collection
