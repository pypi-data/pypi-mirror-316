import os
import pandas as pd
from src.datalib.data.csv_handler import read_csv, write_csv, filter_data

def test_read_csv():
    test_file = "test.csv"
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    data.to_csv(test_file, index=False)

    df = read_csv(test_file)
    assert df.equals(data), "read_csv ne fonctionne pas correctement."
    os.remove(test_file)

def test_write_csv():
    test_file = "test_output.csv"
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    write_csv(data, test_file)
    df = pd.read_csv(test_file)
    assert df.equals(data), "write_csv ne fonctionne pas correctement."
    os.remove(test_file)

def test_filter_data():
    data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    filtered = filter_data(data, "col1", "> 2")
    assert len(filtered) == 1 and filtered.iloc[0]["col1"] == 3, "filter_data ne fonctionne pas correctement."
