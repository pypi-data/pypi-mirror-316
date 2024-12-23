"""
Functions for regression and data analysis.
"""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import numpy as np

def linear_regression(X, y, return_metrics=False):
    """
    Perform linear regression.

    Args:
        X: Feature matrix.
        y: Target vector.
        return_metrics: If True, return model metrics (default: False).
    """
    model = LinearRegression()
    model.fit(X, y)
    metrics = None
    if return_metrics:
        predictions = model.predict(X)
        mse = mean_squared_error(y, predictions)
        metrics = {"R-squared": model.score(X, y), "MSE": mse}
    return model, metrics

def polynomial_regression(X, y, degree, return_metrics=False):
    """
    Perform polynomial regression.

    Args:
        X: Feature matrix.
        y: Target vector.
        degree: Polynomial degree.
        return_metrics: If True, return model metrics (default: False).
    """
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)
    metrics = None
    if return_metrics:
        predictions = model.predict(X_poly)
        mse = mean_squared_error(y, predictions)
        metrics = {"R-squared": model.score(X_poly, y), "MSE": mse}
    return model, metrics

def multiple_linear_regression(X, y, return_metrics=False):
    """
    Perform multiple linear regression.

    Args:
        X: Feature matrix.
        y: Target vector.
        return_metrics: If True, return model metrics (default: False).
    """
    model = LinearRegression()
    model.fit(X, y)
    metrics = None
    if return_metrics:
        predictions = model.predict(X)
        mse = mean_squared_error(y, predictions)
        metrics = {"R-squared": model.score(X, y), "MSE": mse}
    return model, metrics