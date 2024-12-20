# Stat Analysis

`stat_analysis` est un package Python pour l'analyse statistique univariée avancée. Il permet de réaliser des analyses statistiques détaillées et de générer des visualisations pour les variables numériques et catégorielles.

## Installation

Installez le package en utilisant la commande suivante :

```bash
pip install stat_analysis
```

## Utilisation

Voici un exemple d'utilisation du package :

```python
import pandas as pd
from stat_analysis.advanced_univariate_stat import AdvancedUnivariateStat
from stat_analysis.configuration import ConfigurationPlot

# Création d'un DataFrame exemple
data = {
    'numerique': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'categorielle': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']
}
df = pd.DataFrame(data)

# Configuration des paramètres de visualisation
config = ConfigurationPlot(theme_plotly="plotly_dark", theme_seaborn="darkgrid")

# Création de l'objet d'analyse
stat = AdvancedUnivariateStat(config)

# Analyse statistique avancée
resultats = stat.analyse_statistique_avancee(df, colonnes=['numerique', 'categorielle'], afficher_plots=True)
```

## Fonctionnalités

- **Analyse statistique descriptive** : Moyennes, médianes, écart-types, etc.
- **Tests de normalité** : Vérifiez si vos données suivent une distribution normale.
- **Calcul des intervalles de confiance** : Obtenez des estimations robustes de vos données.
- **Visualisations** : Graphiques interactifs avec Plotly et esthétiques avec Seaborn.

## Contribution

Les contributions sont les bienvenues !

1. Ouvrez une issue pour discuter de vos idées d'amélioration ou signaler des bugs.
2. Faites un fork du dépôt.
3. Apportez vos modifications et soumettez une pull request.

Nous serons ravis de collaborer avec vous !
# stat_analysis
