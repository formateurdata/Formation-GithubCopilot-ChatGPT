"""Frais de livraison du panier de la boutique (prolongement de la démo 2)."""

SEUIL_LIVRAISON_OFFERTE = 50.0
FRAIS_LIVRAISON = 4.90


def frais_de_port(montant_ttc: float) -> float:
    """Livraison offerte à partir de 50 euros TTC inclus, sinon 4,90 euros.

    Le montant fourni est positif ou nul, déjà arrondi au centime.
    """
    if montant_ttc >= SEUIL_LIVRAISON_OFFERTE:
        return 0.0
    return FRAIS_LIVRAISON
