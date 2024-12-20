import pytest
import pandas as pd

@pytest.fixture
def sample_dataframe():
    """Fixture for creating a sample dataframe."""
    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    return pd.DataFrame(data)

def test_with_fixture(sample_dataframe):
    """Test using the sample_dataframe fixture."""
    # Ensure the dataframe is not empty
    assert not sample_dataframe.empty, "The dataframe should not be empty."
    
    # Ensure correct columns
    assert list(sample_dataframe.columns) == ["col1", "col2"], "The columns are not as expected."
    
    # Ensure correct data types for each column
    assert sample_dataframe["col1"].dtype == "int64", "Column 'col1' should have dtype 'int64'."
    assert sample_dataframe["col2"].dtype == "int64", "Column 'col2' should have dtype 'int64'."

    # Ensure that the shape of the dataframe is correct
    assert sample_dataframe.shape == (3, 2), f"Expected shape (3, 2), but got {sample_dataframe.shape}"

def test_empty_dataframe():
    """Test an empty dataframe."""
    df = pd.DataFrame()
    
    # Test if the dataframe is empty
    assert df.empty, "The dataframe should be empty."
    
    # Check if there are no columns
    assert df.shape[1] == 0, "Expected dataframe to have no columns."

def test_dataframe_with_missing_values():
    """Test dataframe with missing values."""
    data = {"col1": [1, 2, None], "col2": [4, None, 6]}
    df = pd.DataFrame(data)
    
    # Ensure the missing values are handled
    assert df.isnull().sum().sum() == 2, "There should be exactly two missing values in the dataframe."
    
    # Ensure the sum of non-null values for col1 is correct
    assert df["col1"].dropna().sum() == 3, "The sum of non-null values in 'col1' should be 3."
    
def test_dataframe_column_addition(sample_dataframe):
    """Test adding a new column to the dataframe."""
    sample_dataframe["col3"] = [7, 8, 9]
    
    # Ensure the new column is added correctly
    assert "col3" in sample_dataframe.columns, "'col3' should be added to the dataframe."
    
    # Ensure the column values are correct
    assert list(sample_dataframe["col3"]) == [7, 8, 9], "The values in 'col3' are not correct."

def test_dataframe_column_deletion(sample_dataframe):
    """Test deleting a column from the dataframe."""
    sample_dataframe.drop("col2", axis=1, inplace=True)
    
    # Ensure the column is deleted
    assert "col2" not in sample_dataframe.columns, "'col2' should be deleted from the dataframe."
    
    # Ensure the remaining columns are correct
    assert list(sample_dataframe.columns) == ["col1"], "Remaining columns should be ['col1']."

