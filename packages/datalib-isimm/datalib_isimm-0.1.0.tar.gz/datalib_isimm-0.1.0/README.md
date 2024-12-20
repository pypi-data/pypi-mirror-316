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
  - Modèles de régression
  - Classification supervisée
  - Méthodes non supervisées

## Exemple d'utilisation

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

