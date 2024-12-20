import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pandas as pd
from datalib.preprocessing.transformations import normalize_data, handle_missing_values

@pytest.fixture
def sample_normalize_data():
    """Fixture for sample data to test normalization."""
    return pd.DataFrame({"values": [1, 2, 3, 4, 5]})

@pytest.fixture
def sample_missing_values_data():
    """Fixture for sample data to test missing values handling."""
    return pd.DataFrame({"col1": [1, None, 3], "col2": [4, 5, None]})

def test_normalize_data(sample_normalize_data):
    """Test the normalize_data function."""
    normalized_df = normalize_data(sample_normalize_data, "values")
    
    # Check if the normalized values are between 0 and 1
    assert 0 <= normalized_df["values"].min() <= 1, f"Expected normalized min value to be between 0 and 1, but got {normalized_df['values'].min()}"
    assert 0 <= normalized_df["values"].max() <= 1, f"Expected normalized max value to be between 0 and 1, but got {normalized_df['values'].max()}"
    
    # Verify that the normalization is correct by comparing with expected normalized values
    expected_values = [0, 0.25, 0.5, 0.75, 1]
    assert all(abs(normalized_df["values"].values - expected_values) < 1e-6), "Normalized values do not match expected range."

def test_handle_missing_values_with_mean(sample_missing_values_data):
    """Test the handle_missing_values function using the 'mean' strategy."""
    handled_df = handle_missing_values(sample_missing_values_data, strategy="mean")
    
    # Verify that there are no missing values left
    assert handled_df.isnull().sum().sum() == 0, f"Expected no missing values, but found {handled_df.isnull().sum().sum()}"

    # Verify that the missing value in col1 is replaced by the mean of the non-null values in that column
    assert handled_df.loc[1, "col1"] == 2, f"Expected value in col1[1] to be 2 (mean of [1, 3]), but got {handled_df.loc[1, 'col1']}"

    # Verify the same for col2
    assert handled_df.loc[2, "col2"] == 4.5, f"Expected value in col2[2] to be 4.5 (mean of [4, 5]), but got {handled_df.loc[2, 'col2']}"

def test_handle_missing_values_with_drop(sample_missing_values_data):
    """Test the handle_missing_values function using the 'drop' strategy."""
    handled_df = handle_missing_values(sample_missing_values_data, strategy="drop")
    
    # Verify that the row with missing values has been dropped
    assert handled_df.shape[0] == 2, f"Expected 2 rows after dropping missing values, but got {handled_df.shape[0]}"
    assert handled_df.isnull().sum().sum() == 0, f"Expected no missing values, but found {handled_df.isnull().sum().sum()}"

def test_handle_missing_values_with_invalid_strategy(sample_missing_values_data):
    """Test the handle_missing_values function with an invalid strategy."""
    try:
        handle_missing_values(sample_missing_values_data, strategy="invalid")
    except ValueError as e:
        assert str(e) == "Stratégie non supportée : choisissez parmi 'mean', 'median', ou 'drop'.", f"Unexpected error message: {e}"

def test_normalize_data_with_non_numeric_column():
    """Test normalize_data with a non-numeric column."""
    df = pd.DataFrame({"non_numeric": ["a", "b", "c"]})
    try:
        normalize_data(df, "non_numeric")
    except ValueError as e:
        assert str(e) == "Les colonnes suivantes ne sont pas numériques : ['non_numeric']", f"Unexpected error message: {e}"
