# __init__.py

import pytest

# Example of a shared fixture
@pytest.fixture
def sample_dataframe():
    import pandas as pd
    data = {"col1": [1, 2, 3], "col2": [4, 5, 6]}
    return pd.DataFrame(data)
