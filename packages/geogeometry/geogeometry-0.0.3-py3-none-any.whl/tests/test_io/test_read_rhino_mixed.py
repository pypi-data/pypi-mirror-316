import os
import unittest
from geogeometry import CadReader


class TestReadRhinoMixed(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.resource_dir = os.path.join(self.base_dir, 'resources', 'rhino_files')

        self.extension = "3dm"

        self.file_006_path = os.path.join(self.resource_dir, "file_006." + self.extension)

    def test_file_006(self):
        models_collection = CadReader.readFile(self.file_006_path)
        self.assertEqual(len(models_collection), 2)

        n_triangulations = len(models_collection.getAllTriangulations())
        self.assertEqual(n_triangulations, 2)

        n_polylines = len(models_collection.getAllPolylines())
        self.assertEqual(n_polylines, 3)
