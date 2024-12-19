import pandas as pd
from src.datalib.data.data_cleaning import normalize_column, handle_missing_values

def test_normalize_column():
    data = pd.DataFrame({"values": [1, 2, 3]})
    normalized = normalize_column(data, "values")
    assert normalized["values"].max() == 1 and normalized["values"].min() == 0, "normalize_column ne fonctionne pas correctement."

def test_handle_missing_values_mean():
    data = pd.DataFrame({"values": [1, None, 3]})
    filled = handle_missing_values(data, strategy="mean")
    assert filled["values"].isnull().sum() == 0 and filled["values"][1] == 2, "handle_missing_values (mean) ne fonctionne pas."

def test_handle_missing_values_drop():
    data = pd.DataFrame({"values": [1, None, 3]})
    dropped = handle_missing_values(data, strategy="drop")
    assert len(dropped) == 2, "handle_missing_values (drop) ne fonctionne pas."
