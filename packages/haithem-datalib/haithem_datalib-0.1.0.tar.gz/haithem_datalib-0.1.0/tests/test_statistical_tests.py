from matplotlib import pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind
from src.datalib.stats.statistical_tests import t_test, chi_square_test
import pytest


def test_t_test():
    sample1 = [1, 2, 3]
    sample2 = [4, 5, 6]
    stat, p_value = t_test(sample1, sample2)
    assert round(stat, 2) == -3.67

def test_chi_square_test():
    contingency_table = [[10, 20], [30, 40]]
    chi2, p, _, _ = chi_square_test(contingency_table)
    assert round(chi2, 2) == 0.45

def test_t_test_no_variance():
    """Test t-test with no variance in one sample."""
    sample1 = [5, 5, 5]  # No variance
    sample2 = [1, 2, 3]  # Some variance
    stat, p_value = t_test(sample1, sample2)

    # With no variance in sample1, we expect a high t-statistic or a warning.
    # We should at least ensure the p-value is reasonable.
    assert p_value < 1, f"Expected a small p-value, but got {p_value}."
    assert abs(stat) > 0, f"Expected a non-zero t-statistic, but got {stat}."

def test_chi_square_test_single_category():
    """Test chi-square test with one category."""
    contingency_table = [[100, 100]]
    chi2, p, _, _ = chi_square_test(contingency_table)
    
    # With a single category, we expect a low chi-squared statistic
    assert chi2 == 0, f"Expected chi-squared statistic to be 0, but got {chi2}."
    assert p == 1.0, f"Expected p-value to be 1.0, but got {p}."
