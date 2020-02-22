"""Test cases for the set_freq module."""
from unittest import TestCase
import numpy as np
import pandas as pd
from ..set_freq import set_freq

#
# MARK: lossless conversions
#

class ShouldLosslessConvertUsingGroupby(TestCase):
    def test(self):
        index = pd.to_datetime([1000, 2000, 3000], unit='ms')
        price = pd.Series([100., 101., 102.], index=index)
        dividend = pd.Series([5., 6., 7.], index=index)
        price, dividend = set_freq(price, dividend, '1s', groupby=True)
        # create the expected index and price
        expected_index = pd.to_datetime([1, 2, 3], unit='s')
        # expected values will have NaN where there were none
        expected_price = pd.Series([100., 101., 102.], index=expected_index)
        expected_dividend = pd.Series([5., 6., 7.], index=expected_index)
        # make assertions through the pandas testing module
        pd.testing.assert_series_equal(price, expected_price)
        pd.testing.assert_series_equal(dividend, expected_dividend)


class ShouldLosslessConvertUsingAsfreq(TestCase):
    def test(self):
        index = pd.to_datetime([1000, 2000, 3000], unit='ms')
        price = pd.Series([100., 101., 102.], index=index)
        dividend = pd.Series([5., 6., 7.], index=index)
        price, dividend = set_freq(price, dividend, '1s', groupby=False, method=None)
        # create the expected index and price
        expected_index = pd.to_datetime([1, 2, 3], unit='s')
        # expected values will have NaN where there were none
        expected_price = pd.Series([100., 101., 102.], index=expected_index)
        expected_dividend = pd.Series([5., 6., 7.], index=expected_index)
        # make assertions through the pandas testing module
        pd.testing.assert_series_equal(price, expected_price)
        pd.testing.assert_series_equal(dividend, expected_dividend)


#
# MARK: Up-sampling (inserting missing values)
#


class ShouldUpsampleTimeScaleUsingFfillTrue(TestCase):
    def test(self):
        index = pd.to_datetime([1, 2], unit='ms')
        price = pd.Series([100., 101.], index=index)
        dividend = pd.Series([5., 6.], index=index)
        price, dividend = set_freq(price, dividend, '100U')
        # create the expected index and price
        expected_index = pd.to_datetime(list(range(1000, 2001, 100)), unit='us')
        # expected values will be forward filled to meet timescale
        expected_price = pd.Series(10 * [100.] + [101.], index=expected_index)
        expected_dividend = pd.Series(10 * [5.] + [6.], index=expected_index)
        # make assertions through the pandas testing module
        pd.testing.assert_series_equal(price, expected_price)
        pd.testing.assert_series_equal(dividend, expected_dividend)


class ShouldNotUpsampleTimeScaleUsingFfillFalse(TestCase):
    def test(self):
        index = pd.to_datetime([1, 2], unit='ms')
        price = pd.Series([100., 101.], index=index)
        dividend = pd.Series([5., 6.], index=index)
        price, dividend = set_freq(price, dividend, '100U', ffill=False)
        # create the expected index and price
        expected_index = pd.to_datetime(list(range(1000, 2001, 100)), unit='us')
        # expected values will have NaN where there were none
        expected_price = pd.Series([100.] + 9 * [np.nan] + [101.], index=expected_index)
        expected_dividend = pd.Series([5.] + 9 * [np.nan] + [6.], index=expected_index)
        # make assertions through the pandas testing module
        pd.testing.assert_series_equal(price, expected_price)
        pd.testing.assert_series_equal(dividend, expected_dividend)

#
# MARK: Down-sampling (aggregating groups of data)
#

class ShouldDownsampleUsingGroupbyAndMeanValue(TestCase):
    def test(self):
        index = pd.to_datetime([1001, 1002], unit='ms')
        price = pd.Series([100., 101.], index=index)
        dividend = pd.Series([5., 6.], index=index)
        price, dividend = set_freq(price, dividend, freq='1s', method='mean')
        # create the expected index and price
        expected_index = pd.to_datetime([1], unit='s')
        # expected values will have NaN where there were none
        expected_price = pd.Series([100.5], index=expected_index)
        expected_dividend = pd.Series([5.5], index=expected_index)
        # make assertions through the pandas testing module
        pd.testing.assert_series_equal(price, expected_price)
        pd.testing.assert_series_equal(dividend, expected_dividend)


# class ShouldDownsampleUsingAsfreq(TestCase):
#     def test(self):
#         index = pd.to_datetime([1001, 1002], unit='ms')
#         price = pd.Series([100., 101.], index=index)
#         dividend = pd.Series([5., 6.], index=index)
#         price, dividend = set_freq(price, dividend, freq='1s', groupby=False, method='bfill')
#         # create the expected index and price
#         expected_index = pd.to_datetime([1], unit='s')
#         # expected values will have NaN where there were none
#         expected_price = pd.Series([100.], index=expected_index)
#         expected_dividend = pd.Series([5.], index=expected_index)
#         # make assertions through the pandas testing module
#         pd.testing.assert_series_equal(price, expected_price)
#         pd.testing.assert_series_equal(dividend, expected_dividend)
