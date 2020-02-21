"""Test cases for the volatility module."""
from unittest import TestCase
import pandas as pd
from .. import returns
from ..volatility import volatility


# price data for the test cases
PRICE = pd.Series([
    147.82,
    149.5,
    149.78,
    149.86,
    149.93,
    150.89,
    152.39,
    153.74,
    152.79,
    151.23,
    151.78
])


class ShouldCalculateVolatilityTotal(TestCase):
    def test(self):
        vol = PRICE.percent_return().std()
        self.assertAlmostEqual(0.006959, vol, 6)


class ShouldCalculateVolatility(TestCase):
    def test(self):
        vol = volatility(PRICE.percent_return())
        self.assertAlmostEqual(0.006959, vol, 6)
        # TODO rolling test
        vol = volatility(PRICE.percent_return(), 2)


class ShouldCalculateVolatilityFromSelf(TestCase):
    def test(self):
        self.assertTrue(hasattr(PRICE, 'volatility'))
        vol = PRICE.percent_return().volatility()
        self.assertAlmostEqual(0.006959, vol, 6)
        # TODO rolling test
        vol = PRICE.percent_return().volatility(2)
