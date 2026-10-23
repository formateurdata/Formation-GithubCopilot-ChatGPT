from panier import facture, frais_de_port, total_ht


def test_total_ht():
    lignes = [{"produit": "Clavier", "prix_unitaire": 49.90, "quantite": 2},
              {"produit": "Souris", "prix_unitaire": 19.90, "quantite": 1}]
    assert round(total_ht(lignes), 2) == 119.70


def test_livraison_offerte_a_partir_de_50_euros():
    assert frais_de_port(50) == 0


def test_facture_sans_code():
    lignes = [{"produit": "Câble", "prix_unitaire": 10.00, "quantite": 2}]
    assert facture(lignes) == {"ht": 20.0, "remise": 0, "tva": 4.0, "port": 4.9, "total": 28.9}
