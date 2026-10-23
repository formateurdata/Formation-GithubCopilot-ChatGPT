---
name: review-code
description: Relire le code sélectionné ou joint et proposer des améliorations justifiées.
agent: ask
---

Fais une revue du code sélectionné ou du fichier joint, en suivant les
[conventions du projet](../copilot-instructions.md).
Prends en compte les précisions ajoutées après la commande.
Si la cible n'est pas fournie, demande quel code relire.

Examine la conformité aux docstrings, les bugs possibles, les cas limites,
la lisibilité et la couverture des tests disponibles dans le contexte.

Présente les constats par ordre d'importance. Pour chacun, indique :

- la fonction ou le passage concerné ;
- le problème et un exemple concret qui le montre ;
- l'amélioration proposée et le test qui permettrait de la vérifier.

S'il n'y a pas de problème identifié, dis-le et précise les limites de la revue.
Ne modifie aucun fichier et n'exécute aucune commande.
