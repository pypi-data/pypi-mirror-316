import numpy as np
import pandas as pd
import pytest
from src.datalib.data.data_cleaning import normalize_column, handle_missing_values

def test_normalize_column():
    """Test normalize_column function."""
    data = pd.DataFrame({"values": [1, 2, 3]})
    normalized = normalize_column(data, "values")
    assert normalized["values"].max() == 1, "normalize_column ne normalise pas correctement (max)."
    assert normalized["values"].min() == 0, "normalize_column ne normalise pas correctement (min)."
    assert round(normalized["values"].mean(), 3) == 0.5, "normalize_column ne normalise pas correctement (moyenne)."

def test_normalize_column_same_values():
    """Test normalize_column with a column of identical values."""
    data = pd.DataFrame({"values": [1, 1, 1]})
    normalized = normalize_column(data, "values")
    assert normalized["values"].isnull().all(), "normalize_column ne gère pas les valeurs identiques correctement."

def test_handle_missing_values_mean():
    """Test handle_missing_values with mean strategy."""
    data = pd.DataFrame({"values": [1, None, 3]})
    filled = handle_missing_values(data, strategy="mean")
    assert filled["values"].isnull().sum() == 0, "handle_missing_values (mean) ne remplit pas les valeurs manquantes correctement."
    assert filled["values"][1] == 2, "handle_missing_values (mean) ne remplace pas correctement la valeur manquante."

def test_handle_missing_values_median():
    """Test handle_missing_values with median strategy."""
    data = pd.DataFrame({"values": [1, None, 3, 4]})
    filled = handle_missing_values(data, strategy="median")
    assert filled["values"].isnull().sum() == 0, "handle_missing_values (median) ne remplit pas les valeurs manquantes correctement."
    assert filled["values"][1] == 3, "handle_missing_values (median) ne remplace pas correctement la valeur manquante."

def test_handle_missing_values_drop():
    """Test handle_missing_values with drop strategy."""
    data = pd.DataFrame({"values": [1, None, 3]})
    dropped = handle_missing_values(data, strategy="drop")
    assert len(dropped) == 2, "handle_missing_values (drop) ne fonctionne pas correctement."

def test_handle_missing_values_no_missing():
    """Test handle_missing_values when no missing values exist."""
    data = pd.DataFrame({"values": [1, 2, 3]})
    filled = handle_missing_values(data, strategy="mean")
    assert filled["values"].equals(data["values"]), "handle_missing_values (mean) ne fonctionne pas quand il n'y a pas de valeurs manquantes."

def test_handle_missing_values_invalid_strategy():
    df = pd.DataFrame({"A": [1, 2, np.nan, 4]})
    with pytest.raises(ValueError, match="Stratégie non supportée"):
        handle_missing_values(df, strategy="invalid")
