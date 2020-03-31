# -*- coding: utf-8 -*-
import unittest
from src.minimize_transactions import minimize_transactions


class TestOptimalBalance(unittest.TestCase):

    def _helper(self, pay, get, optimal, decimal_places):
        res = minimize_transactions(pay, get, decimal_places)
        t_pay = sum(pay)
        t_get = sum(get)
        self.assertAlmostEqual(t_pay, t_get)
        self.assertEqual(len(res), optimal)
        self.assertAlmostEqual(t_pay, sum(r[2] for r in res))

    def _test_both_ways(self, pay, get, optimal, decimal_places=2):
        self._helper(pay, get, optimal, decimal_places)
        self._helper(get, pay, optimal, decimal_places)

    def test_optimality(self):
        self._test_both_ways([11, 2.5], [9.5, 4], 3)
        self._test_both_ways([11, 9.5], [9.5, 7, 4], 3)
        self._test_both_ways([20, 16, 7], [15, 10, 8, 5, 5], 6)
        self._test_both_ways([20, 16, 7], [15, 10, 8, 4, 3, 3], 7)

    def test_optimality_decimal(self):
        self._test_both_ways([11, 2.5], [9.5, 4], 3, 1)
        self._test_both_ways([11, 2.5], [9.5, 4], 3, 2)
        self._test_both_ways([11, 2.505], [9.505, 4], 3, 3)

        self._test_both_ways([11, 9.5], [9.5, 7, 4], 3, 1)
        self._test_both_ways([11, 9.5], [9.5, 7, 4], 3, 2)
        self._test_both_ways([11, 9.5], [9.5, 7, 4], 3, 3)
        self._test_both_ways([11.1234, 9.5], [9.5, 7.1234, 4], 3, 4)

        self._test_both_ways([20.00034, 16, 7], [15, 10.00034, 8, 4, 3, 3], 7, 5)
