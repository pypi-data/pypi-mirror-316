import matplotlib.pyplot as plt

def plot_histogram(data, title="Histogramme", bins=10):
    """
    Trace un histogramme des données.

    Parameters:
        data (array-like): Série de données à représenter.
        title (str, optional): Titre du graphique. Par défaut "Histogramme".
        bins (int, optional): Nombre de classes (bins) dans l'histogramme. Par défaut 10.

    Returns:
        None
    """
    plt.hist(data, bins=bins, color="skyblue", edgecolor="black")
    plt.title(title)
    plt.xlabel("Valeurs")
    plt.ylabel("Fréquence")
    plt.show()

def plot_scatter(x, y, title="Nuage de points"):
    """
    Trace un nuage de points entre deux séries de données.

    Parameters:
        x (array-like): Série de données pour l'axe des abscisses.
        y (array-like): Série de données pour l'axe des ordonnées.
        title (str, optional): Titre du graphique. Par défaut "Nuage de points".

    Returns:
        None
    """
    plt.scatter(x, y, color="red")
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def plot_correlation_matrix(dataframe):
    """
    Affiche une matrice de corrélation pour les colonnes numériques d'un DataFrame.

    Parameters:
        dataframe (pandas.DataFrame): DataFrame contenant les données.

    Returns:
        None
    """
    import seaborn as sns
    corr = dataframe.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Matrice de corrélation")
    plt.show()
