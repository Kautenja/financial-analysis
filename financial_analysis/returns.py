"""A method to calculate returns.
Source: https://financeformulas.net/Total-Stock-Return.html

"""
import pandas as pd


def _set_freq(
    price: pd.Series,
    dividend: pd.Series = None,
    freq: any = None,
    groupby: bool = True,
    method: any = 'mean'
) -> pd.Series:
    """
    Set the frequency for the given price / dividend.

    Args:
        price: the price time-series to set the frequency for
        dividend: any dividend paid to set the frequency for
        freq: the frequency of periods for calculating returns
        groupby: whether to use groupby or asfreq
        method: the method to use for aggregating the time frequency group by

    Returns:
        a tuple of:
        - the price after setting the frequency
        - the dividend after setting the frequency
    """
    if freq is not None:  # adjust the frequency of the data
        if groupby:  # use a groupby to set the frequency
            price = price.groupby(pd.Grouper(freq=freq)).agg(method)
        else:  # just use asfreq (i.e., take the last value in the period)
            price = price.asfreq(freq)
        if dividend is not None:  # adjust the frequency of the dividend
            if groupby:  # use a groupby to set the frequency
                dividend = dividend.groupby(pd.Grouper(freq=freq)).agg(method)
            else:  # just use asfreq (i.e., take the last value in the period)
                dividend = dividend.asfreq(freq)
    return price, dividend


def cash_return(
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

        r = (P1 - P0) + D

        where:
        - P0 is the initial price
        - P1 is the ending price for the period
        - D are any dividend paid
    """
    # set the frequency of the price and dividend data
    price, dividend = _set_freq(price, dividend, freq, groupby, method)
    if dividend is None:  # don't use dividend in the calculation
        returns = price - price.shift(1)
    else:  # use dividend in the calculation
        returns = price - price.shift(1) + dividend
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
    price, dividend = _set_freq(price, dividend, freq, groupby, method)
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
