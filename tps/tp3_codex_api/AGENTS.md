# AGENTS.md : notes de frais et catalogue de boutique

## Projet
Python 3.13 . Deux volets :
- Notes de frais : legacy/notes_frais.py, bibliothèque standard uniquement. Référence métier : SPEC.md.
- Catalogue : catalogue.py, avec openai et pydantic (déjà installés). Référence : docstrings et modèles de catalogue.py.

## Commandes
- Préférer uv ; environnement commun préparé avec uv sync à la racine de la copie complète de la formation.
- Tests, depuis le dossier du TP :
  - notes de frais : uv run pytest -q test_acceptation_tp3.py ;
  - catalogue : uv run pytest -q test_api_catalogue.py ;
  - bilan : uv run pytest -q.

## Conventions
- Lire les fichiers utiles et reproduire le problème avant de corriger ; changements ciblés, dans les fichiers demandés uniquement.
- Ne pas ajouter de dépendance.
- Docstrings en français ; documenter uniquement les commandes et comportements vérifiés.
- Ne pas consulter corrige/ pendant l'exercice.
- Terminer chaque modification par un résumé : fichiers changés, commandes réellement exécutées avec leurs résultats, tests non exécutés.

## Tests
- Valeurs attendues tirées de la référence (SPEC.md, docstrings de catalogue.py), jamais de l'implémentation.
- Ne jamais modifier les tests fournis, SPEC.md ni les jeux de données pour faire passer les tests.
- Les tests du catalogue utilisent un client simulé : aucun appel réel à l'API, aucune lecture de clé. L'apprenant fait l'essai réel dans son terminal avec la clé de formation.
