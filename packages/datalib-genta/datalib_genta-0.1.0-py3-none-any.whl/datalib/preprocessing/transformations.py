from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

def normalize_data(dataframe, columns):
    """
    Normalise les colonnes spécifiées du DataFrame en utilisant StandardScaler.

    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données à normaliser.
        columns (list): Liste des noms de colonnes à normaliser.

    Returns:
        pd.DataFrame: Le DataFrame avec les colonnes normalisées.

    Raises:
        KeyError: Si une ou plusieurs colonnes spécifiées n'existent pas dans le DataFrame.
        ValueError: Si les colonnes spécifiées ne sont pas numériques.
    """
    # Vérification des colonnes
    missing_columns = [col for col in columns if col not in dataframe.columns]
    if missing_columns:
        raise KeyError(f"Les colonnes suivantes n'existent pas dans le DataFrame : {missing_columns}")

    # Vérification que les colonnes sont numériques
    non_numeric_columns = [col for col in columns if not np.issubdtype(dataframe[col].dtype, np.number)]
    if non_numeric_columns:
        raise ValueError(f"Les colonnes suivantes ne sont pas numériques : {non_numeric_columns}")

    # Normalisation des données
    scaler = StandardScaler()
    dataframe[columns] = scaler.fit_transform(dataframe[columns])
    return dataframe

def handle_missing_values(dataframe, strategy="mean"):
    """
    Gère les valeurs manquantes dans le DataFrame.

    Args:
        dataframe (pd.DataFrame): Le DataFrame à traiter.
        strategy (str): La stratégie à utiliser pour traiter les valeurs manquantes.
            Options : 
            - "mean" : Remplacer les valeurs manquantes par la moyenne.
            - "median" : Remplacer les valeurs manquantes par la médiane.
            - "drop" : Supprimer les lignes contenant des valeurs manquantes.

    Returns:
        pd.DataFrame: Le DataFrame après traitement des valeurs manquantes.

    Raises:
        ValueError: Si une stratégie invalide est spécifiée.
    """
    if strategy == "mean":
        return dataframe.fillna(dataframe.mean(numeric_only=True))
    elif strategy == "median":
        return dataframe.fillna(dataframe.median(numeric_only=True))
    elif strategy == "drop":
        return dataframe.dropna()
    else:
        raise ValueError("Stratégie non supportée : choisissez parmi 'mean', 'median', ou 'drop'.")
