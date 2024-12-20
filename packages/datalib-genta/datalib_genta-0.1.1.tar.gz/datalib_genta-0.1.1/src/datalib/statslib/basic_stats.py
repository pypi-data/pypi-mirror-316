import pandas as pd
import numpy as np
from typing import Optional, Union

def calculate_mean(dataframe: pd.DataFrame, column: str) -> Union[float, None]:
    """
    Calcule la moyenne d'une colonne dans le DataFrame.
    
    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        column (str): Le nom de la colonne dont la moyenne doit être calculée.
    
    Returns:
        Union[float, None]: La moyenne de la colonne, ou None si la colonne est vide.
    
    Raises:
        KeyError: Si la colonne spécifiée n'existe pas dans le DataFrame.
    """
    if column not in dataframe.columns:
        raise KeyError(f"La colonne '{column}' n'existe pas dans le DataFrame.")
    return dataframe[column].mean()

def calculate_median(dataframe: pd.DataFrame, column: str) -> Union[float, None]:
    """
    Calcule la médiane d'une colonne dans le DataFrame.
    
    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        column (str): Le nom de la colonne dont la médiane doit être calculée.
    
    Returns:
        Union[float, None]: La médiane de la colonne, ou None si la colonne est vide.
    
    Raises:
        KeyError: Si la colonne spécifiée n'existe pas dans le DataFrame.
    """
    if column not in dataframe.columns:
        raise KeyError(f"La colonne '{column}' n'existe pas dans le DataFrame.")
    return dataframe[column].median()

def calculate_mode(dataframe: pd.DataFrame, column: str) -> Union[float, None]:
    """
    Calcule le mode d'une colonne dans le DataFrame.
    
    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        column (str): Le nom de la colonne dont le mode doit être calculé.
    
    Returns:
        Union[float, None]: Le mode de la colonne, ou None si la colonne est vide ou si aucun mode n'est trouvé.
    
    Raises:
        KeyError: Si la colonne spécifiée n'existe pas dans le DataFrame.
    """
    if column not in dataframe.columns:
        raise KeyError(f"La colonne '{column}' n'existe pas dans le DataFrame.")
    mode = dataframe[column].mode()
    if mode.empty:
        return None
    return mode.iloc[0]

def calculate_std(dataframe: pd.DataFrame, column: str) -> Union[float, None]:
    """
    Calcule l'écart-type d'une colonne dans le DataFrame.

    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        column (str): Le nom de la colonne dont l'écart-type doit être calculé.

    Returns:
        Union[float, None]: L'écart-type de la colonne, ou None si la colonne est vide ou ne contient qu'une seule valeur.

    Raises:
        KeyError: Si la colonne spécifiée n'existe pas dans le DataFrame.
    """
    if column not in dataframe.columns:
        raise KeyError(f"La colonne '{column}' n'existe pas dans le DataFrame.")
    
    # Handle empty or single-value columns
    if dataframe[column].nunique() <= 1:
        return 0.0  # Standard deviation is 0 for single-value columns
    
    return dataframe[column].std()


def calculate_correlation(dataframe: pd.DataFrame, col1: str, col2: str) -> Optional[float]:
    """
    Calcule la corrélation entre deux colonnes dans le DataFrame.
    
    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        col1 (str): Le nom de la première colonne.
        col2 (str): Le nom de la deuxième colonne.
    
    Returns:
        Optional[float]: La corrélation entre les deux colonnes, ou None si l'une des colonnes est vide ou non numérique.
    
    Raises:
        KeyError: Si l'une ou l'autre des colonnes spécifiées n'existe pas dans le DataFrame.
        ValueError: Si l'une des colonnes spécifiées n'est pas numérique.
    """
    if col1 not in dataframe.columns or col2 not in dataframe.columns:
        raise KeyError(f"Les colonnes '{col1}' et/ou '{col2}' n'existent pas dans le DataFrame.")
    
    # Vérification que les colonnes sont numériques
    if not np.issubdtype(dataframe[col1].dtype, np.number) or not np.issubdtype(dataframe[col2].dtype, np.number):
        raise ValueError(f"Les colonnes '{col1}' et '{col2}' doivent être numériques pour calculer la corrélation.")
    
    return dataframe[col1].corr(dataframe[col2])
