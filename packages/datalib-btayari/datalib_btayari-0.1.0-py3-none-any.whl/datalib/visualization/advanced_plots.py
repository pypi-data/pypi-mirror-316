import seaborn as sns
import matplotlib.pyplot as plt

def correlation_matrix(dataframe):
    """Afficher une matrice de corrélation."""
    corr = dataframe.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.show()
