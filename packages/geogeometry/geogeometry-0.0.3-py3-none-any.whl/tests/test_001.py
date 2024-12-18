import unittest
from geogeometry import Triangulation, Vector, Rotations


class TestBaseGeometry(unittest.TestCase):

    def setUp(self):
        pass

    def test_triangulation_creation(self):
        t = Triangulation()
        self.assertIsNotNone(t)
        self.assertIsInstance(t, Triangulation)

    def test_vectors_rotations(self):
        v1 = Vector(tip=[0., 0., 1.])
        v2 = Vector(tip=[0, 1, 0])

        R = Rotations.calculateRotationMatrixFromVectors(v0=v1, v1=v2)

        v1.rotateByRotationMatrix(R)

        self.assertEqual(v1, v2)


if __name__ == "__main__":
    unittest.main()
