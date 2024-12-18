import os
import unittest
from geogeometry import CadReader


class TestReadCsvPoints(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.resource_dir = os.path.join(self.base_dir, 'resources', 'csv_files')

        self.extension = "csv"

        self.file_001_path = os.path.join(self.resource_dir, "file_001." + self.extension)

    def test_file_001(self):
        models_collection = CadReader.readFile(self.file_001_path,
                                               xlabel="LocX [m]", ylabel="LocY [m]", zlabel="LocZ [m]")
        self.assertEqual(len(models_collection), 1)

        n_points = len(models_collection[0].getPoints())
        self.assertEqual(n_points, 4336)


if __name__ == "__main__":
    unittest.main()
