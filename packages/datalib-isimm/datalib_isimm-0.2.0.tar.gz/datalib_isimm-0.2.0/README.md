# DataLib

DataLib est une bibliothèque Python conçue pour simplifier la manipulation et l'analyse de données.

## Installation

```bash
pip install datalib
```

## Fonctionnalités principales

- Manipulation de données
  - Chargement et traitement des fichiers CSV
  - Transformation des données (normalisation, gestion des valeurs manquantes)
- Statistiques
  - Calculs statistiques de base (moyenne, médiane, mode, écart-type)
  - Tests statistiques simples
- Visualisation
  - Graphiques simples (barres, histogrammes, nuages de points)
  - Visualisations avancées (matrices de corrélation)
- Analyse avancée
  - Modèles de régression (linéaire, Ridge)
  - Classification supervisée (k-NN, Random Forest)
  - Méthodes non supervisées (k-means, DBSCAN, PCA)

## Exemples d'utilisation

### Manipulation de données

```python
from datalib.data import loader, transformer
from datalib.stats import basic
from datalib.viz import basic as viz

# Charger des données
data_loader = loader.DataLoader()
df = data_loader.read_csv("donnees.csv")

# Transformer les données
data_transformer = transformer.DataTransformer()
df_normalized = data_transformer.normalize(df["colonne"])
df_clean = data_transformer.handle_missing_values(df)

# Calculer des statistiques
stats = basic.BasicStats()
moyenne = stats.mean(df["colonne"])
correlation = stats.correlation(df["colonne1"], df["colonne2"])

# Créer des visualisations
plots = viz.BasicPlots()
plots.histogram(df["colonne"], title="Distribution des valeurs")
plots.scatter_plot(df["colonne1"], df["colonne2"], title="Relation entre variables")
```

### Apprentissage supervisé

```python
from datalib.ml.supervised import SupervisedModels

# Régression linéaire
reg_model = SupervisedModels.linear_regression(X, y)
print(f"R² Score: {reg_model['r2']}")
print(f"Coefficients: {reg_model['coefficients']}")

# Classification avec Random Forest
rf_model = SupervisedModels.random_forest_classifier(
    X, y,
    n_estimators=100,
    max_depth=5
)
print(f"Accuracy: {rf_model['accuracy']}")
print("Classification Report:")
print(rf_model['classification_report'])

# Évaluation avec validation croisée
eval_results = SupervisedModels.evaluate_classifier(
    rf_model['model'],
    X, y,
    cv=5
)
print(f"Mean CV Accuracy: {eval_results['mean_accuracy']}")
print(f"Mean CV F1-Score: {eval_results['mean_f1']}")
```

### Apprentissage non supervisé

```python
from datalib.ml.unsupervised import UnsupervisedModels

# Clustering K-means
kmeans_results = UnsupervisedModels.kmeans_clustering(
    X,
    n_clusters=3
)
print(f"Inertia: {kmeans_results['inertia']}")
print("Cluster Labels:", kmeans_results['labels'])

# Analyse en composantes principales (PCA)
pca_results = UnsupervisedModels.pca_analysis(
    X,
    n_components=2
)
print("Variance expliquée:", pca_results['explained_variance_ratio'])

# Clustering DBSCAN
dbscan_results = UnsupervisedModels.dbscan_clustering(
    X,
    eps=0.5,
    min_samples=5
)
print(f"Nombre de clusters: {dbscan_results['n_clusters']}")
print(f"Points de bruit: {dbscan_results['n_noise']}")

# Évaluation du clustering
eval_scores = UnsupervisedModels.evaluate_clustering(
    X,
    kmeans_results['labels']
)
print(f"Score de silhouette: {eval_scores['silhouette_score']}")
```

## Documentation

La documentation complète est disponible sur [Read the Docs](https://datalib.readthedocs.io/).

## Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

## Tests

Pour exécuter les tests :

```bash
pytest tests/
```

## Licence

Ce projet est sous licence MIT.

