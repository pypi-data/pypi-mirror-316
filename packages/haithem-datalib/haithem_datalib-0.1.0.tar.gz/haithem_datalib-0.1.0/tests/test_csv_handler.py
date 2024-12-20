import os
import pytest
import pandas as pd
from src.datalib.data.csv_handler import read_csv, write_csv, filter_data

@pytest.fixture
def temp_csv_file():
    """Fixture to create and clean up a temporary CSV file."""
    file_name = "test_temp.csv"
    yield file_name
    if os.path.exists(file_name):
        os.remove(file_name)

def test_read_csv(temp_csv_file):
    """Test read_csv function."""
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    data.to_csv(temp_csv_file, index=False)

    df = read_csv(temp_csv_file)
    assert df.equals(data), "read_csv ne fonctionne pas correctement."
    # Clean up is handled by the fixture

def test_read_csv_non_existent_file():
    """Test read_csv with a non-existent file."""
    with pytest.raises(FileNotFoundError):
        read_csv("non_existent_file.csv")

def test_write_csv(temp_csv_file):
    """Test write_csv function."""
    data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    write_csv(data, temp_csv_file)
    
    df = pd.read_csv(temp_csv_file)
    assert df.equals(data), "write_csv ne fonctionne pas correctement."

def test_filter_data():
    """Test filter_data function."""
    data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    
    # Test with a condition that filters only the last row
    filtered = filter_data(data, "col1", "> 2")
    assert len(filtered) == 1, "filter_data ne filtre pas correctement."
    assert filtered.iloc[0]["col1"] == 3, "filter_data ne fonctionne pas pour le filtre col1 > 2."

    # Test with an empty DataFrame
    empty_data = pd.DataFrame({"col1": [], "col2": []})
    filtered_empty = filter_data(empty_data, "col1", "> 2")
    assert filtered_empty.empty, "filter_data ne gère pas les DataFrames vides."

    # Test with a condition that results in no data being selected
    filtered_none = filter_data(data, "col1", "> 10")
    assert filtered_none.empty, "filter_data ne gère pas les conditions retournant un DataFrame vide."

