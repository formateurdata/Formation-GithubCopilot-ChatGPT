# Démo 2 — Corriger un bug, générer des tests, refactoriser avec Copilot

**Durée** : 15 min. **Partie** : P2 (utilisation avancée de Copilot). **Dossier à ouvrir dans VS Code** : `demos/demo2_copilot_avance/`.

Message de la démo : on donne à Copilot le bon contexte (fichier, test qui échoue, exigence écrite), on relit chaque diff, et les tests servent de filet avant tout refactoring.

## Avant la séance

- uv installé et environnement commun préparé avec `uv sync` à la racine de la copie complète du dépôt (voir `README.md`). Les commandes `uv run` se lancent depuis le dossier de la démo.

- Fichiers dans leur état de départ : `panier.py`, `test_panier.py`.
- Terminal intégré ouvert sur le dossier, `uv run pytest -q` prêt (environnement avec pytest).
- Chat view ouverte (`Ctrl+Cmd+I`, Windows : `Ctrl+Alt+I`), nouvelle session, modèle **Auto**, permissions **Manual permissions**.

## Étapes

### 1. Comprendre le code existant (2 min)

1. Sélectionner la fonction `facture`, ouvrir l'inline chat (`Cmd+I`, Windows : `Ctrl+I`) et taper `/explain`.
2. Faire remarquer : l'explication décrit ce que fait le code, y compris ses défauts éventuels ; elle ne dit pas ce qu'il devrait faire.

### 2. Corriger un bug à partir d'un test qui échoue (3 min)

1. Lancer `uv run pytest -q` : `test_livraison_offerte_a_partir_de_50_euros` échoue.
2. Dans la Chat view, agent **Ask** (ou question simple), prompt :

   > Le test test_livraison_offerte_a_partir_de_50_euros de #file:test_panier.py échoue. La règle métier est dans la docstring de frais_de_port. Corrige l'implémentation, pas le test, et explique la cause en une phrase.

3. Appliquer la proposition (`>` remplacé par `>=`), relancer les tests : vert.
4. Faire remarquer : la même règle est recopiée dans `facture` (`if ttc > 50`), toujours fausse. Ajouter un test : un article à 41,67 EUR HT, quantité 1, donne 50 EUR TTC et aucun port. Faire corriger ce second seuil, puis relancer les tests. Les deux implémentations sont maintenant correctes avant le refactoring.

Plan B : si Copilot propose de modifier le test, refuser et rappeler la consigne « corriger l'implémentation, pas le test ».

### 3. Générer des tests à partir des exigences (4 min)

Prompt dans la Chat view :

> Écris des tests pytest pour #file:panier.py dans test_panier.py. Base les résultats attendus sur les docstrings, pas sur l'implémentation. Couvre : panier vide, quantité nulle, code promo inconnu, seuil de livraison à 49,99 / 50 / 50,01 euros. Ne modifie pas panier.py.

1. Relire les tests proposés avant de les accepter (**Keep** fichier par fichier).
2. Lancer les tests : `appliquer_remise` avec un code inconnu lève `KeyError` alors que la docstring exige `ValueError`. C'est le test qui a raison.
3. Corriger avec l'inline chat sur `appliquer_remise` : `/fix lever ValueError si le code est inconnu, comme indiqué dans la docstring`.

À faire remarquer : un test généré à partir de l'implémentation aurait figé le bug.

### 4. Écrire l'AGENTS.md du projet (2 min)

1. Agent **Agent**, prompt :

   > Crée un fichier AGENTS.md à la racine, structuré en sections Projet, Commandes, Conventions, Tests et Sécurité, à partir de ce dépôt. Une règle par ligne. N'invente aucune commande : uniquement celles qui marchent ici. Ajoute la règle « ne jamais modifier un test existant pour le faire passer ».

2. Relire le fichier ligne à ligne : la commande de test est-elle exacte ? une règle est-elle vague ou déjà imposée par l'outillage ? Comparer avec `final/AGENTS.md` (le modèle montré sur la slide « Structurer un AGENTS.md »).
3. Faire remarquer : AGENTS.md est lu par le chat et les agents de Copilot, et aussi par Codex et d'autres agents ; il n'est pas utilisé par les complétions en ligne.

Plan B : copier `final/AGENTS.md` à la racine du dossier.

### 5. Refactoriser sous le filet des tests (4 min)

Passer l'agent sur **Agent**, prompt :

> Refactorise facture() dans panier.py : supprime la duplication avec total_ht, appliquer_remise et frais_de_port, et remplace les nombres magiques par des constantes. Le comportement doit rester identique. Lance les tests après la modification.

1. Approuver la commande de test quand l'agent la demande (montrer la demande d'approbation).
2. Ouvrir le diff de `panier.py`, parcourir les modifications, **Keep**.
3. Montrer **Restore Checkpoint** au survol de la requête (sans l'exécuter, ou l'exécuter puis **Redo**).
4. Faire remarquer : `facture` appelle maintenant `frais_de_port`. Le refactoring conserve le seuil déjà corrigé ; il évite de maintenir la règle en deux endroits.

## État final de secours

`final/panier.py`, `final/test_panier.py`, `final/AGENTS.md` (`uv run python outils/verifier.py`). Les propositions de Copilot varient d'une exécution à l'autre : ces fichiers montrent un résultat correct, pas le résultat garanti.

## Transition vers le TP2

« À vous, sur un autre module : écrire avec les complétions, générer des tests depuis les exigences, corriger un bug, refactoriser sous filet. »
