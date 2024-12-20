import pandas as pd
from datalib.manipulation import read_csv, write_csv, fill_missing_values
from datalib.data_statistics import calculate_mean, calculate_median, calculate_mode, calculate_statistics, calculate_std, calculate_correlation
from datalib.visualization import plot_correlation_matrix, plot_histogram, plot_scatter
from datalib.analysis import linear_regression, kmeans_clustering, pca_analysis
import matplotlib.pyplot as plt

def main():
    """
    Fonction principale exécutant une série d'analyses et de visualisations sur un dataset CSV.
    
    Elle inclut les étapes suivantes :
    1. Chargement du dataset depuis un fichier CSV.
    2. Manipulation des données, y compris le remplissage des valeurs manquantes.
    3. Sauvegarde des données modifiées dans un nouveau fichier CSV.
    4. Calcul des statistiques pour les colonnes numériques du dataset.
    5. Visualisation des données avec des histogrammes, des nuages de points et une matrice de corrélation.
    6. Analyse avancée comprenant :
        - Régression linéaire
        - Clustering k-means
        - Analyse en composantes principales (ACP)
    
    Utilise des fonctions provenant de différentes parties de la bibliothèque `datalib`.
    
    Returns:
        None: Cette fonction ne retourne rien mais affiche les résultats et les graphiques.
    """
    print('WELCOME!!')
    # Charger le dataset depuis le fichier CSV en utilisant la fonction read_csv
    file_path = 'enhanced_fever_medicine_recommendation.csv'  # Chemin vers votre fichier CSV
    loaded_data = read_csv(file_path)

    # Affichage des premières lignes du dataset
    print("=== DONNÉES CHARGÉES ===")
    print(loaded_data.head())

    # Manipulation des données (ici, nous remplissons les valeurs manquantes)
    loaded_data = fill_missing_values(loaded_data)  # Remplir les valeurs manquantes avec la moyenne des colonnes
    print("=== DONNÉES APRÈS REMPLISSAGE DES VALEURS MANQUANTES ===")
    print(loaded_data.head())

    # Sauvegarder les données transformées dans un nouveau fichier CSV
    filled_file_path = "filled_fever_medicine_data.csv"
    write_csv(loaded_data, filled_file_path)
    print(f"Fichier '{filled_file_path}' sauvegardé.")

    # Calcul des statistiques sur les colonnes pertinentes (remplacez 'column_name' par les vraies colonnes)
   # Calculate statistics for all numeric columns
    print("=== STATISTIQUES ===")
    calculate_statistics(loaded_data)

    # Visualisation des données
    print("\n=== VISUALISATION ===")

    # Auto-detect numeric columns for visualizations
    numeric_columns = loaded_data.select_dtypes(include=["number"]).columns
    print(f"Numeric columns detected: {numeric_columns.tolist()}")

    # Plot histogram for each numeric column
    for column in numeric_columns:
        print(f"Generating histogram for: {column}")
        plot_histogram(loaded_data[column], title=f"Histogramme de {column}")

    # Auto-generate scatter plots between each pair of numeric columns
    for i, column_x in enumerate(numeric_columns):
        for column_y in numeric_columns[i+1:]:
            print(f"Generating scatter plot: {column_x} vs {column_y}")
            plot_scatter(loaded_data[column_x], loaded_data[column_y], title=f"Nuage de points {column_x} vs {column_y}")

    # Generate correlation matrix
    print("Generating correlation matrix...")
    plot_correlation_matrix(loaded_data)

    print("\n=== ANALYSE AVANCÉE ===")
    X = loaded_data[numeric_columns].fillna(0)
    
    # Régression linéaire
    if len(numeric_columns) >= 2:
        y = X.iloc[:, 1]
        model = linear_regression(X.iloc[:, [0]], y)
        print("Régression linéaire : Coefficients :", model.coef_, "Intercept :", model.intercept_)

        # Visualisation de la régression linéaire
        plt.scatter(X.iloc[:, 0], y, color="blue", label="Données réelles")
        plt.plot(X.iloc[:, 0], model.predict(X.iloc[:, [0]]), color="red", label="Régression linéaire")
        plt.title("Régression Linéaire")
        plt.xlabel("Variable Indépendante (X)")
        plt.ylabel("Variable Dépendante (y)")
        plt.legend()
        plt.show()

    # Clustering k-means
    kmeans = kmeans_clustering(X, n_clusters=2)
    print("Centroides des clusters :", kmeans.cluster_centers_)

    # Visualisation des clusters
    if X.shape[1] >= 2:
        plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=kmeans.labels_, cmap="viridis", label="Clusters")
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color="red", marker="x", label="Centroïdes")
        plt.title("Clustering k-means")
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.legend()
        plt.show()

    # PCA
    pca, X_pca = pca_analysis(X, n_components=2)
    print("Résultat de l'ACP (2 composantes) :\n", X_pca)

    # Visualisation de l'ACP
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c='orange')
    plt.title("Analyse en Composantes Principales (ACP)")
    plt.xlabel("Composante Principale 1")
    plt.ylabel("Composante Principale 2")
    plt.show()

if __name__ == "__main__":
    main()
