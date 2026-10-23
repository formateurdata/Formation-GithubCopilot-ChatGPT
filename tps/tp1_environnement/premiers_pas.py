"""TP1 : trois fonctions, écrites par Copilot.

Règle du jeu : ne tapez pas le corps des fonctions vous-même. Placez le curseur sous
la docstring, supprimez la ligne `raise NotImplementedError`, et laissez Copilot proposer.
Acceptez (Tab), acceptez mot par mot (Cmd/Ctrl + Flèche droite), ou guidez-le avec un
commentaire. Vérifiez les trois premières avec : uv run pytest -q
"""


def est_palindrome(texte: str) -> bool:
    """Vrai si le texte se lit de la même façon dans les deux sens.

    On ignore la casse, les espaces et la ponctuation (seuls les lettres et chiffres comptent).

    >>> est_palindrome("Engage le jeu que je le gagne")
    True
    >>> est_palindrome("Copilot")
    False
    """
    raise NotImplementedError


def formater_euros(montant: float) -> str:
    """Formate un montant à la française : séparateur de milliers espace, virgule, 2 décimales, suffixe EUR.

    >>> formater_euros(1234.5)
    '1 234,50 EUR'
    >>> formater_euros(-7)
    '-7,00 EUR'
    """
    raise NotImplementedError


def est_email_valide(adresse: str) -> bool:
    """Vérification simple d'une adresse e-mail.

    Règles : exactement un @, une partie locale non vide, un domaine qui contient
    un point (ni au début ni à la fin du domaine), aucun espace.

    >>> est_email_valide("alice@exemple.fr")
    True
    >>> est_email_valide("alice@exemple")
    False
    """
    raise NotImplementedError
