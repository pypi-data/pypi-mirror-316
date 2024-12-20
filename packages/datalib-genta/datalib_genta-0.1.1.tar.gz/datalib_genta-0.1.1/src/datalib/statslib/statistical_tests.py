import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency
from typing import Union, Dict, Any

def t_test(group1: pd.Series, group2: pd.Series) -> Dict[str, Union[float, None]]:
    """
    Effectue un test t pour deux groupes indépendants afin de comparer leurs moyennes.
    
    Args:
        group1 (pd.Series): Les données du premier groupe.
        group2 (pd.Series): Les données du deuxième groupe.
    
    Returns:
        Dict[str, Union[float, None]]: Un dictionnaire contenant la statistique du test et la p-valeur.
    
    Raises:
        ValueError: Si les deux groupes n'ont pas le même nombre d'éléments ou contiennent des valeurs non numériques.
    """
    # Vérification que les groupes contiennent des valeurs numériques
    if not pd.api.types.is_numeric_dtype(group1) or not pd.api.types.is_numeric_dtype(group2):
        raise ValueError("Les groupes doivent contenir des données numériques.")
    
    # Vérification que les groupes ont la même taille
    if len(group1) != len(group2):
        raise ValueError("Les deux groupes doivent avoir le même nombre d'éléments.")
    
    stat, p_value = ttest_ind(group1, group2)
    return {"statistic": stat, "p_value": p_value}

def chi_square_test(dataframe: pd.DataFrame, col1: str, col2: str) -> Dict[str, Any]:
    """
    Effectue un test du chi-carré entre deux colonnes catégoriques d'un DataFrame.
    
    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        col1 (str): Le nom de la première colonne catégorique.
        col2 (str): Le nom de la deuxième colonne catégorique.
    
    Returns:
        Dict[str, Any]: Un dictionnaire contenant les résultats du test (statistique chi2, p-valeur, degrés de liberté, et valeurs attendues).
    
    Raises:
        KeyError: Si l'une ou l'autre des colonnes spécifiées n'existe pas dans le DataFrame.
        ValueError: Si les colonnes spécifiées ne sont pas catégorielles.
    """
    # Vérification que les colonnes existent dans le DataFrame
    if col1 not in dataframe.columns or col2 not in dataframe.columns:
        raise KeyError(f"Les colonnes '{col1}' et/ou '{col2}' n'existent pas dans le DataFrame.")
    
    # Vérification que les colonnes sont catégorielles (types object ou category)
    if not pd.api.types.is_categorical_dtype(dataframe[col1]) and not pd.api.types.is_object_dtype(dataframe[col1]):
        raise ValueError(f"La colonne '{col1}' doit être catégorielle (type 'object' ou 'category').")
    
    if not pd.api.types.is_categorical_dtype(dataframe[col2]) and not pd.api.types.is_object_dtype(dataframe[col2]):
        raise ValueError(f"La colonne '{col2}' doit être catégorielle (type 'object' ou 'category').")
    
    # Création de la table de contingence
    contingency_table = pd.crosstab(dataframe[col1], dataframe[col2])
    
    # Test du chi-carré
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return {
        "chi2": chi2,
        "p_value": p,
        "dof": dof,
        "expected": expected
    }
