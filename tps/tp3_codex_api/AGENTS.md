# TP3 — projet d'exercice pour Codex

Ces consignes concernent le travail sur le projet pendant le TP.

- Référence métier des notes de frais : SPEC.md. Pour le catalogue : docstrings et modèles de catalogue.py.
- Lire les fichiers utiles, reproduire les problèmes, puis faire des changements ciblés dans les fichiers demandés.
- Ne pas consulter corrige/ pendant l'exercice ; ne pas modifier les tests fournis, SPEC.md ni les jeux de données pour faire passer les tests.
- Python 3.12 ou plus ; pas de nouvelle dépendance. Bibliothèque standard pour les notes de frais ; openai et pydantic déjà installés pour le catalogue.
- Environnement commun préparé avec uv sync à la racine de la copie complète de la formation.
- Depuis le dossier du TP : uv run pytest -q test_acceptation_tp3.py pour les notes de frais ; uv run pytest -q test_api_catalogue.py pour le catalogue ; uv run pytest -q pour le bilan.
- Vérifier les attentes des nouveaux tests dans SPEC.md, pas dans l'implémentation.
- Docstrings en français ; documenter uniquement les commandes et comportements vérifiés.
- Les tests du catalogue utilisent un client simulé. Ne pas lancer d'appel réel à l'API et ne pas lire de clé ; l'apprenant effectue l'essai réel dans son terminal avec la clé de formation.
- Terminer chaque modification par un résumé des fichiers changés et des commandes réellement exécutées avec leurs résultats. Signaler un test non exécuté.
