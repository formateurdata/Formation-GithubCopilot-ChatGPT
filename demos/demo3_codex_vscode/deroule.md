# Démo 3 — Codex dans VS Code

**Durée** : 8 min. **Partie** : P3 (l'offre OpenAI pour les développeurs). **Dossier à ouvrir dans VS Code** : `demos/demo3_codex_vscode/`.

Message de la démo : Codex, l'agent de code d'OpenAI, travaille dans l'éditeur, sur le dépôt. Il lit l'AGENTS.md du projet, agit dans les permissions accordées, reproduit le bug lui-même, et ses modifications se relisent dans le code. C'est le geste que les stagiaires pratiqueront au TP3, avec le compte ChatGPT.

## Avant la séance

- uv installé et environnement commun préparé avec `uv sync` à la racine de la copie complète du dépôt (voir `README.md`). Les commandes `uv run` se lancent depuis le dossier de la démo.

- Extension Codex installée depuis la marketplace (identifiant `openai.chatgpt`) et connectée avec le compte ChatGPT de démonstration.
- Ouvrir le dossier `demos/demo3_codex_vscode/` seul dans VS Code (pour que son `AGENTS.md` soit celui du projet).
- Copie de sauvegarde du dossier : Codex va modifier `versions.py` et `test_versions.py` (`cp -R demos/demo3_codex_vscode /tmp/demo3_sauvegarde`).
- Dans Codex : contrôle des permissions sous la zone de saisie sur **Ask for approval** ; modèle : celui conseillé pour le code (gpt-6.1-sol au 09/10/2026).
- Terminal intégré ouvert, environnement avec pytest.

## Étapes

### 1. L'extension et ses réglages (1 min)

1. Ouvrir Codex depuis son icône dans la barre latérale (sinon, Command Palette : **Codex: Open Codex Sidebar**).
2. Montrer le compte ChatGPT connecté, le sélecteur de modèle, et le contrôle des permissions : **Ask for approval** (point de départ conseillé), **Approve for me**, **Full access**, **Custom (config.toml)**.
3. Faire remarquer : Copilot et Codex cohabitent dans le même éditeur ; on choisit l'outil, pas l'éditeur.

### 2. Le bug et les règles du projet (1 min)

1. Terminal : `uv run pytest -q` : `test_derniere_version_apres_1_9` échoue, `1.10.0` est classée avant `1.9.0`.
2. Ouvrir `AGENTS.md` : commande de test, pas de dépendance (pas de bibliothèque `packaging`), tests tirés de semver.org.

### 3. Corriger avec Codex (3 min)

1. Ouvrir `versions.py` et sélectionner `comparer_versions` (les fichiers ouverts sont inclus d'office ; la sélection précise la cible, ou commande **Add to Codex Thread**). Taper `@` pour citer `test_versions.py`.
2. Prompt :

   > Le test test_derniere_version_apres_1_9 échoue : 1.10.0 est classée avant 1.9.0. Reproduis avec uv run pytest -q, corrige versions.py en respectant AGENTS.md, ajoute des tests pour les cas limites, puis relance les tests. Explique la cause en une phrase.

3. Si Codex demande une autorisation, lire sa cible avant d'approuver. **Ask for approval** autorise les actions dans le périmètre de travail et demande avant de le dépasser ; le test local ne provoque pas forcément une demande.
4. Relire le résumé et les lignes modifiées dans les fichiers ; garder ce qui convient (Undo sinon).
5. Faire remarquer : la cause (comparaison de chaînes de caractères, et non de nombres), la commande lancée par Codex lui-même, et le respect de l'AGENTS.md (aucune dépendance ajoutée). Demander au besoin : « Quelles règles du projet as-tu appliquées ? »

### 4. Planifier avant d'agir (2 min)

1. Prompt :

   > Avant de modifier quoi que ce soit, propose un plan pour gérer les pré-versions selon semver.org (2.0.0-rc.1 est plus ancienne que 2.0.0). Liste les tests que tu ajouterais.

   (La documentation de Codex cite aussi la commande `/plan` pour les tâches en plusieurs étapes : l'utiliser si l'extension la propose.)
2. Relire le plan, le corriger si besoin, puis : « Applique ce plan et lance les tests. »
3. Si le temps manque, s'arrêter au plan : l'état final de secours contient l'implémentation.

### 5. Local ou cloud (1 min)

Montrer le choix **Work locally** / **Cloud** : une tâche longue peut être déléguée à Codex Cloud, et son résultat revient dans la même conversation pour être relu. Ne pas lancer de tâche cloud en démo.

## Plan B

Sans extension ou sans réseau : ouvrir `final/versions.py` et `final/test_versions.py`, lancer `uv run pytest -q final` (16 tests), et décrire les étapes. Les réponses de Codex varient d'une exécution à l'autre : `final/` montre un résultat correct, pas le résultat garanti.

## Après la démo

Restaurer le dossier depuis la sauvegarde, pour que la prochaine session reparte du bug.

## Transition

« Vous utiliserez Codex au TP3 pour lire un projet, le corriger, le tester et intégrer une fonction API. Voyons maintenant comment formuler les demandes, dans ChatGPT comme dans Codex. »
