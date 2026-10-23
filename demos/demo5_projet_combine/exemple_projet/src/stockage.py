"""Accès aux données (exemple pour la démo 5)."""

CONNEXION = None


def ouvrir():
    # HACK: connexion globale en attendant le pool
    global CONNEXION
    CONNEXION = object()
    return CONNEXION


def fermer():
    # TODO: fermer proprement en cas d'exception
    pass
