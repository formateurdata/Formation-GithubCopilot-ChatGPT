# Formation PLB « GitHub Copilot et ChatGPT » (GHCG)

Matériel de formation en 1 jour (programme officiel en 2 jours) : plan, présentation, démonstrations et TP. Les consignes de production sont dans `AGENTS.MD`, le déroulé horaire dans `plan/deroule.md`, la correspondance programme, sources et livrables dans `plan/couverture.md`.

## Contenu

```
plan/            programme officiel, déroulé de la journée, couverture et sources
slides/          formation.pptx (75 slides dont 2 annexes masquées, notes du formateur) et without/ (copie sans speech)
demos/           5 démos : deroule.md (script du formateur), code de départ, final/ (état de secours)
tps/             4 TP : enonce.md, code de départ et tests d'acceptation, corrige/
outils/          verifier.py : vérification des démos et des TP
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

Stagiaires : VS Code récent avec GitHub Copilot (compte GitHub), compte ChatGPT (vérifier l’accès à Codex dans la surface utilisée), Python 3.12 ou plus, Git et [uv](https://docs.astral.sh/uv/getting-started/installation/).

À la racine de la copie complète du dépôt, préparer l'environnement commun une seule fois :

```bash
uv sync
```

Conserver l'arborescence complète, avec `pyproject.toml` et `uv.lock` à la racine.
Ouvrir ensuite le dossier de la démo ou du TP seul dans VS Code, et placer le terminal
dans ce dossier. Les commandes suivantes utilisent l'environnement du projet :

```bash
uv run pytest -q
uv run python nom_du_script.py
```

`nom_du_script.py` est à remplacer par le fichier indiqué dans l'exercice. Aucun `uv init`
n'est nécessaire dans les sous-dossiers. Les [commandes de projet uv](https://docs.astral.sh/uv/guides/projects/)
servent de référence pour cette préparation et l'exécution.

Alternative si uv n'est pas disponible : dans un environnement virtuel Python déjà activé,
installer `python -m pip install -r requirements.txt` depuis la racine. Dans les consignes,
remplacer `uv run python` par `python` et `uv run pytest` par `python -m pytest`.

Chaque démo et chaque TP utilise ainsi son `AGENTS.md` et ses fichiers `.github/`. Pour la partie API de l'après-midi, la clé d'API OpenAI se lit dans la variable `OPENAI_API_KEY` ; le formateur fournit une clé de projet à budget plafonné, révoquée en fin de journée.

Pour les essais API, définir la clé fournie dans le terminal qui lance la commande :

```bash
# macOS / Linux : remplacer la valeur par la clé fournie
export OPENAI_API_KEY="cle-fournie-par-le-formateur"
```

Sous Windows PowerShell : `$env:OPENAI_API_KEY="cle-fournie-par-le-formateur"`.
Ne jamais enregistrer cette clé dans un fichier du dépôt.

Les fichiers `pytest.ini` de chaque exercice isolent les tests de départ des dossiers `final/`
et `corrige/`. La commande `uv run pytest -q` lance les tests de toutes les parties. Conserver ces configurations.
Pour la démo 5 et la partie 4 du TP4, choisir la cible **Local** dans la Chat view avant les commandes de prompt.
Le TP4 utilise `commits.txt` fourni ; aucun commit Git n’est nécessaire au parcours guidé.

Formateur (environnement géré avec uv) :

```bash
uv sync                                         # bibliothèques des démos et TP, outils des slides
uv run python outils/verifier.py                # démos et TP : départ en échec, corrigés au vert, pas d'emoji
uv run python slides/build/build.py             # génère slides/formation.pptx
uv run python slides/build/check_snippets.py    # vérifie le code Python des slides
uv run python slides/build/sans_speech.py       # copie sans speech dans slides/without/
uv run python tps/build_pdf.py                  # actualise les énoncés PDF (pandoc et Chrome)
uv run python slides/build/index_slides.py      # met à jour l'index des slides de plan/couverture.md
```

La génération s'arrête si un titre dépasse une ligne, si un bloc de code dépasse 15 lignes ou descend sous 15 pt, si un prompt déborde de sa carte, ou si le speech ne compte pas une partie par clic.

## Avant chaque session

Les outils changent tous les mois. Revérifier dans les documentations officielles (liens dans `plan/couverture.md`) : noms des modèles OpenAI et leurs prix, offres et quotas Copilot, noms des agents et des réglages dans VS Code. Les points non confirmés au 09/10/2026 sont listés dans `plan/couverture.md`.

Les appels réels à l'API n'ont pas été exécutés pendant la préparation (pas de clé) : les tests utilisent un client simulé. Faire un essai réel de `demos/demo4_chatgpt_api/triage_support.py` avec la clé de formation la veille.

## Les quatre TP

Chaque TP suit un seul parcours découpé en parties à réaliser. Les blocs d'aide donnent
un exemple pour les passages techniques ; les stagiaires font relire et expliquer les
propositions, puis les vérifient. Les corrigés se trouvent dans chaque dossier `corrige/`.

| TP | Parties | Durée | Tests fournis |
|---|---|---|---|
| TP1 | Environnement, trois complétions, comparaison ChatGPT, vérification | 25 min | 18 |
| TP2 | Complétions, tests, bug, refactoring, AGENTS.md, import CSV | 65 min | 19 |
| TP3 | Codex : lecture, corrections, tests, documentation, intégration de l'API catalogue, bilan | 50 min | 15 |
| TP4 | Spécification, AGENTS.md, implémentation, fichier de prompt, charte, bilan | 60 min | 13 |

## Deux usages métier de l'API

Dans le TP3, Codex travaille dans le projet : il lit les fichiers, applique des corrections et exécute les tests. L'apprenant contrôle les différences et relance les commandes. L'API est une fonction de la boutique, développée avec son aide.

La démo 4 classe un ticket support : catégorie, priorité et résumé pour proposer son
orientation. Le TP3 génère la fiche d'un nouvel article de boutique, en préservant les
fiches existantes. Les résultats restent à vérifier avant leur utilisation.
Ces scripts simulent les traitements de l'application ; aucun site ni serveur n'est requis.

Secours de la démo, depuis `demos/demo4_chatgpt_api/` :

```bash
uv run python triage_support.py ticket.json --exemple final/triage_exemple.json
```

Cette commande annonce qu'elle utilise un exemple fourni, sans requête API. Les tests
utilisent des clients simulés. Le formateur essaie l'appel réel avec sa clé avant la session.
Le modèle par défaut de ces cas est `gpt-6-luna`, configurable dans `OPENAI_MODEL`.
Sources et limites de validation : `plan/couverture.md`.
