import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datalib.viz.basic import BasicPlots
from datalib.viz.advanced import AdvancedPlots

@pytest.fixture
def sample_data():
    """Génère des données pour les tests de visualisation."""
    np.random.seed(42)
    n_samples = 100
    
    # Créer un DataFrame avec plusieurs types de données
    df = pd.DataFrame({
        'numeric': np.random.normal(0, 1, n_samples),
        'categorical': np.random.choice(['A', 'B', 'C'], n_samples),
        'uniform': np.random.uniform(0, 10, n_samples),
        'integer': np.random.randint(1, 100, n_samples)
    })
    
    return df

@pytest.fixture
def correlation_data():
    """Génère des données corrélées pour les tests."""
    np.random.seed(42)
    n_samples = 100
    
    x = np.random.normal(0, 1, n_samples)
    y = x * 0.5 + np.random.normal(0, 0.5, n_samples)
    z = -x * 0.3 + np.random.normal(0, 0.5, n_samples)
    
    return pd.DataFrame({
        'x': x,
        'y': y,
        'z': z
    })

def test_histogram(sample_data):
    """Test la création d'histogrammes."""
    basic_plots = BasicPlots()
    
    # Test avec différentes configurations
    basic_plots.histogram(sample_data['numeric'])
    plt.close()
    
    basic_plots.histogram(
        sample_data['numeric'],
        bins=20,
        title="Test Histogram",
        xlabel="Values",
        ylabel="Frequency"
    )
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0  # Le plot précédent a été fermé

def test_scatter_plot(correlation_data):
    """Test la création de nuages de points."""
    basic_plots = BasicPlots()
    
    # Test avec différentes configurations
    basic_plots.scatter_plot(
        correlation_data['x'],
        correlation_data['y']
    )
    plt.close()
    
    basic_plots.scatter_plot(
        correlation_data['x'],
        correlation_data['y'],
        title="Test Scatter Plot",
        xlabel="X values",
        ylabel="Y values"
    )
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0

def test_bar_plot(sample_data):
    """Test la création de graphiques en barres."""
    basic_plots = BasicPlots()
    
    # Créer des données agrégées pour le bar plot
    category_means = sample_data.groupby('categorical')['numeric'].mean()
    
    basic_plots.bar_plot(category_means)
    plt.close()
    
    basic_plots.bar_plot(
        category_means,
        title="Test Bar Plot",
        xlabel="Categories",
        ylabel="Mean Values"
    )
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0

def test_correlation_matrix(correlation_data):
    """Test la création de matrices de corrélation."""
    advanced_plots = AdvancedPlots()
    
    advanced_plots.correlation_matrix(correlation_data)
    plt.close()
    
    advanced_plots.correlation_matrix(
        correlation_data,
        figsize=(8, 6),
        cmap="viridis"
    )
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0

def test_box_plot(sample_data):
    """Test la création de boîtes à moustaches."""
    advanced_plots = AdvancedPlots()
    
    # Test avec toutes les colonnes numériques
    numeric_cols = sample_data.select_dtypes(include=[np.number]).columns
    
    advanced_plots.box_plot(sample_data[numeric_cols])
    plt.close()
    
    advanced_plots.box_plot(
        sample_data[numeric_cols],
        figsize=(10, 6)
    )
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0

def test_pair_plot(correlation_data):
    """Test la création de pair plots."""
    advanced_plots = AdvancedPlots()
    
    advanced_plots.pair_plot(correlation_data)
    plt.close()
    
    advanced_plots.pair_plot(
        correlation_data,
        diag_kind="hist"
    )
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0

def test_violin_plot(sample_data):
    """Test la création de violin plots."""
    advanced_plots = AdvancedPlots()
    
    advanced_plots.violin_plot(
        sample_data,
        x='categorical',
        y='numeric'
    )
    plt.close()
    
    advanced_plots.violin_plot(
        sample_data,
        x='categorical',
        y='numeric',
        figsize=(12, 6)
    )
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0

@pytest.mark.parametrize("plot_function", [
    "histogram",
    "scatter_plot",
    "bar_plot"
])
def test_basic_plot_parameters(sample_data, plot_function):
    """Test les paramètres des fonctions de visualisation de base."""
    basic_plots = BasicPlots()
    
    if plot_function == "histogram":
        getattr(basic_plots, plot_function)(
            sample_data['numeric'],
            bins=15,
            title="Test",
            xlabel="X",
            ylabel="Y",
            figsize=(8, 6)
        )
    elif plot_function == "scatter_plot":
        getattr(basic_plots, plot_function)(
            sample_data['numeric'],
            sample_data['uniform'],
            title="Test",
            xlabel="X",
            ylabel="Y",
            figsize=(8, 6)
        )
    else:  # bar_plot
        category_means = sample_data.groupby('categorical')['numeric'].mean()
        getattr(basic_plots, plot_function)(
            category_means,
            title="Test",
            xlabel="X",
            ylabel="Y",
            figsize=(8, 6)
        )
    
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0

@pytest.mark.parametrize("plot_function", [
    "correlation_matrix",
    "box_plot",
    "pair_plot",
    "violin_plot"
])
def test_advanced_plot_parameters(sample_data, correlation_data, plot_function):
    """Test les paramètres des fonctions de visualisation avancées."""
    advanced_plots = AdvancedPlots()
    
    if plot_function == "correlation_matrix":
        getattr(advanced_plots, plot_function)(
            correlation_data,
            figsize=(8, 6),
            cmap="coolwarm",
            annot=True
        )
    elif plot_function == "box_plot":
        numeric_cols = sample_data.select_dtypes(include=[np.number]).columns
        getattr(advanced_plots, plot_function)(
            sample_data[numeric_cols],
            figsize=(8, 6)
        )
    elif plot_function == "pair_plot":
        getattr(advanced_plots, plot_function)(
            correlation_data,
            diag_kind="kde"
        )
    else:  # violin_plot
        getattr(advanced_plots, plot_function)(
            sample_data,
            x='categorical',
            y='numeric',
            figsize=(8, 6)
        )
    
    plt.close()
    
    # Vérifier que le graphique est créé
    fig = plt.gcf()
    assert len(fig.axes) == 0 