import pandas as pd
import pytest
from src.datalib.stats.descriptive_stats import calculate_mean, calculate_median, calculate_mode, calculate_std_dev, calculate_correlation

def test_calculate_mean():
    """Test calculate_mean function."""
    data = pd.DataFrame({"values": [1, 2, 3]})
    assert calculate_mean(data, "values") == 2, "calculate_mean ne fonctionne pas."

def test_calculate_mean_empty():
    df = pd.DataFrame(columns=["A"])
    result = calculate_mean(df, "A")
    assert result == 0

def test_calculate_median():
    """Test calculate_median function."""
    data = pd.DataFrame({"values": [1, 2, 3]})
    assert calculate_median(data, "values") == 2, "calculate_median ne fonctionne pas."

def test_calculate_median_single_value():
    """Test calculate_median with a single value."""
    data = pd.DataFrame({"values": [3]})
    assert calculate_median(data, "values") == 3, "calculate_median ne fonctionne pas avec une seule valeur."

def test_calculate_mode():
    """Test calculate_mode function."""
    data = pd.DataFrame({"values": [1, 1, 2]})
    assert calculate_mode(data, "values") == 1, "calculate_mode ne fonctionne pas."

def test_calculate_mode_multiple_modes():
    """Test calculate_mode with multiple modes."""
    data = pd.DataFrame({"values": [1, 1, 2, 2]})
    assert calculate_mode(data, "values") == 1, "calculate_mode ne fonctionne pas avec plusieurs modes."

def test_calculate_std_dev():
    """Test calculate_std_dev function."""
    data = pd.DataFrame({"values": [1, 2, 3]})
    assert round(calculate_std_dev(data, "values"), 2) == 1.0, "calculate_std_dev ne fonctionne pas."

def test_calculate_std_dev_single_value():
    df = pd.DataFrame({"A": [5]})
    result = calculate_std_dev(df, "A")
    assert result == 0

def test_calculate_correlation():
    """Test calculate_correlation function."""
    data = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    assert calculate_correlation(data, "x", "y") == 1.0, "calculate_correlation ne fonctionne pas."

def test_calculate_correlation_negative():
    """Test calculate_correlation with negative correlation."""
    data = pd.DataFrame({"x": [1, 2, 3], "y": [6, 4, 2]})
    assert calculate_correlation(data, "x", "y") == -1.0, "calculate_correlation ne fonctionne pas avec une corrélation négative."

def test_calculate_correlation_empty():
    df = pd.DataFrame(columns=["A", "B"])
    result = calculate_correlation(df, "A", "B")
    assert result is None