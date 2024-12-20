import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Régression linéaire
def linear_regression(X, y):
    """
    Applique une régression linéaire sur les données fournies.
    
    Parameters:
        X (array-like): Les caractéristiques d'entrée.
        y (array-like): Les cibles à prédire.
    
    Returns:
        LinearRegression: Le modèle de régression linéaire ajusté.
    """
    model = LinearRegression()
    model.fit(X, y)
    return model

# Régression polynomiale
def polynomial_regression(X, y, degree=2):
    """
    Applique une régression polynomiale sur les données fournies.
    
    Parameters:
        X (array-like): Les caractéristiques d'entrée.
        y (array-like): Les cibles à prédire.
        degree (int, optional): Le degré du polynôme. Par défaut 2.
    
    Returns:
        tuple: Le modèle de régression polynomiale et l'instance de PolynomialFeatures.
    """
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)
    return model, poly

# k-means clustering
def kmeans_clustering(X, n_clusters=3):
    """
    Applique l'algorithme de clustering k-means sur les données fournies.
    
    Parameters:
        X (array-like): Les données à regrouper.
        n_clusters (int, optional): Le nombre de clusters à générer. Par défaut 3.
    
    Returns:
        KMeans: Le modèle de clustering k-means ajusté.
    """
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    return kmeans

# PCA
def pca_analysis(X, n_components=2):
    """
    Applique une analyse en composantes principales (PCA) sur les données.
    
    Parameters:
        X (array-like): Les données à transformer.
        n_components (int, optional): Le nombre de composantes principales. Par défaut 2.
    
    Returns:
        tuple: Le modèle PCA ajusté et les données transformées.
    """
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    return pca, X_pca

# k-NN Classification
def knn_classification(X_train, y_train, n_neighbors=5):
    """
    Applique un classificateur k-plus proches voisins (k-NN) sur les données d'entraînement.
    
    Parameters:
        X_train (array-like): Les caractéristiques d'entraînement.
        y_train (array-like): Les cibles d'entraînement.
        n_neighbors (int, optional): Le nombre de voisins à considérer pour la classification. Par défaut 5.
    
    Returns:
        KNeighborsClassifier: Le modèle k-NN ajusté.
    """
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X_train, y_train)
    return knn

# Decision Tree Classification
def decision_tree_classification(X_train, y_train):
    """
    Applique un classificateur arbre de décision sur les données d'entraînement.
    
    Parameters:
        X_train (array-like): Les caractéristiques d'entraînement.
        y_train (array-like): Les cibles d'entraînement.
    
    Returns:
        DecisionTreeClassifier: Le modèle d'arbre de décision ajusté.
    """
    tree = DecisionTreeClassifier()
    tree.fit(X_train, y_train)
    return tree
