# Prompts de la démo 4

À copier dans ChatGPT. Remplacer `<CODE>` par le contenu de `import_contacts.py`.

## 1. Revue : prompt naïf

```
Est-ce que ce code est bon ?
<CODE>
```

## 2. Revue : prompt structuré

```
Rôle : tu es un relecteur Python senior, exigeant sur la fiabilité des données.

Contexte : ce script importe un fichier CSV de contacts clients (séparateur ;)
pour alimenter un CRM. Il tourne une fois par jour sur des fichiers de 10 000 lignes.
Python 3.12, bibliothèque standard uniquement.

Tâche : fais la revue du code ci-dessous.

Contraintes :
- signale uniquement les problèmes réels, pas les préférences de style ;
- pour chaque problème : ligne, gravité (bloquant, majeur, mineur), explication en une phrase ;
- ne réécris pas tout le fichier.

Format : un tableau Markdown, trié par gravité, puis trois recommandations prioritaires.

Code :
"""
<CODE>
"""
```

## 3. Débogage : symptôme, attendu, reproduction

```
Le script ci-dessous, lancé sur le fichier CSV suivant, affiche ce résultat.

Commande : uv run python import_contacts.py contacts.csv
Fichier :
<CONTENU DE contacts.csv>

Sortie obtenue :
<SORTIE>

Sortie attendue : 3 contacts (Alice Martin une seule fois, Chloé Durand gardée
sans téléphone), téléphones au format 0612345678.

Explique la cause de chaque écart, puis propose le correctif minimal pour chacun.
Code :
"""
<CODE>
"""
```

## 4. Documentation

```
Écris les docstrings (style Google, en français) des fonctions du code corrigé ci-dessous,
puis une section README « Utilisation » de 10 lignes maximum avec un exemple de commande.
N'invente aucune option : documente uniquement ce que fait le code.
"""
<CODE CORRIGÉ>
"""
```
