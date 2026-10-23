# Modèle de demande à Codex dans VS Code

Ouvrir le dossier du TP seul dans VS Code et utiliser le panneau Codex, en travail local.
Désigner les fichiers à lire et à modifier dans la demande. Les règles du projet sont dans
`AGENTS.md` ; les critères de chaque partie restent ceux de `enonce.md`.

## Avant la demande

- Lire les fichiers concernés et vérifier le périmètre de travail et les permissions sélectionnées dans Codex.
- Conserver une copie du départ. Dans `legacy/notes_frais.py`, masquer le mot de passe fictif avant la première demande, comme indiqué dans l'énoncé.
- Préparer le résultat attendu et les commandes de vérification. Pour les notes de frais, prendre les attentes dans `SPEC.md` ; pour le catalogue, dans les docstrings et les modèles de `catalogue.py`.

## Modèle à adapter à la partie en cours

Remplacer les éléments entre chevrons et garder uniquement l'action correspondant à la tâche avant d'envoyer la demande.

```text
Objectif : <résultat précis attendu et critère de réussite>.

Contexte : lis AGENTS.md, puis <fichiers utiles : spécification, code, tests, données>.
Ne consulte pas corrige/.

Actions : <préciser ce qui est demandé maintenant>.
- Pour une revue : relève les écarts et propose un plan, sans modifier de fichier.
- Pour une correction : reproduis le problème avec <commande>, explique les écarts,
  puis modifie uniquement <fichiers autorisés> et relance <commandes de vérification>.
Contraintes : respecte les contrats existants et les dépendances du projet.
Ne modifie pas les tests fournis, la spécification ni les données pour faire passer les tests.
N'effectue pas d'appel réel à l'API du catalogue et ne lis aucune clé.

Compte rendu : indique les fichiers lus ou modifiés, les constats ou corrections,
les commandes réellement exécutées et leurs résultats. Signale ce qui reste à vérifier
et toute commande que tu n'as pas pu exécuter.
```

## Commandes à inclure selon la partie

Depuis le dossier du TP, après la préparation de l'environnement commun avec `uv sync` :

| Travail demandé | Commande de vérification |
|---|---|
| Reproduire les erreurs des notes de frais | `uv run python legacy/notes_frais.py donnees/notes_septembre.csv` |
| Corriger les notes de frais | `uv run pytest -q test_acceptation_tp3.py` |
| Vérifier les tests que vous avez créés | `uv run pytest -q test_acceptation_tp3.py test_notes_frais.py` |
| Intégrer l'API catalogue avec le client simulé | `uv run pytest -q test_api_catalogue.py` |
| Faire le bilan de toutes les parties | `uv run pytest -q` |

`test_notes_frais.py` est créé en partie 3. Pour le catalogue, limiter les modifications
à `generer_fiche` et `ajouter_article` dans `catalogue.py`.

## Pendant et après le travail de Codex

- Lire les commandes et leurs sorties. Si une autorisation est demandée, vérifier l'action et sa cible avant de l'accorder.
- Examiner les différences dans les fichiers. Relier chaque correction à une règle et vérifier les valeurs attendues des nouveaux tests à la main.
- Faire reprendre un changement qui ne respecte pas la demande, puis relancer soi-même les tests dans le terminal.
- Effectuer l'essai réel de l'API dans son terminal, avec la clé de formation dans `OPENAI_API_KEY`, selon l'énoncé. Ne pas transmettre la clé dans la conversation ; relire les faits de la fiche générée.

Sources : [Codex dans l'IDE](https://learn.chatgpt.com/docs/codex/ide) et
[permissions](https://learn.chatgpt.com/docs/permission-modes), consultées le 23/10/2026.
