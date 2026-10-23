# Démo 4 — Revue et débogage dans ChatGPT, puis tri de tickets support par l'API

**Durée** : 12 min. **Partie** : P3 (ChatGPT en développement, API OpenAI). **Dossier à ouvrir dans VS Code** : `demos/demo4_chatgpt_api/`.

Message de la démo : ChatGPT aide à relire et corriger du code. L'API sert ici à
une fonction métier distincte : proposer la catégorie, la priorité et le résumé d'un
ticket reçu, pour aider son orientation vers une équipe support.

## Avant la séance

- uv installé et environnement commun préparé avec `uv sync` à la racine de la copie complète du dépôt (voir `README.md`). Les commandes `uv run` se lancent depuis le dossier de la démo.

- ChatGPT ouvert, chat temporaire activé (**Temporary Chat**), pour montrer le bon réflexe.
- Variable `OPENAI_API_KEY` définie dans le terminal intégré (clé du projet de formation, budget plafonné). Ne jamais l'afficher à l'écran.
- Prompts prêts dans `prompts.md`.

## Étapes

Avant tout envoi : utiliser les fichiers fictifs fournis et vérifier qu’aucun secret ni donnée personnelle réelle n’est inclus. Pour comparer deux prompts, choisir un chat temporaire sans personnalisation si cette option est disponible.

### 1. Prompt naïf contre prompt structuré (3 min)

1. Coller le prompt 1 de `prompts.md` (« Est-ce que ce code est bon ? ») avec le code de `import_contacts.py`.
2. Nouvelle conversation, coller le prompt 2 (structuré).
3. Comparer à l'écran : précision des lignes, gravité, problèmes réels trouvés (argument par défaut mutable `vus=[]`, `except` nu qui avale les erreurs, zéro initial perdu par `int()`, doublons sensibles à la casse, fichier jamais fermé).

À faire remarquer : une demande plus précise donne des critères de comparaison ; vérifier les problèmes réels trouvés, les faux positifs et le format obtenu. Aucun résultat précis n’est garanti.

### 2. Débogage guidé par le symptôme (3 min)

1. Lancer `uv run python import_contacts.py contacts.csv` dans le terminal : Alice Martin apparaît deux fois, les numéros perdent leur 0, Chloé Durand a disparu.
2. Coller le prompt 3 avec la sortie obtenue.
3. Faire remarquer : on donne le symptôme, l'attendu et un moyen de reproduire, comme dans un bon ticket ; il a fallu tout copier, là où Codex (démo 3) lançait la commande lui-même. Relire le correctif avant de l'appliquer.
4. Ouvrir `final/import_contacts.py` et lancer `uv run pytest -q final` : les tests passent.

### 3. Documentation (1 min)

Coller le prompt 4 avec le code corrigé, et vérifier une docstring contre le code : « N'invente aucune option » limite les hallucinations, sans les supprimer.

### 4. Classer un ticket support avec l'API (5 min)

1. **Le besoin (1 min).** Ouvrir `ticket.json` : un client fictif signale un double débit. Le support reçoit des messages libres et veut une catégorie, une priorité et un résumé. La commande simule le traitement à réception du ticket.
2. **L'intégration (1 min).** Ouvrir `triage_support.py`. Montrer les quatre catégories autorisées, la règle de priorité et le schéma `TriageTicket`. `classer_ticket(ticket, client)` appelle le modèle ; le programme associe la catégorie à un service proposé.
3. **L'appel (1 min).** Lancer `uv run python triage_support.py ticket.json`. Comparer le résultat au message et aux règles : paiement, priorité haute pour le double débit, résumé fidèle. Ce sont les résultats attendus selon le contrat, pas une prédiction garantie du modèle.
4. **Le contrôle (1 min).** Montrer le statut `a_verifier`. Le schéma limite les catégories, mais ne prouve pas que le classement est juste. Aucun remboursement ni modification de commande n'est exécuté. Contrôler une réponse absente et rappeler que seuls les champs utiles d'un ticket fictif sont transmis.
5. **Les tests (1 min).** Lancer `uv run pytest -q test_api_triage.py`. Le faux client vérifie l'entrée, le schéma, une catégorie inconnue, l'absence de réponse et la propagation d'une panne. Un test simulé ne mesure pas la qualité réelle du classement.

Plan B, sans clé ou sans réseau :

```bash
uv run python triage_support.py ticket.json --exemple final/triage_exemple.json
uv run pytest -q test_api_triage.py final
```

La commande annonce « Exemple fourni : aucune requête API ». C'est un exemple rédigé,
pas une réponse obtenue en direct. Le script complet de secours est aussi dans `final/triage_support.py`.

## Transition vers le TP3

« À vous, avec Codex dans VS Code comme dans la démo 3 : lui faire lire et corriger le script de notes de frais, exécuter les tests et intégrer l'API au catalogue. Relisez ses changements et relancez les commandes. Notre démo API classe un ticket ; votre application préparera la fiche d'un nouvel article de boutique. »
