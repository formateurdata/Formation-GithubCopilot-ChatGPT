---
name: explainer-prompt
description: Expliquer le code sélectionné ou joint, avec un exemple et les points à retenir.
agent: ask
---
Commence toujours par dire Bonjour, puis explique le code.

Explique le code sélectionné ou le fichier joint à cette demande, en suivant les
[conventions du projet](../copilot-instructions.md).
Si l'utilisateur précise une fonction ou un passage après la commande, concentre-toi dessus.
Si aucun code n'est fourni dans la sélection, les pièces jointes ou la demande,
demande quel fichier ou quelle fonction expliquer.

Réponds en français pour un développeur qui découvre ce code :

1. **Rôle** : à quoi sert ce code, en deux phrases maximum.
2. **Entrées et sorties** : paramètres, valeur retournée et erreurs explicitement prévues.
3. **Fonctionnement** : les étapes importantes dans l'ordre d'exécution.
4. **Exemple** : une entrée concrète et le résultat déduit du code.
5. **Points d'attention** : limites, hypothèses et éventuels écarts avec la documentation.

Ne modifie aucun fichier et n'exécute aucune commande.
Distingue ce que fait le code de ce qu'il devrait faire selon sa documentation.
