import unittest
import numpy as np


class TestPhysics(unittest.TestCase):

    PRECISION = 5

    def test_utils(self):
        from datrack.physics import utils
        x = np.array((2., 3.))

        self.assertAlmostEqual(np.linalg.norm(
            utils.rotate_90(x) - utils.rotate_vector(x, -np.pi/2)),
                               0.,
                               self.PRECISION)

        # from matplotlib import pyplot
        #
        # pyplot.figure()
        # for a in np.linspace(0, np.pi * 2, 12, endpoint=False):
        #     y = utils.rotate_vector(x, a)
        #     z = np.vstack(((0,0), y))
        #     pyplot.plot(*z.T, 'o-')
        #
        # pyplot.gca().axis('equal')
        # pyplot.show()

if __name__ == '__main__':
    unittest.main()
