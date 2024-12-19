import matplotlib.pyplot as plt
from src.datalib.visualization.simple_plots import bar_chart, histogram, scatter_plot

def test_bar_chart():
    bar_chart([1, 2, 3], ["A", "B", "C"], title="Test Bar Chart")
    plt.close()

def test_histogram():
    histogram([1, 2, 3, 3, 2, 1], bins=3, title="Test Histogram")
    plt.close()

def test_scatter_plot():
    scatter_plot([1, 2, 3], [3, 2, 1], title="Test Scatter Plot")
    plt.close()
