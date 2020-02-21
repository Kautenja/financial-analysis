"""A method for calculating the volatility of a time-series in pandas"""
import pandas as pd


def volatility(arr: pd.Series, window=None):
    """
    Calculate the volatility of a pandas time-series.

    Args:
        arr: the array to calculate the volatility of
        window: the window size for calculating the volatility

    Returns:
        the volatility of the input array

    """
    if window is None:  # no window, return total volatility
        return arr.std()
    return arr.rolling(window).std(ddof=0)


# create a `volatility` method for pandas series objects
setattr(pd.Series, 'volatility', volatility)


# explicitly define the outward facing API of this module
__all__ = [volatility.__name__]
