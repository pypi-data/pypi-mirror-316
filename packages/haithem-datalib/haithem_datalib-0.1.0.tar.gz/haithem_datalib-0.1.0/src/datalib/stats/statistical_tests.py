import numpy as np
from scipy import stats

def t_test(sample1: list, sample2: list):
    """
    Performs a t-test to compare the means of two samples.

    Parameters:
    - sample1 (list): The first sample data.
    - sample2 (list): The second sample data.

    Returns:
    - tuple: A tuple containing the t-statistic and the p-value.
    """
    stat, p_value = stats.ttest_ind(sample1, sample2)
    return stat, p_value

def chi_square_test(contingency_table: list):
    """
    Performs a chi-square test for independence.

    Parameters:
    - contingency_table (list): A list of lists representing the contingency table.

    Returns:
    - tuple: A tuple containing the chi-square statistic, p-value, degrees of freedom, and expected frequencies.
    """
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    return chi2, p, dof, expected
