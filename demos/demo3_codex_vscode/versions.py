"""Comparaison et tri de numéros de version (démo 3 : Codex dans VS Code).

Une version s'écrit "MAJEUR.MINEUR.CORRECTIF", par exemple "1.10.2".
"""


def comparer_versions(a: str, b: str) -> int:
    """Compare deux versions "MAJEUR.MINEUR.CORRECTIF".

    Renvoie -1 si a est plus ancienne que b, 0 si elles sont égales, 1 si a est plus récente.
    Lève ValueError si une version est mal formée.
    """
    if a == b:
        return 0
    return -1 if a < b else 1


def trier_versions(versions: list[str]) -> list[str]:
    """Trie les versions de la plus ancienne à la plus récente."""
    return sorted(versions)


def derniere_version(versions: list[str]) -> str:
    """Version la plus récente de la liste."""
    return trier_versions(versions)[-1]
