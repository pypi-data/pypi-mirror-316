import pandas as pd
from src.datalib.stats.descriptive_stats import calculate_mean, calculate_median, calculate_mode, calculate_std_dev, calculate_correlation

def test_calculate_mean():
    data = pd.DataFrame({"values": [1, 2, 3]})
    assert calculate_mean(data, "values") == 2, "calculate_mean ne fonctionne pas."

def test_calculate_median():
    data = pd.DataFrame({"values": [1, 2, 3]})
    assert calculate_median(data, "values") == 2, "calculate_median ne fonctionne pas."

def test_calculate_mode():
    data = pd.DataFrame({"values": [1, 1, 2]})
    assert calculate_mode(data, "values") == 1, "calculate_mode ne fonctionne pas."

def test_calculate_std_dev():
    data = pd.DataFrame({"values": [1, 2, 3]})
    assert round(calculate_std_dev(data, "values"), 2) == 1.0, "calculate_std_dev ne fonctionne pas."

def test_calculate_correlation():
    data = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    assert calculate_correlation(data, "x", "y") == 1.0, "calculate_correlation ne fonctionne pas."
