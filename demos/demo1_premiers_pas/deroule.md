# Démo 1 — Installer Copilot, premières complétions, même question dans ChatGPT

**Durée** : 10 min. **Partie** : P1 (découverte et installation). **Dossier à ouvrir dans VS Code** : `demos/demo1_premiers_pas/`.

Message de la démo : Copilot complète à partir de ce qu'il voit (nom, signature, docstring, commentaire, fichiers ouverts) ; ChatGPT ne voit que ce qu'on lui colle.

## Avant la séance

- uv installé et environnement commun préparé avec `uv sync` à la racine de la copie complète du dépôt (voir `README.md`). Les commandes `uv run` se lancent depuis le dossier de la démo.

- VS Code à jour, connecté au compte GitHub de démonstration ; une seconde fenêtre VS Code avec un profil vierge (`Profils > Nouveau profil`) pour montrer l'installation sans abîmer la configuration principale.
- Navigateur ouvert sur ChatGPT, connecté.
- Police de l'éditeur à 18 pt au moins pour la projection.
- `conversions.py` dans son état de départ (le fichier se termine par une signature sans corps).

## Étapes

Avant tout envoi : utiliser les fichiers fictifs fournis et vérifier qu’aucun secret ni donnée personnelle réelle n’est inclus. Pour comparer deux prompts, choisir un chat temporaire sans personnalisation si cette option est disponible.

### 1. Activer Copilot (2 min)

1. Dans le profil vierge : survoler l'icône Copilot de la barre d'état, choisir **Use AI Features**, se connecter avec GitHub.
2. Montrer le tableau de bord Copilot (clic sur l'icône de la barre d'état) : pourcentage de l'allocation mensuelle utilisée.
3. Faire remarquer : sans plan payant, le compte passe en Copilot Free (2 000 complétions par mois, chat et agents limités par une allocation de crédits IA).

Plan B : si la connexion échoue (proxy, SSO), basculer sur le profil déjà connecté et décrire l'étape.

### 2. Compléter à partir d'une signature (2 min)

1. Revenir au profil connecté, ouvrir `conversions.py`, placer le curseur sous la signature de `celsius_vers_fahrenheit`.
2. Attendre le texte grisé (ghost text), accepter avec `Tab`.
3. Faire remarquer : le nom et les types suffisent pour une fonction aussi classique.

### 3. Compléter à partir d'une docstring avec un exemple (2 min)

Taper :

```python
def slugifier(titre: str) -> str:
    """Transforme un titre en identifiant d'URL : minuscules, sans accents, mots séparés par des tirets.

    >>> slugifier("Formation GitHub Copilot & ChatGPT")
    'formation-github-copilot-chatgpt'
    """
```

1. Accepter mot par mot avec `Cmd+Flèche droite` (Windows : `Ctrl+Flèche droite`) pour montrer l'acceptation partielle.
2. Survoler la suggestion pour voir les autres propositions.
3. Faire remarquer : l'exemple dans la docstring guide la proposition (accents, ponctuation) ; les imports `re` et `unicodedata` déjà présents en haut du fichier aussi.

### 4. Compléter à partir d'un commentaire (2 min)

Taper le commentaire, puis `def` :

```python
# Convertit une durée écrite "1h30", "2h" ou "45min" en minutes ; ValueError si le format est inconnu
def
```

1. Accepter, puis relire à voix haute : la proposition gère-t-elle `"45min"` ? une chaîne vide ?
2. Ouvrir l'inline chat (`Cmd+I`, Windows : `Ctrl+I`) sur la fonction et taper :

   > Ajoute la gestion des espaces et des majuscules, sans changer la signature.

3. Montrer le diff inline, puis **Keep**.

### 5. La même question dans ChatGPT (2 min)

Dans ChatGPT, nouvelle conversation :

> Écris une fonction Python duree_en_minutes(texte) qui convertit "1h30", "2h" ou "45min" en minutes et lève ValueError si le format est inconnu. Donne aussi 5 cas de test pytest.

Faire remarquer :

- la réponse est souvent plus explicative et propose des tests, mais ChatGPT ignore nos conventions et nos fichiers : il faut lui donner le contexte ;
- le code doit être copié, relu, puis testé dans le projet ;
- montrer le réglage **Settings > Data controls > Improve the model for everyone** (libellés de l'interface anglaise ; la traduction française peut varier) et le chat temporaire (**Temporary Chat**) : à régler avant de coller du code d'entreprise.

## État final de secours

`final/conversions.py` et `final/test_conversions.py` (`uv run pytest demos/demo1_premiers_pas/final`). Les propositions de Copilot varient d'une exécution à l'autre : ce fichier montre un résultat correct, pas le résultat garanti.

## Transition vers le TP1

« À vous : installez, réglez, et faites écrire trois fonctions à Copilot sans taper leur corps. »
