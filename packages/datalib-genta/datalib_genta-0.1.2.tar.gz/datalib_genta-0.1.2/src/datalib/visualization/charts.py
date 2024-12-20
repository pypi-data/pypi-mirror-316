import matplotlib.pyplot as plt


def bar_chart(dataframe, column, title=None, xlabel=None, ylabel=None, color='skyblue', figsize=(10, 6)):
    """
    Génère un graphique à barres.

    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        column (str): Le nom de la colonne pour le graphique à barres.
        title (str, optional): Titre du graphique (par défaut None).
        xlabel (str, optional): Label de l'axe x (par défaut None).
        ylabel (str, optional): Label de l'axe y (par défaut None).
        color (str, optional): Couleur des barres (par défaut 'skyblue').
        figsize (tuple, optional): Taille de la figure (par défaut (10, 6)).

    Returns:
        None
    """
    # Vérification que la colonne existe
    if column not in dataframe.columns:
        raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame.")

    # Création du graphique à barres
    plt.figure(figsize=figsize)
    dataframe[column].value_counts().plot(kind="bar", color=color)

    # Ajout du titre et des labels
    plt.title(title or f"Bar Chart of {column}")
    plt.xlabel(xlabel or column)
    plt.ylabel(ylabel or 'Frequency')

    # Retourner la figure pour les tests
    return plt.gcf()  # plt.gcf() returns the current figure



def histogram(dataframe, column, bins=30, title=None, xlabel=None, ylabel=None, color='skyblue', figsize=(10, 6)):
    """
    Génère un histogramme.

    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        column (str): Le nom de la colonne pour l'histogramme.
        bins (int, optional): Nombre de bins pour l'histogramme (par défaut 30).
        title (str, optional): Titre du graphique (par défaut None).
        xlabel (str, optional): Label de l'axe x (par défaut None).
        ylabel (str, optional): Label de l'axe y (par défaut None).
        color (str, optional): Couleur des barres de l'histogramme (par défaut 'skyblue').
        figsize (tuple, optional): Taille de la figure (par défaut (10, 6)).

    Returns:
        matplotlib.figure.Figure: La figure contenant l'histogramme.
    """
    # Vérification que la colonne existe
    if column not in dataframe.columns:
        raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame.")

    # Création de l'histogramme
    fig, ax = plt.subplots(figsize=figsize)
    dataframe[column].plot(kind="hist", bins=bins, color=color, edgecolor='black', ax=ax)

    # Ajout du titre et des labels
    ax.set_title(title or f"Histogram of {column}")
    ax.set_xlabel(xlabel or column)
    ax.set_ylabel(ylabel or 'Frequency')

    # Retourner la figure pour une utilisation ou un test ultérieur
    return fig



def scatter_plot(dataframe, x_col, y_col, title=None, xlabel=None, ylabel=None, color='skyblue', figsize=(10, 6)):
    """
    Génère un nuage de points.

    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données.
        x_col (str): Le nom de la colonne pour l'axe x.
        y_col (str): Le nom de la colonne pour l'axe y.
        title (str, optional): Titre du graphique (par défaut None).
        xlabel (str, optional): Label de l'axe x (par défaut None).
        ylabel (str, optional): Label de l'axe y (par défaut None).
        color (str, optional): Couleur des points (par défaut 'skyblue').
        figsize (tuple, optional): Taille de la figure (par défaut (10, 6)).

    Returns:
        matplotlib.figure.Figure: La figure contenant le nuage de points.
    """
    # Vérification que les colonnes existent
    if x_col not in dataframe.columns or y_col not in dataframe.columns:
        raise ValueError(f"Les colonnes '{x_col}' ou '{y_col}' n'existent pas dans le DataFrame.")

    # Création du nuage de points
    fig, ax = plt.subplots(figsize=figsize)
    dataframe.plot(kind="scatter", x=x_col, y=y_col, color=color, ax=ax)

    # Ajout du titre et des labels
    ax.set_title(title or f"Scatter Plot of {x_col} vs {y_col}")
    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel or y_col)

    # Retourner la figure pour une utilisation ou un test ultérieur
    return fig
