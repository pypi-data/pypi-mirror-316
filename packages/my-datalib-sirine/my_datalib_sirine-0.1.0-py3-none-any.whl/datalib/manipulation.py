import pandas as pd

def read_csv(file_path):
    """
    Lit un fichier CSV et retourne un DataFrame.
    
    Parameters:
        file_path (str): Le chemin du fichier CSV à lire.
    
    Returns:
        pd.DataFrame: Le contenu du fichier CSV sous forme de DataFrame.
    
    Raises:
        ValueError: Si une erreur se produit lors de la lecture du fichier.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier CSV : {e}")

def write_csv(data, file_path):
    """
    Écrit un DataFrame dans un fichier CSV.
    
    Parameters:
        data (pd.DataFrame): Le DataFrame à écrire dans le fichier.
        file_path (str): Le chemin où enregistrer le fichier CSV.
    
    Raises:
        ValueError: Si une erreur se produit lors de l'écriture du fichier.
    """
    try:
        data.to_csv(file_path, index=False)
    except Exception as e:
        raise ValueError(f"Erreur lors de l'écriture dans le fichier CSV : {e}")

def fill_missing_values(data, method="mean"):
    """
    Remplit les valeurs manquantes d'un DataFrame.
    
    Parameters:
        data (pd.DataFrame): Le DataFrame contenant les valeurs manquantes.
        method (str): La méthode utilisée pour remplir les valeurs manquantes. Peut être "mean", "median", ou "mode".
                      La valeur par défaut est "mean".
    
    Returns:
        pd.DataFrame: Le DataFrame avec les valeurs manquantes remplies.
    
    Raises:
        ValueError: Si la méthode spécifiée n'est pas supportée.
    """
    if method == "mean":
        return data.fillna(data.mean())
    elif method == "median":
        return data.fillna(data.median())
    elif method == "mode":
        return data.fillna(data.mode().iloc[0])
    else:
        raise ValueError("Méthode non supportée : choisissez 'mean', 'median', ou 'mode'.")
