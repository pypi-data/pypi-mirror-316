import pytest
import numpy as np
from datalib.analysis import k_means_clustering, pca_analysis, linear_regression, polynomial_regression
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans


@pytest.fixture
def sample_data():
    """Fixture to provide sample data for testing."""
    X = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6], [0.7, 0.8], [0.9, 1.0]])
    y = np.array([1, 2, 3, 4, 5])
    return X, y


def test_k_means_clustering(sample_data):
    """Test the k_means_clustering function."""
    X, _ = sample_data

    # Test with 2 clusters
    model = k_means_clustering(X, 2)
    assert isinstance(model, KMeans), "Le modèle retourné n'est pas de type KMeans."
    assert model.n_clusters == 2, "Le nombre de clusters n'est pas correct."

    # Test for invalid input (negative clusters)
    with pytest.raises(ValueError):
        k_means_clustering(X, -1)

    # Test for invalid input (non-numeric data)
    with pytest.raises(ValueError):
        k_means_clustering(np.array([["a", "b"], ["c", "d"]]), 2)


def test_pca_analysis(sample_data):
    """Test the pca_analysis function."""
    X, _ = sample_data

    # Test PCA with 1 component
    X_pca, variance_ratio = pca_analysis(X, 1)
    assert X_pca.shape[1] == 1, "Le nombre de composantes principales n'est pas correct."
    assert len(variance_ratio) == 1, "Le ratio de variance expliqué n'est pas correct."

    # Test for invalid input (non-numeric data)
    with pytest.raises(ValueError):
        pca_analysis(np.array([["a", "b"], ["c", "d"]]), 1)

    # Test for invalid number of components
    with pytest.raises(ValueError):
        pca_analysis(X, 3)


def test_linear_regression(sample_data):
    """Test the linear_regression function."""
    X, y = sample_data

    # Test linear regression
    model = linear_regression(X, y)
    assert isinstance(model, LinearRegression), "Le modèle retourné n'est pas de type LinearRegression."
    assert hasattr(model, "coef_"), "Le modèle n'a pas d'attribut 'coef_'."

    # Test for invalid input (shape mismatch)
    with pytest.raises(ValueError):
        linear_regression(X, np.array([1, 2]))  # y has a different shape


def test_polynomial_regression(sample_data):
    """Test the polynomial_regression function."""
    X, y = sample_data

    # Test polynomial regression with degree 2
    model = polynomial_regression(X, y, degree=2)
    assert isinstance(model, LinearRegression), "Le modèle retourné n'est pas de type LinearRegression."
    assert hasattr(model, "coef_"), "Le modèle n'a pas d'attribut 'coef_'."

    # Test polynomial regression with invalid degree
    with pytest.raises(ValueError):
        polynomial_regression(X, y, degree=0)

    # Test for invalid input (shape mismatch)
    with pytest.raises(ValueError):
        polynomial_regression(X, np.array([1, 2]))  # y has a different shape
