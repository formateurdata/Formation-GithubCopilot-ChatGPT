# TP3 — piloter Codex : prompts et points de contrôle (corrigé)

Ces prompts se saisissent dans l'extension Codex de VS Code, sur le dossier du TP ouvert seul. Codex lit les fichiers, les modifie et exécute les commandes autorisées. Ses réponses varient : vérifier les différences et les sorties réelles, puis relancer les tests dans son terminal. Les blocs ci-dessous donnent des demandes de départ, pas des réponses garanties.

## Partie 1 — lecture et plan

Avant la première demande, masquer le mot de passe fictif dans le fichier. Lire `AGENTS.md`, conserver une copie du départ et vérifier le périmètre de travail local dans Codex.

```
Lis AGENTS.md, SPEC.md et legacy/notes_frais.py. Ne consulte pas corrige/.
Sans modifier de fichier, relève les écarts à la spécification dans un tableau :
ligne, règle concernée, gravité, correction proposée. Propose un plan court
et indique les commandes pour reproduire puis vérifier les problèmes.
```

Points qu'une bonne revue relève :

| Gravité | Problème |
|---|---|
| bloquant | `eval()` sur le contenu de `taux.json` : exécution de code arbitraire ; utiliser `json.load` |
| bloquant | mot de passe SMTP fictif en clair dans le code ; le retirer. Pour un secret réel exposé, prévoir sa révocation et son remplacement |
| majeur | plafond appliqué avant la conversion de devise (contraire à la règle 1) |
| majeur | `except:` nu qui avale toutes les erreurs : catégorie inconnue et montant à virgule disparaissent en silence (règle 4) |
| majeur | `float("21,40")` échoue : la virgule décimale n'est pas gérée |
| majeur | `TOT` global : deux appels successifs à `traiter` cumulent les totaux |
| mineur | `taux.json` ouvert relativement au dossier courant ; fichiers jamais fermés ; noms d'une lettre ; affichage `189.0 EUR` au lieu de `189,00 EUR` |

## Partie 2 — reproduction, correction et tests

```
Exécute uv run python legacy/notes_frais.py donnees/notes_septembre.csv
et uv run pytest -q test_acceptation_tp3.py.
Explique les échecs observés par rapport à SPEC.md, puis applique les corrections
du plan dans legacy/notes_frais.py uniquement. Retire le mot de passe inutilisé,
remplace eval, puis relance ces commandes. Ne modifie pas les tests fournis.
Termine par les fichiers modifiés, les corrections et les résultats des commandes.
```

Attendu : Martin (hôtel 110 GBP plafonné avant conversion), Diallo (26 USD plafonnés à 25 avant conversion, taxi ignoré), Nguyen (21,40 illisible, avalé par `except`). Après correction : Diallo 48,92 EUR, Martin 180,30 EUR et Nguyen 251,40 EUR ; taxi signalé. Relire les différences dans l'éditeur et relancer les tests soi-même. Si Codex modifie un test fourni, lui faire rétablir le fichier et corriger l'implémentation.

## Partie 3 — tests depuis la spécification

```
À partir des règles et exemples de SPEC.md, propose d'abord un tableau de cas
et de résultats attendus. Après ma relecture, crée test_notes_frais.py avec ces
tests pytest, adapte les appels aux fonctions corrigées et exécute les tests.
Ne déduis pas les valeurs attendues du code et ne change pas les tests fournis.
```

Vérifier le tableau avant de demander la création du fichier. Voir `corrige/test_notes_frais.py` : les noms retenus sont `montant_rembourse` et `lire_montant`. D'autres noms sont acceptables s'ils respectent le contrat ; les attentes viennent de `SPEC.md`. Le modèle ayant déjà lu le code, la vérification manuelle des attentes reste nécessaire.

## Partie 4 — documentation

```
Ajoute les docstrings en français dans legacy/notes_frais.py et crée README.md,
avec une section « Utilisation » de dix lignes maximum. Vérifie la commande
et l'exemple de sortie en exécutant le script. N'invente ni option ni format.
Ne modifie pas le comportement du code pendant cette étape.
```

Vérification : chaque phrase de la documentation se retrouve dans le code (voir `corrige/README.md`).

## Partie 5 — catalogue e-commerce

Le script de notes de frais illustre le développement assisté par Codex.
Ce second cas montre une fonction de l'application : préparer une fiche lorsque
le gestionnaire ajoute un article à la boutique.

Prompt pour demander à Codex de compléter `catalogue.py` :

```
Complète uniquement generer_fiche et ajouter_article en respectant leurs docstrings.
Une référence déjà présente est refusée avant tout appel API. Un nouvel article
reçoit une seule fiche, en brouillon, sans changer les articles existants.
Utilise client.responses.parse avec FicheProduit et store=False.
Ne modifie pas test_api_catalogue.py. Exécute uv run pytest -q test_api_catalogue.py
avec le client simulé. N'effectue pas d'appel réel à l'API et ne lis pas de clé.
Indique les fichiers modifiés et les résultats des tests.
```

Voir `corrige/catalogue.py`. Le schéma Pydantic fixe le format, pas la véracité.
Les tests remplacent le client : `uv run pytest -q test_api_catalogue.py` (8 tests).
Ils vérifient les champs envoyés, la réponse absente, l'ajout, le doublon sans appel,
la préservation de l'existant sur erreur et les données requises.

Relire les différences et relancer les tests soi-même. Avec la clé de formation, depuis son terminal dans le dossier du TP, après application du corrigé :

```bash
uv run python catalogue.py catalogue.json nouvel_article.json
```

Critères de relecture du brouillon pour la boîte : polypropylène, dimensions
20 x 15 x 10 cm, couleur transparente. Pas de certification alimentaire,
pas de volume ou de charge maximale inventés. Le libellé peut varier.
Le catalogue initial garde sa fiche de câble ; seul le nouvel article est généré.
Le statut `brouillon` n'est pas une publication sur un site.

Pour simuler l'ajout suivant, donner le catalogue de sortie et un autre article,
avec une nouvelle référence et un autre fichier de sortie. Le TP n'implémente
ni serveur web ni tâche de fond. Le formateur essaie l'appel réel avant la séance ; le client simulé sert de secours en cas d'incident d'accès.

## Partie 6 — bilan

Relancer `uv run pytest -q` dans son terminal. Montrer une différence produite par Codex et expliquer sa vérification. Relier une règle de SPEC.md à une correction et à un test. Exemple : convertir 110 GBP
en 128,70 EUR, puis appliquer le plafond hôtel de 120 EUR. La sortie de Martin doit être
180,30 EUR sur les données fournies. Le résultat doit être vérifié même si le modèle
l'affirme avec assurance. Les 7 tests de `test_acceptation_tp3.py` valident les notes de frais ; les 8 tests
de `test_api_catalogue.py` valident l'ajout au catalogue. Les deux parties sont à terminer.

