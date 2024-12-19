import pandas as pd

def read_csv(file_path):
    """Lire un fichier CSV."""
    return pd.read_csv(file_path)

def write_csv(dataframe, file_path):
    """Écrire un DataFrame dans un fichier CSV."""
    dataframe.to_csv(file_path, index=False)

def filter_data(dataframe, column, condition):
    """Filtrer les données en fonction d'une condition."""
    return dataframe.query(f"{column} {condition}")
