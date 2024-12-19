import numpy as np
from src.datalib.analysis.regression import linear_regression, polynomial_regression
import pytest

def test_linear_regression():
    x = np.array([1, 2, 3])
    y = np.array([2, 4, 6])
    model = linear_regression(x, y)
    assert model.coef_[0] == pytest.approx(2.0, rel=1e-9), "linear_regression ne fonctionne pas."

def test_polynomial_regression():
    x = np.array([1, 2, 3])
    y = np.array([1, 8, 27])
    model = polynomial_regression(x, y, degree=3)
    assert len(model.coef_) == 4, "polynomial_regression ne fonctionne pas."
