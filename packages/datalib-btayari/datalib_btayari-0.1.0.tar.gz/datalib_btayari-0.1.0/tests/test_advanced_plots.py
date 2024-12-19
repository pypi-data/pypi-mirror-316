import pandas as pd
from src.datalib.visualization.advanced_plots import correlation_matrix

def test_correlation_matrix():
    data = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    correlation_matrix(data)
