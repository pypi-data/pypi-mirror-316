"""
Functions for performing statistical analysis.
"""
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency, pearsonr, spearmanr
from collections import Counter

def calculate_mean(data):
    """
    Calculate the mean of a dataset.

    Args:
        data: Array-like dataset.
    """
    return np.mean(data)

def calculate_median(data):
    """
    Calculate the median of a dataset.

    Args:
        data: Array-like dataset.
    """
    return np.median(data)

def calculate_mode(data):
    """
    Calculate the mode of a dataset.

    Args:
        data: Array-like dataset.
    """
    # Convert pandas Series to list if necessary
    if hasattr(data, 'mode'):
        # Use pandas mode() function for Series
        mode_result = data.mode()
        return mode_result.iloc[0] if not mode_result.empty else None
    else:
        # For regular lists/arrays
        counter = Counter(data)
        max_count = max(counter.values())
        modes = [k for k, v in counter.items() if v == max_count]
        return modes[0]  # Return first mode if multiple exist

def perform_t_test(data1, data2, alternative="two-sided"):
    """
    Perform a t-test.

    Args:
        data1: First dataset.
        data2: Second dataset.
        alternative: Type of test ("two-sided", "greater", "less").
    """
    return ttest_ind(data1, data2, alternative=alternative)

def perform_chi_square_test(table):
    """
    Perform a chi-square test.

    Args:
        table: Contingency table for the test.
    """
    return chi2_contingency(table)

def calculate_pearson_correlation(x, y):
    """
    Calculate the Pearson correlation coefficient.

    Args:
        x: First dataset.
        y: Second dataset.
    """
    return pearsonr(x, y)

def calculate_spearman_correlation(x, y):
    """
    Calculate the Spearman rank correlation coefficient.

    Args:
        x: First dataset.
        y: Second dataset.
    """
    return spearmanr(x, y)