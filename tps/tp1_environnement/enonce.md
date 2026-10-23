# TP1 : environnement et premières complétions

**Durée** : 25 min. **Partie** : P1 (découverte et installation).

## Objectif

Configurer les outils, puis faire écrire trois fonctions à Copilot. Savoir préciser une demande et vérifier la proposition obtenue.

## Prérequis

- Démo 1 ; VS Code récent, Python 3.12 ou plus, uv, comptes GitHub et ChatGPT.
- Conserver la copie complète du dépôt ; ouvrir `tps/tp1_environnement/` seul dans VS Code.
- Utiliser uniquement les fichiers fictifs fournis. Ne pas modifier `test_premiers_pas.py`.

## Partie 1 — Préparer les outils (10 min)

1. Activer Copilot depuis la barre d'état (**Use AI Features**) et se connecter à GitHub. Vérifier l'allocation disponible dans son tableau de bord.
2. Depuis **Preferences: Open User Settings (JSON)**, lire `settings_recommandes.jsonc` et reporter les réglages utiles.
3. Dans ChatGPT, repérer **Settings > Data controls > Improve the model for everyone** et le chat temporaire, selon les règles de votre entreprise.
4. Lancer `uv sync` à la racine du dépôt, puis, dans le dossier du TP, `uv run pytest -q`. Les 18 tests doivent être collectés ; les fonctions sont encore à compléter.

## Partie 2 — Guider les complétions (10 min)

1. Ouvrir `premiers_pas.py`. Pour `est_palindrome`, `formater_euros` et `est_email_valide`, supprimer `raise NotImplementedError`, laisser Copilot proposer le corps et relire avant d'accepter avec `Tab`.
2. Lancer `uv run pytest -q` après chaque fonction. En cas d'échec, préciser la docstring avec le résultat attendu, puis demander une nouvelle proposition.
3. Conserver une consigne que vous avez précisée et expliquer son effet.

Exemple de contexte à donner à Copilot si le format des euros pose problème :

```python
# Exemples du contrat :
# formater_euros(1234.5) == "1 234,50 EUR"
# formater_euros(999.999) == "1 000,00 EUR"
# Indice Python : f"{1234.5:,.2f}" produit "1,234.50".
# Adapter les séparateurs au format demandé après l'arrondi.
```

Ce bloc aide à formuler la demande. Faire proposer l'implémentation par Copilot, puis la vérifier avec les tests.

## Partie 3 — Comparer avec ChatGPT (3 min)

Coller `formater_euros` avec sa docstring et demander :

> Explique cette fonction et propose trois cas de test supplémentaires. Justifie chaque résultat attendu avec la docstring.

Vérifier un cas proposé à la main. Noter une différence avec Copilot dans l'éditeur.

## Partie 4 — Vérifier et expliquer (2 min)

Lancer `uv run pytest -q`. Montrer une consigne utilisée et le test qui vérifie le résultat.

## Critères de réussite

- Les 18 tests passent, sans modification du fichier de tests.
- Les trois fonctions ont été proposées par Copilot et relues.
- Vous pouvez expliquer comment une signature, une docstring ou un exemple a guidé la proposition.

## Corrigé

`corrige/premiers_pas.py` et `corrige/prompts_types.md`. Une autre implémentation qui respecte le contrat et passe les tests est valable.
