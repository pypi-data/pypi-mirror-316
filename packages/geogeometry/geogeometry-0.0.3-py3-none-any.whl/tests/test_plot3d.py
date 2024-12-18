import os
import tempfile
import unittest
from geogeometry import CadReader


class TestPlot3d(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.resource_dir = os.path.join(self.base_dir, 'test_io', 'resources', 'dxf_files')

        self.file_001_path = os.path.join(self.resource_dir, "file_001.dxf")  # Triangulations
        self.file_004_path = os.path.join(self.resource_dir, "file_004.dxf")  # Polylines
        self.file_006_path = os.path.join(self.resource_dir, "file_006.dxf")  # Mixed

    def test_file_001(self):
        models_collection = CadReader.readFile(self.file_001_path)

        t = models_collection[0].getTriangulations()[0]

        tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        t.plot3d(screenshot=True, filepath=tmpfile.name)

        self.assertTrue(os.path.exists(tmpfile.name))

        tmpfile.close()
        if os.path.exists(tmpfile.name):
            os.remove(tmpfile.name)

    def test_file_004(self):
        models_collection = CadReader.readFile(self.file_004_path)

        drillholes = models_collection.getAllPolylines()

        tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        drillholes.plot3d(screenshot=True, filepath=tmpfile.name)

        self.assertTrue(os.path.exists(tmpfile.name))

        tmpfile.close()
        if os.path.exists(tmpfile.name):
            os.remove(tmpfile.name)

    def test_file_006(self):
        models_collection = CadReader.readFile(self.file_006_path)

        tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        models_collection.plot3d(screenshot=True, filepath=tmpfile.name)

        self.assertTrue(os.path.exists(tmpfile.name))

        tmpfile.close()
        if os.path.exists(tmpfile.name):
            os.remove(tmpfile.name)


if __name__ == "__main__":
    unittest.main()