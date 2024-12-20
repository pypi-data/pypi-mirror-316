import numpy as np
from src.datalib.analysis.regression import linear_regression, polynomial_regression
import pytest

def test_linear_regression():
    x = np.array([1, 2, 3])
    y = np.array([2, 3, 4])
    model = linear_regression(x, y)
    assert hasattr(model, "coef_")

def test_linear_regression_single_data_point():
    """Test linear regression with a single data point."""
    x = np.array([1])
    y = np.array([2])
    model = linear_regression(x, y)
    assert model.coef_[0] == pytest.approx(0, rel=1e-9), "linear_regression ne fonctionne pas avec un seul point."

def test_linear_regression_no_variation():
    """Test linear regression when y has no variation."""
    x = np.array([1, 2, 3])
    y = np.array([5, 5, 5])
    model = linear_regression(x, y)
    assert model.coef_[0] == 0, "linear_regression ne fonctionne pas avec des données constantes."


def test_polynomial_regression():
    x = np.array([1, 2, 3])
    y = np.array([2, 3, 4])
    model = polynomial_regression(x, y, degree=2)
    assert hasattr(model, "coef_")

def test_polynomial_regression_high_degree():
    """Test polynomial regression with a high degree."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 8, 27, 64, 125])
    model = polynomial_regression(x, y, degree=5)
    assert len(model.coef_) == 6, "polynomial_regression ne fonctionne pas avec un degré élevé."

def test_polynomial_regression_overfit():
    """Test polynomial regression overfitting with high degree on small data."""
    x = np.array([1, 2, 3])
    y = np.array([1, 4, 9])  # y = x^2
    model = polynomial_regression(x, y, degree=6)
    assert abs(model.coef_[0]) > 0, "polynomial_regression échoue à ajuster un modèle complexe correctement."

