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
        None
    """
    # Calcul de la matrice de corrélation
    corr = dataframe.corr()

    # Création de la figure
    plt.figure(figsize=figsize)

    # Génération de la heatmap
    sns.heatmap(corr, annot=annot, cmap=cmap, fmt='.2f', linewidths=0.5, cbar_kws={'shrink': 0.8})

    # Ajout du titre
    plt.title(title)

    # Affichage de la heatmap
    plt.show()
