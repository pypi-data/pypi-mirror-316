import unittest
from probability import *

class TestProbabilityAndCombinatorics(unittest.TestCase):

    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(3), 6)

    def test_permutations(self):
        self.assertEqual(permutations(5, 3), 60)
        self.assertEqual(permutations(5, 5), 120)
        self.assertEqual(permutations(3, 4), 0)

    def test_permutations_with_repetition(self):
        self.assertEqual(permutationsWithRepetion(3, 2), 9)
        self.assertEqual(permutationsWithRepetion(2, 3), 0)

    def test_combinations(self):
        self.assertEqual(combinations(5, 3), 10)
        self.assertEqual(combinations(5, 5), 1)
        self.assertEqual(combinations(3, 4), 0)

    def test_combinations_with_repetition(self):
        self.assertEqual(combinationsWithRepetion(3, 2), 6)
        self.assertEqual(combinationsWithRepetion(2, 3), 0)

    def test_bernoulli(self):
        # Пример: m = 2, n = 5, p = 0.5
        m = 2
        n = 5
        p = 0.5
        expected_value = combinations(n, m) * (p ** m) * ((1 - p) ** (n - m))
        self.assertAlmostEqual(Bernoulli(m, n, p), expected_value)

    def test_poisson(self):
        # Пример: n = 10, m = 2, p = 0.5
        n = 10
        m = 2
        p = 0.5
        expected_value = ((n * p) ** m) / factorial(m) * (2.71828 ** (-(n * p)))
        self.assertAlmostEqual(Poisson(n, m, p), expected_value)

if __name__ == '__main__':
    unittest.main()
