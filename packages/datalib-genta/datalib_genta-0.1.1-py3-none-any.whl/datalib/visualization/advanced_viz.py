import seaborn as sns
import matplotlib.pyplot as plt


def correlation_matrix(dataframe, annot=True, cmap="coolwarm", figsize=(10, 8), title="Correlation Matrix"):
    """
    Génère une matrice de corrélation sous forme de heatmap avec options de personnalisation.

    Args:
        dataframe (pd.DataFrame): Le DataFrame contenant les données à analyser.
        annot (bool, optional): Si True, affiche les valeurs dans les cases de la heatmap (par défaut True).
        cmap (str, optional): Le schéma de couleurs à utiliser pour la heatmap (par défaut "coolwarm").
        figsize (tuple, optional): La taille de la figure (largeur, hauteur) (par défaut (10, 8)).
        title (str, optional): Le titre de la matrice de corrélation (par défaut "Correlation Matrix").

    Returns:
        matplotlib.figure.Figure: La figure contenant la heatmap de la matrice de corrélation.
    """
    # Calcul de la matrice de corrélation
    corr = dataframe.corr()

    # Création de la figure et de l'axe
    fig, ax = plt.subplots(figsize=figsize)

    # Génération de la heatmap
    sns.heatmap(corr, annot=annot, cmap=cmap, fmt='.2f', linewidths=0.5, cbar_kws={'shrink': 0.8}, ax=ax)

    # Ajout du titre
    ax.set_title(title)
    

    # Retourner la figure pour une utilisation ou un test ultérieur
    return fig
