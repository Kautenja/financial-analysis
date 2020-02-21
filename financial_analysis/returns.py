"""A method to calculate returns.
Source: https://financeformulas.net/Total-Stock-Return.html

"""
import numpy as np
import pandas as pd
from . import _util


def cash_return(
    price: pd.Series,
    dividend: pd.Series = None,
    freq: any = None,
    groupby: bool = True,
    method: any = 'mean',
    log_return: bool = False
) -> pd.Series:
    """
    Calculate the stock returns of a pandas time-series.

    Args:
        price: the price time-series to calculate the returns of
        dividend: any dividend paid (none by default, i.e., 0)
        freq: the frequency of periods for calculating returns
        groupby: whether to use groupby or asfreq
        method: the method to use for aggregating the time frequency group by
        log_return: whether to use log return

    Returns:
        the returns of the series over the given period

    Notes:

        r = (P1 - P0) + D

        where:
        - P0 is the initial price
        - P1 is the ending price for the period
        - D are any dividend paid
    """
    # set the frequency of the price and dividend data
    price, dividend = _util.set_freq(price, dividend, freq, groupby, method)
    # shift the price vector 1 index value after setting the frequency
    price_last = price.shift(1)
    if log_return:  # apply the logarithmic function to the variables
        # use the subtractive method to allow NumPy to catch the divide by zero
        # error that occurs if price_last is zero. conveniently provides the
        # same functionality for when price is 0.
        return (np.log(price) - np.log(price_last))[1:]
    if dividend is None:  # don't use dividend in the calculation
        returns = price - price_last
    else:  # use dividend in the calculation
        returns = price - price_last + dividend
    # the first value becomes NaN because of the shift operation, skip it
    return returns[1:]


# create a `cash_return` method for pandas series objects
setattr(pd.Series, cash_return.__name__, cash_return)


def percent_return(
    price: pd.Series,
    dividend: pd.Series = None,
    freq: any = None,
    groupby: bool = True,
    method: any = 'mean'
) -> pd.Series:
    """
    Calculate the stock returns of a pandas time-series.

    Args:
        price: the price time-series to calculate the returns of
        dividend: any dividend paid (none by default, i.e., 0)
        freq: the frequency of periods for calculating returns
        groupby: whether to use groupby or asfreq
        method: the method to use for aggregating the time frequency group by

    Returns:
        the returns of the series over the given period

    Notes:

            (P1 - P0) + D
        r = —————————————
                  P0

        where:
        - P0 is the initial price
        - P1 is the ending price for the period
        - D are any dividend paid
    """
    # set the frequency of the price and dividend data
    price, dividend = _util.set_freq(price, dividend, freq, groupby, method)
    if dividend is None:  # don't use dividend in the calculation
        returns = (price / price.shift(1)) - 1
    else:  # use dividend in the calculation
        returns = ((price + dividend) / price.shift(1)) - 1
    # the first value becomes NaN because of the shift operation, skip it
    return returns[1:]


# create a `percent_return` method for pandas series objects
setattr(pd.Series, percent_return.__name__, percent_return)


# explicitly define the outward facing API of this module
__all__ = [
    cash_return.__name__,
    percent_return.__name__
]
