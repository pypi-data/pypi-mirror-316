import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pandas as pd
from datalib.statslib.basic_stats import calculate_mode, calculate_std, calculate_correlation

@pytest.fixture
def sample_mode_data():
    """Fixture for sample data to test mode calculation."""
    return pd.DataFrame({"values": [1, 2, 2, 3, 4]})

@pytest.fixture
def sample_std_data():
    """Fixture for sample data to test standard deviation calculation."""
    return pd.DataFrame({"values": [1, 2, 3, 4, 5]})

@pytest.fixture
def sample_correlation_data():
    """Fixture for sample data to test correlation calculation."""
    return pd.DataFrame({"col1": [1, 2, 3], "col2": [1, 2, 3]})

def test_calculate_mode(sample_mode_data):
    """Test the calculate_mode function."""
    mode = calculate_mode(sample_mode_data, "values")
    # Verify the mode value is correct
    assert mode == 2, f"Expected mode to be 2, but got {mode}"

def test_calculate_std(sample_std_data):
    """Test the calculate_std function."""
    std = calculate_std(sample_std_data, "values")
    # Verify the standard deviation value is correct, rounded to 2 decimal places
    assert round(std, 2) == 1.58, f"Expected standard deviation to be 1.58, but got {round(std, 2)}"

def test_calculate_correlation(sample_correlation_data):
    """Test the calculate_correlation function."""
    correlation = calculate_correlation(sample_correlation_data, "col1", "col2")
    # Verify the correlation value is correct
    assert correlation == 1, f"Expected correlation to be 1, but got {correlation}"

def test_calculate_mode_with_empty_column():
    """Test the calculate_mode function with an empty column."""
    df = pd.DataFrame({"values": []})
    try:
        calculate_mode(df, "values")
    except ValueError as e:
        assert str(e) == "La colonne 'values' est vide ou invalide."

def test_calculate_std_with_single_value():
    """Test the calculate_std function with a single value column."""
    df = pd.DataFrame({"values": [5]})
    std = calculate_std(df, "values")
    # Standard deviation for a single value should be 0
    assert std == 0, f"Expected standard deviation to be 0, but got {std}"
