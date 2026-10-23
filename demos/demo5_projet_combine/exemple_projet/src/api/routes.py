"""Routes HTTP du service de réservation (exemple pour la démo 5)."""


def lister_salles(requete):
    # TODO(nadia): paginer la réponse au-delà de 100 salles
    return []


def reserver(requete):
    # FIXME: deux réservations simultanées peuvent passer (pas de verrou)
    return {"statut": "ok"}
