import unittest

from geney import oncosplice


class TestOncosplice(unittest.TestCase):

    def test_is_monotonic_increasing(self):
        self.assertTrue(oncosplice.is_monotonic([1, 2, 3, 4, 5]))

    def test_is_monotonic_decreasing(self):
        self.assertTrue(oncosplice.is_monotonic([5, 4, 3, 2, 1]))

    def test_is_monotonic_not(self):
        self.assertFalse(oncosplice.is_monotonic([1, 3, 2, 4, 5]))

    def test_is_monotonic_same_elements(self):
        self.assertTrue(oncosplice.is_monotonic([2, 2, 2, 2, 2]))

    def test_is_monotonic_single_element(self):
        self.assertTrue(oncosplice.is_monotonic([1]))


if __name__ == '__main__':
    unittest.main()
