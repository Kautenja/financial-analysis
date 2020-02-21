"""Test cases for the returns module."""
from unittest import TestCase
import pandas as pd
from ..returns import cash_return, percent_return


class ShouldCalculateReturns(TestCase):
    def test(self):
        index = pd.to_datetime([1, 2], unit='ns')
        price = pd.Series([1000, 1020], index=index)
        dividend = pd.Series([0, 20], index=index)
        # cash returns
        returns = cash_return(price, dividend=dividend)
        self.assertEqual(40.0, returns.values[0])
        # percent returns
        returns = percent_return(price, dividend=dividend)
        self.assertAlmostEqual(0.04, returns.values[0])


class ShouldCalculateLogReturns(TestCase):
    def test(self):
        index = pd.to_datetime([1, 2], unit='ns')
        price = pd.Series([3.570, 3.575], index=index)
        # cash returns
        returns = cash_return(price, log_return=True)
        # should be 0.0014, but log in python sucks apparently
        self.assertAlmostEqual(0.00139, returns.values[0], places=4)


class ShouldCalculateReturnsFromSelf(TestCase):
    def test(self):
        index = pd.to_datetime([1, 2], unit='ns')
        price = pd.Series([1000, 1020], index=index)
        dividend = pd.Series([0, 20], index=index)
        # cash returns
        self.assertTrue(hasattr(price, 'cash_return'))
        returns = price.cash_return(dividend=dividend)
        self.assertEqual(40.0, returns.values[0])
        # percent returns
        self.assertTrue(hasattr(price, 'percent_return'))
        returns = price.percent_return(dividend=dividend)
        self.assertAlmostEqual(0.04, returns.values[0])
