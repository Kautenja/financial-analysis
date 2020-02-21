"""Utility functions for modules in the package."""
import pandas as pd


def set_freq(
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


# explicitly define the outward facing API of this module
__all__ = [set_freq.__name__]
