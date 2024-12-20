import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression
from datalib.ml.supervised import SupervisedModels
from datalib.ml.unsupervised import UnsupervisedModels

@pytest.fixture
def regression_data():
    """Génère des données pour les tests de régression."""
    X, y = make_regression(
        n_samples=100,
        n_features=3,
        noise=0.1,
        random_state=42
    )
    return pd.DataFrame(X, columns=[f'feature_{i}' for i in range(3)]), pd.Series(y)

@pytest.fixture
def classification_data():
    """Génère des données pour les tests de classification."""
    X, y = make_classification(
        n_samples=100,
        n_features=4,
        n_classes=3,
        n_clusters_per_class=1,
        random_state=42
    )
    return pd.DataFrame(X, columns=[f'feature_{i}' for i in range(4)]), pd.Series(y)

def test_linear_regression(regression_data):
    """Test la régression linéaire."""
    X, y = regression_data
    results = SupervisedModels.linear_regression(X, y)
    
    assert 'model' in results
    assert 'mse' in results
    assert 'r2' in results
    assert results['r2'] > 0  # Le R² devrait être positif
    assert isinstance(results['coefficients'], pd.Series)
    assert len(results['coefficients']) == X.shape[1]

def test_ridge_regression(regression_data):
    """Test la régression Ridge."""
    X, y = regression_data
    results = SupervisedModels.ridge_regression(X, y, alpha=1.0)
    
    assert 'model' in results
    assert 'mse' in results
    assert 'mae' in results
    assert 'r2' in results
    assert results['r2'] > 0
    assert isinstance(results['coefficients'], pd.Series)
    assert len(results['coefficients']) == X.shape[1]

def test_random_forest_classifier(classification_data):
    """Test le Random Forest Classifier."""
    X, y = classification_data
    results = SupervisedModels.random_forest_classifier(
        X, y,
        n_estimators=10,
        max_depth=5
    )
    
    assert 'model' in results
    assert 'accuracy' in results
    assert 'confusion_matrix' in results
    assert 'classification_report' in results
    assert results['accuracy'] > 0
    assert isinstance(results['feature_importance'], pd.Series)
    assert len(results['feature_importance']) == X.shape[1]

def test_knn_classifier(classification_data):
    """Test le k-NN Classifier."""
    X, y = classification_data
    results = SupervisedModels.knn_classifier(X, y, n_neighbors=3)
    
    assert 'model' in results
    assert 'accuracy' in results
    assert 'classification_report' in results
    assert results['accuracy'] > 0

def test_evaluate_regression(regression_data):
    """Test l'évaluation des modèles de régression."""
    X, y = regression_data
    model = SupervisedModels.linear_regression(X, y)['model']
    results = SupervisedModels.evaluate_regression(model, X, y, cv=3)
    
    assert 'mse_scores' in results
    assert 'mae_scores' in results
    assert 'r2_scores' in results
    assert len(results['r2_scores']) == 3
    assert results['mean_r2'] > 0

def test_evaluate_classifier(classification_data):
    """Test l'évaluation des modèles de classification."""
    X, y = classification_data
    model = SupervisedModels.random_forest_classifier(X, y)['model']
    results = SupervisedModels.evaluate_classifier(model, X, y, cv=3)
    
    assert 'accuracy_scores' in results
    assert 'precision_scores' in results
    assert 'recall_scores' in results
    assert 'f1_scores' in results
    assert len(results['accuracy_scores']) == 3
    assert results['mean_accuracy'] > 0

def test_kmeans_clustering(classification_data):
    """Test le clustering K-means."""
    X, _ = classification_data
    results = UnsupervisedModels.kmeans_clustering(X, n_clusters=3)
    
    assert 'model' in results
    assert 'labels' in results
    assert 'centroids' in results
    assert 'inertia' in results
    assert len(np.unique(results['labels'])) == 3
    assert isinstance(results['centroids'], pd.DataFrame)
    assert results['centroids'].shape == (3, X.shape[1])

def test_dbscan_clustering(classification_data):
    """Test le clustering DBSCAN."""
    X, _ = classification_data
    results = UnsupervisedModels.dbscan_clustering(X, eps=0.5, min_samples=5)
    
    assert 'model' in results
    assert 'labels' in results
    assert 'n_clusters' in results
    assert 'n_noise' in results
    assert isinstance(results['n_clusters'], int)
    assert isinstance(results['n_noise'], int)

def test_pca_analysis(classification_data):
    """Test l'analyse en composantes principales."""
    X, _ = classification_data
    results = UnsupervisedModels.pca_analysis(X, n_components=2)
    
    assert 'model' in results
    assert 'components' in results
    assert 'explained_variance_ratio' in results
    assert isinstance(results['components'], pd.DataFrame)
    assert results['components'].shape == (len(X), 2)
    assert len(results['explained_variance_ratio']) == 2

def test_evaluate_clustering(classification_data):
    """Test l'évaluation du clustering."""
    X, _ = classification_data
    kmeans_results = UnsupervisedModels.kmeans_clustering(X, n_clusters=3)
    results = UnsupervisedModels.evaluate_clustering(X, kmeans_results['labels'])
    
    assert 'silhouette_score' in results
    assert 'calinski_harabasz_score' in results
    assert -1 <= results['silhouette_score'] <= 1
    assert results['calinski_harabasz_score'] >= 0

def test_find_optimal_components(classification_data):
    """Test la recherche du nombre optimal de composantes PCA."""
    X, _ = classification_data
    results = UnsupervisedModels.find_optimal_components(
        X,
        explained_variance_threshold=0.95
    )
    
    assert 'n_components_95' in results
    assert 'explained_variance_ratio' in results
    assert 'cumulative_variance_ratio' in results
    assert isinstance(results['n_components_95'], int)
    assert results['n_components_95'] > 0
    assert results['n_components_95'] <= X.shape[1] 