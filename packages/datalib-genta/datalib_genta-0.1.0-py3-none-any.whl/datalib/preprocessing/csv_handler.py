import pandas as pd

def load_csv(file_path, encoding='utf-8'):
    """
    Charge un fichier CSV et retourne un DataFrame.

    Args:
        file_path (str): Le chemin vers le fichier CSV.
        encoding (str, optional): L'encodage du fichier CSV (par défaut 'utf-8').

    Returns:
        pd.DataFrame: Le DataFrame contenant les données du fichier CSV.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        pd.errors.EmptyDataError: Si le fichier est vide.
        pd.errors.ParserError: Si le fichier contient des erreurs de format.
    """
    try:
        return pd.read_csv(file_path, encoding=encoding)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Le fichier {file_path} est vide.")
    except pd.errors.ParserError:
        raise ValueError(f"Le fichier {file_path} contient des erreurs de format.")


def save_csv(dataframe, file_path, encoding='utf-8'):
    """
    Enregistre un DataFrame dans un fichier CSV.

    Args:
        dataframe (pd.DataFrame): Le DataFrame à enregistrer.
        file_path (str): Le chemin où enregistrer le fichier CSV.
        encoding (str, optional): L'encodage du fichier CSV (par défaut 'utf-8').

    Returns:
        None
    """
    try:
        dataframe.to_csv(file_path, index=False, encoding=encoding)
    except Exception as e:
        raise ValueError(f"Erreur lors de l'enregistrement du fichier {file_path}: {e}")


def filter_data(dataframe, column, value):
    """
    Filtre les lignes du DataFrame selon une valeur dans une colonne donnée.

    Args:
        dataframe (pd.DataFrame): Le DataFrame à filtrer.
        column (str): Le nom de la colonne sur laquelle appliquer le filtre.
        value: La valeur à rechercher dans la colonne.

    Returns:
        pd.DataFrame: Un nouveau DataFrame contenant les lignes filtrées.

    Raises:
        KeyError: Si la colonne spécifiée n'existe pas dans le DataFrame.
    """
    if column not in dataframe.columns:
        raise KeyError(f"La colonne '{column}' n'existe pas dans le DataFrame.")
    return dataframe[dataframe[column] == value]
