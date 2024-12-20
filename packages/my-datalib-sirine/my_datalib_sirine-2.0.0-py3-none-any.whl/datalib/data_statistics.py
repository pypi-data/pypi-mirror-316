import numpy as np
from scipy import stats
from scipy.stats import mode

def calculate_mean(data):
    """
    Calcule la moyenne des données.
    
    Parameters:
        data (array-like): Les données dont la moyenne doit être calculée.
    
    Returns:
        float: La moyenne des données.
    """
    return np.mean(data)

def calculate_median(data):
    """
    Calcule la médiane des données.
    
    Parameters:
        data (array-like): Les données dont la médiane doit être calculée.
    
    Returns:
        float: La médiane des données.
    """
    return np.median(data)

def calculate_mode(data):
    """
    Calcule le mode des données.
    
    Parameters:
        data (array-like): Les données dont le mode doit être calculé.
    
    Returns:
        float or None: Le mode des données, ou None si aucun mode n'est trouvé.
    """
    mode_result = stats.mode(data)
    
    # Si mode_result.mode contient des éléments
    if isinstance(mode_result.mode, np.ndarray) and mode_result.mode.size > 0:
        # Si la fréquence du mode est 1 pour tous les éléments, il n'y a pas de mode
        if mode_result.count[0] == 1:  # Fréquence du mode
            return None
        return mode_result.mode[0]  # Retourne le premier mode trouvé
    elif isinstance(mode_result.mode, np.ndarray) and mode_result.mode.size == 0:
        return None  # Aucun mode trouvé
    
    # Si mode_result.mode est un scalaire (cas peu probable, mais à vérifier)
    return mode_result.mode if mode_result.mode != 0 else None

def calculate_std(data):
    """
    Calcule l'écart-type des données.
    
    Parameters:
        data (array-like): Les données dont l'écart-type doit être calculé.
    
    Returns:
        float: L'écart-type des données.
    """
    return np.std(data)

def calculate_correlation(data1, data2):
    """
    Calcule la corrélation entre deux séries de données.
    
    Parameters:
        data1 (array-like): La première série de données.
        data2 (array-like): La deuxième série de données.
    
    Returns:
        float: La corrélation entre les deux séries de données.
    """
    return np.corrcoef(data1, data2)[0, 1]

def calculate_statistics(dataframe):
    """
    Calcule automatiquement les statistiques pour toutes les colonnes numériques d'un DataFrame.
    
    Parameters:
        dataframe (pandas.DataFrame): Le DataFrame contenant les données à analyser.
    
    Returns:
        None: Affiche les statistiques pour chaque colonne numérique du DataFrame.
    """
    numeric_columns = dataframe.select_dtypes(include=[np.number])  # Select only numeric columns
    for column in numeric_columns.columns:
        print(f"=== Statistics for '{column}' ===")
        print(f"Mean: {calculate_mean(numeric_columns[column])}")
        print(f"Median: {calculate_median(numeric_columns[column])}")
        print(f"Mode: {calculate_mode(numeric_columns[column])}")
        print(f"Standard Deviation: {calculate_std(numeric_columns[column])}")
        print()
