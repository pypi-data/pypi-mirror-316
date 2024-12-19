import pandas as pd

def calculate_mean(dataframe, column):
    """Calculer la moyenne."""
    return dataframe[column].mean()

def calculate_median(dataframe, column):
    """Calculer la médiane."""
    return dataframe[column].median()

def calculate_mode(dataframe, column):
    """Calculer le mode."""
    return dataframe[column].mode()[0]

def calculate_std_dev(dataframe, column):
    """Calculer l'écart-type."""
    return dataframe[column].std()

def calculate_correlation(dataframe, col1, col2):
    """Calculer la corrélation entre deux colonnes."""
    return dataframe[col1].corr(dataframe[col2])
