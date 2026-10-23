# Formation PLB « GitHub Copilot et ChatGPT »

Ce dossier contient le code des démonstrations faites par le formateur et des quatre TP que vous réaliserez pendant la journée.

## Contenu

```
demos/           code des 5 démonstrations du formateur
tps/             4 TP : énoncé (enonce.md et enonce.pdf), code de départ, tests fournis
```

| Heure | Séquence | Dossier |
|---|---|---|
| 9h35 | Démo 1 — Installer Copilot, premières complétions | `demos/demo1_premiers_pas/` |
| 9h45 | TP1 — Environnement et premières complétions (25 min) | `tps/tp1_environnement/` |
| 11h00 | Démo 2 — Bug, tests, refactoring avec Copilot | `demos/demo2_copilot_avance/` |
| 11h15 | TP2 — Module de réservation de salles (65 min) | `tps/tp2_module_reservations/` |
| 13h37 | Démo 3 — Codex dans VS Code | `demos/demo3_codex_vscode/` |
| 14h03 | Démo 4 — ChatGPT pour le code, API pour le support | `demos/demo4_chatgpt_api/` |
| 14h15 | TP3 — Développer avec Codex et intégrer l'API au catalogue (50 min) | `tps/tp3_codex_api/` |
| 15h30 | Démo 5 — Un outil de bout en bout avec les deux outils | `demos/demo5_projet_combine/` |
| 15h40 | TP4 — Générateur de changelog et charte d'usage (60 min) | `tps/tp4_projet_complet/` |

## Environnement

À installer avant la formation : VS Code récent avec GitHub Copilot (compte GitHub), un compte ChatGPT (vérifier l'accès à Codex dans la surface utilisée), Python 3.12 ou plus, Git et [uv](https://docs.astral.sh/uv/getting-started/installation/).

À la racine du dossier, préparer l'environnement une seule fois :

```bash
uv sync
```

Conserver l'arborescence complète, avec `pyproject.toml` et `uv.lock` à la racine.
Ouvrir ensuite le dossier du TP seul dans VS Code, et placer le terminal
dans ce dossier. Les commandes suivantes utilisent l'environnement du projet :

```bash
uv run pytest -q
uv run python nom_du_script.py
```

`nom_du_script.py` est à remplacer par le fichier indiqué dans l'énoncé. Aucun `uv init`
n'est nécessaire dans les sous-dossiers.

Si uv n'est pas disponible : dans un environnement virtuel Python déjà activé,
installer `python -m pip install -r requirements.txt` depuis la racine. Dans les consignes,
remplacer `uv run python` par `python` et `uv run pytest` par `python -m pytest`.

Chaque TP utilise ainsi son `AGENTS.md` et ses fichiers `.github/`.
Conserver les fichiers `pytest.ini` de chaque TP.

Pour la partie 4 du TP4, choisir la cible **Local** dans la Chat view avant les commandes de prompt.
Le TP4 utilise le fichier `commits.txt` fourni ; aucun commit Git n'est nécessaire.

## Clé d'API OpenAI

Pour la partie API de l'après-midi, le formateur fournit une clé de projet à budget plafonné, révoquée en fin de journée. Elle se lit dans la variable `OPENAI_API_KEY`, à définir dans le terminal qui lance la commande :

```bash
# macOS / Linux : remplacer la valeur par la clé fournie
export OPENAI_API_KEY="cle-fournie-par-le-formateur"
```

Sous Windows PowerShell : `$env:OPENAI_API_KEY="cle-fournie-par-le-formateur"`.
Ne jamais enregistrer cette clé dans un fichier.

Le modèle utilisé par défaut est `gpt-6-luna` ; la variable `OPENAI_MODEL` permet d'en choisir un autre.

## Les quatre TP

Chaque TP suit un seul parcours découpé en parties. Les blocs d'aide de l'énoncé donnent
un exemple pour les passages techniques. Faites relire et expliquer chaque proposition de l'IA,
puis vérifiez-la avec les tests fournis.

| TP | Parties | Durée | Tests fournis |
|---|---|---|---|
| TP1 | Environnement, trois complétions, comparaison ChatGPT, vérification | 25 min | 18 |
| TP2 | Complétions, tests, bug, refactoring, AGENTS.md, import CSV | 65 min | 19 |
| TP3 | Codex : lecture, corrections, tests, documentation, intégration de l'API catalogue, bilan | 50 min | 15 |
| TP4 | Spécification, AGENTS.md, implémentation, fichier de prompt, charte, bilan | 60 min | 13 |

Dans le TP3, Codex travaille dans le projet : il lit les fichiers, applique des corrections et
exécute les tests. Vous contrôlez les différences et relancez les commandes. L'API sert à générer
la fiche d'un nouvel article de la boutique, en préservant les fiches existantes ; le résultat
reste à vérifier avant son utilisation. Aucun site ni serveur n'est nécessaire.
