# Notes de frais — utilisation

Calcule le montant remboursé à chaque salarié à partir d'un fichier CSV de dépenses, selon les règles de `SPEC.md` (conversion en euros, puis plafond par dépense).

```bash
uv run python legacy/notes_frais.py donnees/notes_septembre.csv
```

Le fichier CSV utilise le séparateur `;` et les colonnes `date;salarie;categorie;montant;devise`. Les taux de conversion sont lus dans `taux.json`, à côté du dossier `legacy/`. Le script affiche un total par salarié, trié par nom, puis les dépenses rejetées avec leur motif :

```
Martin : 180,30 EUR
Dépenses rejetées :
- ligne 7, Diallo : catégorie inconnue : taxi
```


## Partie 5 — catalogue e-commerce

Après application du corrigé, depuis le dossier du TP :

```bash
uv run pytest -q test_api_catalogue.py
uv run python catalogue.py catalogue.json nouvel_article.json
```

La première commande utilise un faux client. La seconde nécessite la clé de formation
dans OPENAI_API_KEY et écrit `catalogue_brouillon.json`. Relire les affirmations avant
publication : le schéma valide la forme, pas les faits. La fiche existante reste inchangée.
Les deux jeux JSON sont aussi fournis dans `corrige/` pour un essai depuis ce dossier.
