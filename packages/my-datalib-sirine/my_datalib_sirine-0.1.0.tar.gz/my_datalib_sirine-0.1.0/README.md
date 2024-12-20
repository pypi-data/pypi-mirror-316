# DataLib

DataLib est une bibliothèque Python dédiée à la manipulation, l'analyse et la visualisation de données. Elle offre des fonctionnalités pour charger, nettoyer, analyser et visualiser des données de manière simple et efficace.

## Fonctionnalités principales

### 1. Manipulation des données
- **Chargement de données** : Chargement de fichiers CSV dans des DataFrames à l'aide de `read_csv`.
- **Écriture de données** : Enregistrement des DataFrames dans des fichiers CSV avec `write_csv`.
- **Traitement des valeurs manquantes** : Remplissage des valeurs manquantes avec des méthodes comme la moyenne, la médiane ou le mode via `fill_missing_values`.

### 2. Calcul des statistiques
- **Statistiques descriptives** : Calcul des principales statistiques sur les colonnes numériques (moyenne, médiane, écart-type, mode) avec des fonctions comme `calculate_mean`, `calculate_median`, `calculate_std`, et `calculate_mode`.
- **Corrélation** : Calcul de la corrélation entre deux séries de données avec `calculate_correlation`.
- **Statistiques automatiques** : Calcul automatique des statistiques pour toutes les colonnes numériques d'un DataFrame avec `calculate_statistics`.

### 3. Visualisation des données
- **Histogrammes** : Visualisation de la distribution des données avec des histogrammes via `plot_histogram`.
- **Nuages de points** : Génération de nuages de points pour explorer les relations entre deux séries de données avec `plot_scatter`.
- **Matrice de corrélation** : Affichage d'une matrice de corrélation pour visualiser les relations entre toutes les colonnes numériques d'un DataFrame avec `plot_correlation_matrix`.

### 4. Analyse avancée
- **Régression linéaire** : Application d'un modèle de régression linéaire sur des données avec `linear_regression`.
- **Régression polynomiale** : Application d'une régression polynomiale pour ajuster des courbes de degré supérieur avec `polynomial_regression`.
- **Clustering K-means** : Application de l'algorithme de clustering K-means pour regrouper des données avec `kmeans_clustering`.
- **Analyse en Composantes Principales (PCA)** : Réduction de la dimensionnalité des données avec PCA via `pca_analysis`.
- **Classification k-NN et arbre de décision** : Classification des données avec les modèles k-NN (`knn_classification`) et arbre de décision (`decision_tree_classification`).

## Installation

DataLib peut être installé facilement via `pip` :

```bash
pip install datalib

Ou via Poetry :

.. code-block:: bash

   poetry add datalib
```

## Utilisation
-----------

Voici un exemple d'utilisation de la bibliothèque :

.. code-block:: python

   import pandas as pd
   from datalib.manipulation import read_csv, write_csv, fill_missing_values
   from datalib.data_statistics import calculate_mean, calculate_statistics
   from datalib.visualization import plot_histogram
   from datalib.analysis import linear_regression

   # Charger un dataset CSV
   file_path = 'path_to_your_data.csv'
   data = read_csv(file_path)

   # Remplir les valeurs manquantes
   data_filled = fill_missing_values(data)

   # Calculer la moyenne d'une colonne spécifique
   mean_value = calculate_mean(data_filled['column_name'])
   print(f"La moyenne de la colonne est : {mean_value}")

   # Calculer les statistiques pour toutes les colonnes numériques
   calculate_statistics(data_filled)

   # Visualisation des données
   plot_histogram(data_filled['column_name'], title="Histogramme de la colonne_name")

   # Régression linéaire
   X = data_filled[['feature1']]
   y = data_filled['target']
   model = linear_regression(X, y)
   print(f"Coefficients de la régression linéaire : {model.coef_}")

## Licence
-------

Ce projet est sous licence MIT - voir le fichier `LICENSE` pour plus de détails.

## Documentation complète 
La documentation complète de DataLib est disponible dans le dossier docs/, générée avec Sphinx.

## Contribuer
Les contributions à DataLib sont les bienvenues. Pour contribuer, suivez ces étapes :

Fork ce projet.
Créez une branche pour votre fonctionnalité (git checkout -b feature-name).
Committez vos changements (git commit -am 'Add feature').
Poussez la branche (git push origin feature-name).
Ouvrez une Pull Request.