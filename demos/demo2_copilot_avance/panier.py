"""Calcul du montant d'une commande en ligne (démo 2).

Une ligne de panier est un dictionnaire :
{"produit": "Clavier", "prix_unitaire": 49.90, "quantite": 2}
Les prix unitaires sont hors taxes (HT).
"""

TVA = 0.20
CODES_PROMO = {"BIENVENUE10": 0.10, "FIDELE20": 0.20}


def total_ht(lignes):
    """Somme des prix unitaires multipliés par les quantités."""
    total = 0
    for ligne in lignes:
        total += ligne["prix_unitaire"] * ligne["quantite"]
    return total


def appliquer_remise(montant, code):
    """Applique le code promo au montant.

    Lève ValueError si le code est inconnu.
    """
    taux = CODES_PROMO[code]
    return montant - montant * taux


def frais_de_port(montant_ttc):
    """Livraison offerte à partir de 50 euros TTC, sinon 4,90 euros."""
    if montant_ttc > 50:
        return 0
    return 4.90


def facture(lignes, code=None):
    """Détail de la facture : HT, remise, TVA, port et total à payer, arrondis au centime."""
    ht = 0
    for l in lignes:
        if l["quantite"] <= 0:
            raise ValueError("quantité invalide")
        ht = ht + l["prix_unitaire"] * l["quantite"]
    ht = round(ht, 2)
    if code is not None:
        if code in CODES_PROMO:
            remise = round(ht * CODES_PROMO[code], 2)
        else:
            raise ValueError("code promo inconnu")
    else:
        remise = 0
    ht_apres_remise = round(ht - remise, 2)
    tva = round(ht_apres_remise * 0.2, 2)
    ttc = round(ht_apres_remise + tva, 2)
    if ttc > 50:
        port = 0
    else:
        port = 4.9
    total = round(ttc + port, 2)
    return {"ht": ht, "remise": remise, "tva": tva, "port": port, "total": total}
