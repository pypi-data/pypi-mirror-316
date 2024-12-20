import pytest
import pandas as pd
import matplotlib.pyplot as plt
from src.datalib.visualization.advanced_plots import correlation_matrix


def test_correlation_matrix_valid_data():
    """Test correlation matrix with valid numeric data."""
    data = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    
    # Test that the function runs without errors
    correlation_matrix(data)
    plt.close()  # Close the plot to avoid affecting other tests

def test_correlation_matrix_single_column():
    """Test correlation matrix with a DataFrame with a single column."""
    data = pd.DataFrame({"x": [1, 2, 3]})
    
    # The correlation matrix should still be computed (it will just be a 1x1 matrix)
    correlation_matrix(data)
    plt.close()

def test_correlation_matrix_non_numeric_data():
    """Test correlation matrix with non-numeric data."""
    data = pd.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
    
    # Expecting to see only the numeric correlation (will ignore non-numeric columns)
    correlation_matrix(data)
    plt.close()

def test_correlation_matrix_missing_values():
    """Test correlation matrix with missing values in the DataFrame."""
    data = pd.DataFrame({"x": [1, 2, None], "y": [2, 4, 6]})
    
    # Check if missing values are handled correctly
    correlation_matrix(data)
    plt.close()

def test_correlation_matrix_empty_dataframe():
    """Test correlation matrix with an empty DataFrame."""
    data = pd.DataFrame()
    
    # The function should raise an error or handle it gracefully
    with pytest.raises(ValueError):
        correlation_matrix(data)
    plt.close()

