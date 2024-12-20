import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def linear_regression(x: np.ndarray, y: np.ndarray) -> LinearRegression:
    """
    Performs linear regression on the input data.

    Parameters:
    - x (np.ndarray): The independent variable data.
    - y (np.ndarray): The dependent variable data.

    Returns:
    - LinearRegression: The fitted linear regression model.
    """
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    return model

def polynomial_regression(x: np.ndarray, y: np.ndarray, degree: int) -> LinearRegression:
    """
    Performs polynomial regression on the input data.

    Parameters:
    - x (np.ndarray): The independent variable data.
    - y (np.ndarray): The dependent variable data.
    - degree (int): The degree of the polynomial regression.

    Returns:
    - LinearRegression: The fitted polynomial regression model.
    """
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))
    model = LinearRegression()
    model.fit(x_poly, y)
    return model
