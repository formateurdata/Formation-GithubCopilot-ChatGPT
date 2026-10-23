---
name: run-test
description: Exécuter les tests avec uv et pytest, puis fournir un rapport des résultats.
agent: agent
---

Exécute les tests existants en suivant les
[conventions du projet](../copilot-instructions.md).

1. Identifie le dossier du projet ouvert et sa configuration pytest.
2. Si l'utilisateur précise un fichier de tests, un dossier de tests ou un identifiant
   pytest après la commande ou en pièce jointe, utilise cette cible. Si la cible est
   un fichier source, recherche ses tests associés ; si plusieurs choix sont ambigus,
   demande lequel exécuter.
3. Depuis le dossier du projet ouvert, lance `uv run pytest -q -rA`, en ajoutant la cible
   lorsqu'elle est précisée. Sans cible, lance tous les tests du projet ouvert.
4. Lis la sortie réelle et le code de retour. Ne modifie aucun fichier, ne crée aucun test
   et ne corrige pas automatiquement les erreurs. N'installe pas de dépendance supplémentaire.

Rends un rapport en français :

- **Commande et dossier** : commande exacte exécutée et répertoire de travail.
- **Bilan** : nombres de tests réussis, échoués, ignorés et en erreur, selon la sortie.
- **Échecs** : nom de chaque test concerné, attendu et obtenu si disponibles,
  puis cause probable en distinguant les faits des hypothèses.
- **Suite proposée** : prochaine action utile, sans l'appliquer.

Si la commande ne peut pas être exécutée, rapporte l'erreur observée et indique
que le résultat des tests est inconnu. Aucun test collecté ne signifie pas que les tests passent.
