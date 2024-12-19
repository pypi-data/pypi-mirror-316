import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def linear_regression(x, y):
    """Effectuer une régression linéaire."""
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    return model

def polynomial_regression(x, y, degree=2):
    """Effectuer une régression polynomiale."""
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))
    model = LinearRegression()
    model.fit(x_poly, y)
    return model
