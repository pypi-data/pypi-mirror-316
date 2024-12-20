import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
import pandas as pd
import numpy as np
from datalib.data.loader import DataLoader
from datalib.data.transformer import DataTransformer

def test_csv_loading():
    """Test le chargement d'un fichier CSV."""
    # Créer un DataFrame de test
    test_data = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['a', 'b', 'c']
    })
    
    # Sauvegarder en CSV
    test_file = "test_data.csv"
    test_data.to_csv(test_file, index=False)
    
    # Charger avec DataLoader
    loader = DataLoader()
    loaded_data = loader.read_csv(test_file)
    
    # Vérifier que les données sont correctement chargées
    pd.testing.assert_frame_equal(test_data, loaded_data)
    
def test_data_normalization():
    """Test la normalisation des données."""
    # Créer des données de test
    test_data = pd.Series([1, 2, 3, 4, 5])
    transformer = DataTransformer()
    
    # Test normalisation z-score
    normalized_zscore = transformer.normalize(test_data, method="zscore")
    assert abs(normalized_zscore.mean()) < 1e-10  # Moyenne proche de 0
    assert abs(normalized_zscore.std() - 1.0) < 1e-10  # Écart-type proche de 1
    
    # Test normalisation min-max
    normalized_minmax = transformer.normalize(test_data, method="minmax")
    assert normalized_minmax.min() == 0  # Minimum doit être 0
    assert normalized_minmax.max() == 1  # Maximum doit être 1
    
def test_missing_values_handling():
    """Test la gestion des valeurs manquantes."""
    # Créer des données de test avec valeurs manquantes
    test_data = pd.DataFrame({
        'A': [1, np.nan, 3, np.nan, 5],
        'B': [np.nan, 2, 3, 4, 5]
    })
    
    transformer = DataTransformer()
    
    # Test remplacement par la moyenne
    filled_mean = transformer.handle_missing_values(test_data, strategy="mean")
    assert not filled_mean.isna().any().any()  # Pas de valeurs manquantes
    
    # Test suppression des lignes avec valeurs manquantes
    filled_drop = transformer.handle_missing_values(test_data, strategy="drop")
    assert not filled_drop.isna().any().any()  # Pas de valeurs manquantes
    assert len(filled_drop) < len(test_data)  # Nombre de lignes réduit 