import pytest
from datalib.data_processing import load_csv, save_csv
import pandas as pd
from io import StringIO

@pytest.fixture
def sample_csv():
    data = """col1,col2\n1,2\n3,4"""
    return StringIO(data)


def test_load_csv(sample_csv):
    df = load_csv(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["col1", "col2"]


def test_save_csv(tmp_path):
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    filepath = tmp_path / "output.csv"
    save_csv(df, filepath)
    assert filepath.read_text().startswith("col1,col2")