# AGENTS.md : comparaison de numéros de version

## Projet
Python 3.12, bibliothèque standard uniquement. Module : versions.py.
Les versions suivent la gestion sémantique de version (semver.org) : MAJEUR.MINEUR.CORRECTIF.

## Commandes
- Préférer uv ; environnement commun préparé avec uv sync à la racine de la copie complète du dépôt.
- Tests : uv run pytest -q, après chaque modification.

## Conventions
- Noms en français, snake_case ; docstring en français sur chaque fonction publique, avec les exceptions levées.
- Ne pas ajouter de dépendance (pas de bibliothèque packaging) : l'outil doit tourner sur un Python nu.

## Tests
- Valeurs attendues tirées des docstrings et de semver.org, jamais du code actuel.
- Ne jamais modifier un test existant pour le faire passer.
