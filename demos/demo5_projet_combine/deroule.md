# Démo 5 — Un outil de bout en bout : ChatGPT cadre, Copilot planifie et implémente

**Durée** : 10 min. **Partie** : P4 (combiner les deux outils). **Dossier à ouvrir dans VS Code** : `demos/demo5_projet_combine/`.

Message de la démo : chaque outil à sa place. ChatGPT transforme un besoin flou en spécification ; Copilot (Plan puis Agent) l'implémente dans le dépôt, sous contrôle des tests ; un fichier de prompt rend la tâche répétable.

## Avant la séance

- uv installé et environnement commun préparé avec `uv sync` à la racine de la copie complète du dépôt (voir `README.md`). Les commandes `uv run` se lancent depuis le dossier de la démo.

- Dossier dans son état de départ : `besoin.md`, `exemple_projet/`, pas de `spec.md`, pas de `todo_report.py`, pas de `.github/`.
- ChatGPT ouvert en chat temporaire.
- Chat view : nouvelle session, cible **Local**, agent **Plan**, modèle **Auto**, permissions manuelles proposées par cette cible. Les fichiers `.prompt.md` de cette démo nécessitent Local.

## Étapes

### 1. ChatGPT : du besoin à la spécification (3 min)

Coller dans ChatGPT :

```
Voici un besoin exprimé par un responsable d'équipe :
<CONTENU DE besoin.md>

Rédige une spécification courte en Markdown pour un script Python 3.12 (bibliothèque standard) :
règles numérotées, critères d'acceptation vérifiables, cas limites, hors périmètre.
Pose-moi d'abord les questions nécessaires si le besoin est ambigu.
```

1. Répondre aux questions éventuelles (par exemple : « marqueurs en majuscules seulement », « ignorer les dossiers cachés »).
2. Copier la spécification dans `spec.md`, la relire et la corriger à la main : c'est le développeur qui la valide.

Plan B : copier `final/spec.md`.

### 2. Copilot Plan : un plan avant le code (2 min)

Dans la Chat view, choisir l'agent **Plan**, prompt :

> Propose un plan pour implémenter #file:spec.md dans todo_report.py, avec des tests pytest dans test_todo_report.py. Le dossier exemple_projet sert de données de test.

1. Relire le plan : fonctions, tests, ordre. Demander une correction si un critère d'acceptation manque.
2. Faire remarquer : le Plan lit le dépôt mais ne modifie rien.

### 3. Copilot Agent : implémenter et tester (3 min)

Passer sur **Agent** et demander d'exécuter le plan :

> Implémente ce plan. Lance les tests à la fin et corrige jusqu'à ce qu'ils passent, sans modifier spec.md.

1. Approuver la commande de test quand elle est demandée.
2. Ouvrir le diff, vérifier un critère d'acceptation (dossier `.dependances/` ignoré), **Keep**.
3. Lancer `uv run python todo_report.py exemple_projet` dans le terminal.

Plan B : depuis le dossier de la démo, copier `final/todo_report.py` et `final/test_todo_report.py` à la racine, en conservant `pytest.ini` et `exemple_projet/`, puis lancer `uv run pytest -q` (6 tests). Les chemins des tests fonctionnent dans les deux emplacements.

Variante à citer : la même étape avec Codex (extension IDE ou `codex` dans le terminal), qui lit le même `AGENTS.md`.

### 4. Rendre la tâche répétable (2 min)

1. Copier `final/AGENTS.md` et `final/.github/` dans le dossier : les règles du projet (sections Projet, Commandes, Conventions, Tests, Limites) et le fichier de prompt.
2. Dans la Chat view, taper `/revue-avant-commit` : la revue utilise la même liste de contrôle. Sans historique Git, le prompt annonce une revue complète des fichiers de l’exercice contre spec.md, plutôt qu’un diff.
3. Faire remarquer : le script tourne sans IA chaque lundi ; l'IA a servi à le construire et sert à le relire.

## État final de secours

`final/` (`uv run python outils/verifier.py`). Les réponses des modèles varient d'une exécution à l'autre : ces fichiers montrent un résultat correct, pas le résultat garanti.

## Transition vers le TP4

« À vous : un générateur de changelog testé et une charte courte d'usage de l'IA. Vous créerez aussi le fichier de prompt réutilisable, puis vérifierez chaque résultat. »
