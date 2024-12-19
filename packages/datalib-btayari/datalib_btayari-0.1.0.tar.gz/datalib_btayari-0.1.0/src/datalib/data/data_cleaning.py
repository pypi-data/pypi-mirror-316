import pandas as pd

def normalize_column(dataframe, column):
    """Normaliser une colonne spécifique."""
    dataframe[column] = (dataframe[column] - dataframe[column].min()) / (dataframe[column].max() - dataframe[column].min())
    return dataframe

def handle_missing_values(dataframe, strategy='mean'):
    """Gérer les valeurs manquantes."""
    if strategy == 'mean':
        return dataframe.fillna(dataframe.mean())
    elif strategy == 'median':
        return dataframe.fillna(dataframe.median())
    elif strategy == 'drop':
        return dataframe.dropna()
    else:
        raise ValueError("Stratégie non supportée : 'mean', 'median', 'drop'")
