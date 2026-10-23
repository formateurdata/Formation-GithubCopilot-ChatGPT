# Démo 6 — Enregistrer les prompts que l'on répète souvent

**Durée** : 10 min. **Partie** : complément P2 (Copilot avancé) ou P4 (tâches répétables).
**Dossier à ouvrir dans VS Code** : `demos/demo6_commandes_github/` seul.

Message de la démo : au lieu de réécrire « explique ce code avec ses entrées, ses sorties
et un exemple » ou « lance les tests avec uv et fais un rapport », on enregistre une fois
ces consignes dans `.github/prompts/`. Ensuite, on appelle la commande sur le code de son choix.

Le petit module `livraison.py` conserve le contexte de la boutique utilisé dans la formation.
Les commandes sont génériques : elles peuvent être copiées dans les autres projets Python
des TP, en adaptant les conventions du projet.

## Avant la séance

- Préparer l'environnement avec `uv sync` à la racine de la copie complète du dépôt.
- Ouvrir le dossier de cette démo seul et placer le terminal intégré dans ce dossier.
- Dans la Chat view de VS Code, choisir la cible **Local**, le modèle **Auto** et les
  permissions manuelles, avec GitHub Copilot connecté.
- Lancer `uv run pytest -q` : les **5 tests fournis passent**.

## 1. Passer d'un prompt répété à une commande (2 min)

Montrer une demande que l'on pourrait retaper chaque fois que l'on découvre du code :

> Explique ce code en français : son rôle, ses entrées et sorties, les étapes importantes,
> un exemple concret et les points d'attention. Ne modifie aucun fichier.

Ouvrir `.github/prompts/explainer-prompt.prompt.md` : cette demande y est enregistrée,
avec un format de réponse réutilisable. Montrer l'en-tête :

```yaml
---
name: explainer-prompt
description: Expliquer le code sélectionné ou joint, avec un exemple et les points à retenir.
agent: ask
---
```

Expliquer : `name` donne le nom de la commande, `description` décrit son usage et
`agent: ask` choisit le mode adapté à une explication. Le texte sous l'en-tête est le
prompt que l'on évite désormais de retaper.

## 2. Utiliser `/explainer-prompt` sur plusieurs fichiers (3 min)

1. Ouvrir une nouvelle conversation Local. Taper `/explainer-prompt` et sélectionner
   la commande dans les suggestions.
2. Joindre `livraison.py` avec le sélecteur de contexte `#`, puis envoyer.
3. Montrer la réponse : rôle, entrées/sorties, fonctionnement, exemple, points d'attention.
   Vérifier l'exemple dans le code : à 50 euros TTC, le port vaut 0 euro.
4. Dans une nouvelle conversation, réutiliser **la même commande** en joignant cette
   fois `test_livraison.py` : l'explication porte maintenant sur les tests paramétrés.

On peut aussi sélectionner une fonction dans l'éditeur et l'ajouter au contexte du chat,
ou compléter la commande par une précision :

```text
/explainer-prompt Concentre-toi sur les paramètres du test et explique pytest.mark.parametrize.
```

Joindre `test_livraison.py` à cette demande. La commande contient les consignes communes ;
le fichier joint et la phrase ajoutée précisent la cible du moment.

## 3. Utiliser `/run-test` pour exécuter et obtenir un rapport (3 min)

Montrer le prompt que cette seconde commande remplace :

> Lance les tests existants avec uv et pytest dans le projet ouvert. Donne la commande
> exécutée, le nombre de réussites et d'échecs, puis explique les échecs éventuels.
> Ne modifie pas le code.

Ouvrir `.github/prompts/run-test.prompt.md`, puis dans une nouvelle conversation envoyer :

```text
/run-test
```

1. Montrer `agent: agent` : la commande doit pouvoir lancer pytest dans le terminal.
2. Lire les éventuelles demandes d'autorisation avant de les approuver.
3. Vérifier l'exécution réelle de `uv run pytest -q -rA` depuis le dossier de la démo.
4. Relire le rapport : **5 tests réussis, 0 échec**, avec la commande et le dossier utilisés.
   `-rA` permet d'afficher le détail des résultats, y compris les tests réussis.

Pour relancer uniquement un fichier de tests, envoyer :

```text
/run-test test_livraison.py
```

Résultat attendu : exécution de `uv run pytest -q -rA test_livraison.py`, puis un rapport.
La commande exécute les tests existants ; la génération de nouveaux tests a sa propre commande.
Si un test échoue, `/run-test` décrit cet échec et propose une suite sans corriger les fichiers.

## 4. Montrer les autres prompts réutilisables (2 min)

Afficher le dossier :

```text
.github/
├── copilot-instructions.md
└── prompts/
    ├── explainer-prompt.prompt.md
    ├── run-test.prompt.md
    ├── review-code.prompt.md
    └── generate-tests.prompt.md
```

| Commande | Prompt récurrent enregistré | Contexte à donner à chaque usage |
|---|---|---|
| `/explainer-prompt` | Explique le code avec un exemple et ses points d'attention. | Code sélectionné ou fichier joint. |
| `/run-test` | Exécute les tests avec uv et produis un rapport. | Facultatif : fichier, dossier ou identifiant de test. |
| `/review-code` | Relis le code et présente les problèmes avec des exemples et des améliorations. | Code sélectionné ou fichier joint. |
| `/generate-tests` | Ajoute les tests pytest manquants selon les exigences, puis exécute-les. | Code sélectionné ou fichier joint, cas particuliers éventuels. |

Ces fichiers ne contiennent aucun nom de fonction ni chemin de code propre à la livraison.
Leur seule référence commune est le fichier de conventions du projet.
`copilot-instructions.md` fournit les conventions générales ; les fichiers `.prompt.md`
enregistrent les tâches que l'on appelle à la demande.

Pour créer une nouvelle commande, lancer **Chat: New Prompt File** depuis la palette,
choisir le stockage dans le workspace, puis enregistrer un fichier dans `.github/prompts/`.
Par exemple, `document-code.prompt.md` peut contenir cette consigne :

```markdown
---
name: document-code
description: Proposer une docstring pour le code fourni.
agent: ask
---
Propose une docstring en français pour la fonction sélectionnée ou jointe.
Décris ses paramètres, sa valeur de retour, ses erreurs et un exemple.
Si aucune fonction n'est fournie, demande laquelle documenter.
Présente la docstring dans la réponse sans modifier le fichier.
```

## Plan B

Si une commande n'apparaît pas, vérifier le dossier ouvert, la cible **Local**,
l'extension `.prompt.md` et l'enregistrement du fichier. Utiliser **Chat: Run Prompt**
dans la palette ou le bouton de lecture du fichier de prompt. **Chat: Open Customizations**,
section **Prompts**, permet de vérifier les commandes découvertes.

Sans accès au chat, lire les fichiers de prompt pour montrer les consignes enregistrées,
puis lancer manuellement `uv run pytest -q -rA`. Exemple de bilan à comparer à la sortie :

```text
Commande : uv run pytest -q -rA
Dossier : demos/demo6_commandes_github/
Résultat : 5 réussites, 0 échec, 0 test ignoré, 0 erreur.
Suite : aucune correction nécessaire pour les cas couverts.
```

L'exécution des tests ne modifie pas les sources : cette partie se rejoue directement.
Les commandes qui génèrent des fichiers demandent de relire leurs différences.

## Transition

« Identifiez les consignes que vous répétez chaque jour : expliquer, tester, relire,
documenter. Enregistrez-les une fois, puis donnez seulement la cible à chaque utilisation.
Au TP4, vous créerez une commande `/changelog` selon le même principe. »

Référence : [fichiers de prompt dans VS Code](https://code.visualstudio.com/docs/agent-customization/prompt-files).
