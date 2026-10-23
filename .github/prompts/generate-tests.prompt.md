---
name: generate-tests
description: Ajouter les tests pytest manquants pour le code sélectionné ou joint.
agent: agent
---

Ajoute des tests pytest pour le code sélectionné ou le fichier joint, en suivant les
[conventions du projet](../copilot-instructions.md).
Prends en compte les cas demandés après la commande.
Si la cible n'est pas fournie, demande quel code tester.

1. Lis le code, ses docstrings et les tests existants associés.
2. Déduis les résultats attendus des exigences documentées. Si une règle manque,
   signale l'ambiguïté avant d'inventer un comportement.
3. Complète les tests manquants : cas nominal, limites et erreurs documentées.
   Conserve les tests existants et évite les doublons. Si les cas sont déjà couverts,
   explique-le sans ajouter des tests identiques.
4. Ne modifie pas le code de production ni les fichiers de configuration.
5. Depuis le dossier du projet ouvert, lance les tests concernés avec `uv run pytest -q`.
6. Résume les cas ajoutés et le résultat réel. Si un test révèle un bug, explique-le
   sans modifier l'implémentation ni affaiblir le test pour obtenir un succès.

Si l'exécution est impossible, indique-le clairement.
