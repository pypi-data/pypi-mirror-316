import matplotlib.pyplot as plt

def bar_chart(data, labels, title="Bar Chart"):
    """Créer un graphique en barres."""
    plt.bar(labels, data)
    plt.title(title)
    plt.show()

def histogram(data, bins=10, title="Histogram"):
    """Créer un histogramme."""
    plt.hist(data, bins=bins)
    plt.title(title)
    plt.show()

def scatter_plot(x, y, title="Scatter Plot"):
    """Créer un nuage de points."""
    plt.scatter(x, y)
    plt.title(title)
    plt.show()
