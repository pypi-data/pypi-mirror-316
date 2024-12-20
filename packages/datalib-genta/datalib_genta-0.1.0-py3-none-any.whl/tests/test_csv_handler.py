import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pandas as pd
import os
from datalib.preprocessing.csv_handler import load_csv, save_csv, filter_data

@pytest.fixture
def sample_dataframe():
    """Fixture for sample dataframe to be used in tests."""
    return pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

@pytest.fixture
def temporary_file():
    """Fixture to handle temporary file creation and deletion."""
    file_path = "test_temp.csv"
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

def test_load_csv(temporary_file, sample_dataframe):
    """Test the load_csv function."""
    # Save sample data to temporary file
    sample_dataframe.to_csv(temporary_file, index=False)
    
    # Load and test the CSV file
    df = load_csv(temporary_file)
    assert not df.empty, "Le dataframe chargé ne doit pas être vide."
    assert list(df.columns) == ["col1", "col2"], "Les colonnes du dataframe ne correspondent pas."

def test_save_csv(temporary_file, sample_dataframe):
    """Test the save_csv function."""
    # Save dataframe to temporary file
    save_csv(sample_dataframe, temporary_file)
    
    # Check if the file exists
    assert os.path.exists(temporary_file), f"Le fichier {temporary_file} n'a pas été créé."
    
    # Load the file and verify its content
    df_loaded = pd.read_csv(temporary_file)
    pd.testing.assert_frame_equal(sample_dataframe, df_loaded, check_dtype=True)

def test_filter_data():
    """Test the filter_data function."""
    data = {"col1": [1, 2, 3], "col2": ["a", "b", "a"]}
    df = pd.DataFrame(data)
    
    # Test filtering by value "a"
    filtered_df = filter_data(df, "col2", "a")
    assert len(filtered_df) == 2, "Le filtre ne renvoie pas le bon nombre de lignes."
    assert all(filtered_df["col2"] == "a"), "Les valeurs filtrées ne sont pas correctes."
    
    # Test error handling for non-existing column
    with pytest.raises(KeyError):
        filter_data(df, "non_existing_column", "a")
