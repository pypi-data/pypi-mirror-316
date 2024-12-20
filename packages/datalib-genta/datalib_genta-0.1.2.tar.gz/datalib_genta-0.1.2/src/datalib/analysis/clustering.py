from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from typing import Tuple, Any


def k_means_clustering(X: np.ndarray, n_clusters: int) -> KMeans:
    """
    Effectue un clustering k-means sur un jeu de données.

    Args:
        X (np.ndarray): Les données d'entrée sous forme de tableau NumPy (ex. : [n_samples, n_features]).
        n_clusters (int): Le nombre de clusters à former.

    Returns:
        KMeans: L'objet KMeans ajusté avec les données d'entrée.

    Raises:
        ValueError: Si le nombre de clusters est inférieur ou égal à zéro.
        ValueError: Si les données d'entrée ne sont pas numériques.
    """
    # Vérification des données d'entrée
    if not isinstance(X, np.ndarray):
        raise ValueError("Les données d'entrée doivent être un tableau NumPy.")
    if n_clusters <= 0:
        raise ValueError("Le nombre de clusters doit être un entier positif.")
    
    # Check for non-numeric data
    if not np.issubdtype(X.dtype, np.number):
        raise ValueError("Les données d'entrée doivent être numériques.")

    if np.any(np.isnan(X)) or np.any(np.isinf(X)):
        raise ValueError("Les données d'entrée ne doivent pas contenir de valeurs NaN ou infinies.")

    # Application de l'algorithme KMeans
    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(X)
    return model



def pca_analysis(X: np.ndarray, n_components: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Effectue une analyse en composantes principales (PCA) sur un jeu de données.

    Args:
        X (np.ndarray): Les données d'entrée sous forme de tableau NumPy.
        n_components (int): Le nombre de composantes principales à retenir.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Le tableau transformé des données réduites et les ratios de variance expliquée.

    Raises:
        ValueError: Si le nombre de composantes est supérieur au nombre de caractéristiques des données.
        ValueError: Si les données d'entrée ne sont pas numériques ou contiennent des NaN/inf.
    """
    # Vérification des données d'entrée
    if not isinstance(X, np.ndarray):
        raise ValueError("Les données d'entrée doivent être un tableau NumPy.")
    if n_components <= 0 or n_components > X.shape[1]:
        raise ValueError(f"Le nombre de composantes principales doit être un entier positif et inférieur ou égal au nombre de caractéristiques (actuellement {X.shape[1]}).")

    # Check for non-numeric data
    if not np.issubdtype(X.dtype, np.number):
        raise ValueError("Les données d'entrée doivent être numériques.")

    # Check for NaN or infinite values
    if np.any(np.isnan(X)) or np.any(np.isinf(X)):
        raise ValueError("Les données d'entrée ne doivent pas contenir de valeurs NaN ou infinies.")

    # Application de l'analyse en composantes principales (PCA)
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    return X_pca, pca.explained_variance_ratio_
