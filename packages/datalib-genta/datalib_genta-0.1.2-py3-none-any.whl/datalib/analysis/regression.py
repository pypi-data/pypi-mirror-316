from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from typing import Tuple


def linear_regression(X: np.ndarray, y: np.ndarray) -> LinearRegression:
    """
    Effectue une régression linéaire sur un jeu de données.

    Args:
        X (np.ndarray): Les données d'entrée sous forme de tableau NumPy (ex. : [n_samples, n_features]).
        y (np.ndarray): Les cibles ou les valeurs à prédire sous forme de tableau NumPy (ex. : [n_samples]).

    Returns:
        LinearRegression: L'objet LinearRegression ajusté avec les données d'entrée.

    Raises:
        ValueError: Si les données d'entrée ne sont pas sous forme de tableau NumPy ou si leur forme est incorrecte.
        ValueError: Si le nombre de lignes de X ne correspond pas au nombre d'éléments de y.
    """
    # Vérification des données d'entrée
    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
        raise ValueError("Les données d'entrée et les cibles doivent être des tableaux NumPy.")
    if X.shape[0] != y.shape[0]:
        raise ValueError("Le nombre de lignes de X doit correspondre au nombre d'éléments de y.")

    # Application de la régression linéaire
    model = LinearRegression()
    model.fit(X, y)
    return model


def polynomial_regression(X: np.ndarray, y: np.ndarray, degree: int = 2) -> LinearRegression:
    """
    Effectue une régression polynomiale sur un jeu de données.

    Args:
        X (np.ndarray): Les données d'entrée sous forme de tableau NumPy.
        y (np.ndarray): Les cibles ou les valeurs à prédire sous forme de tableau NumPy.
        degree (int, optional): Le degré du polynôme (par défaut 2).

    Returns:
        LinearRegression: L'objet LinearRegression ajusté avec les données polynomiales.

    Raises:
        ValueError: Si les données d'entrée ne sont pas sous forme de tableau NumPy ou si leur forme est incorrecte.
        ValueError: Si le nombre de lignes de X ne correspond pas au nombre d'éléments de y.
    """
    # Vérification des données d'entrée
    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
        raise ValueError("Les données d'entrée et les cibles doivent être des tableaux NumPy.")
    if X.shape[0] != y.shape[0]:
        raise ValueError("Le nombre de lignes de X doit correspondre au nombre d'éléments de y.")
    if degree <= 0:
        raise ValueError("Le degré du polynôme doit être un entier positif.")

    # Transformation polynomiale des données
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X)

    # Application de la régression linéaire sur les données transformées
    model = LinearRegression()
    model.fit(X_poly, y)
    return model
