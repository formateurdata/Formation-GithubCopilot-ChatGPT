"""Tests d'acceptation du TP2 : ne pas les modifier.

Vos propres tests (étape 2) vont dans test_reservations.py.
"""

from datetime import date, datetime, time

import pytest

from reservations import (ConflitDeReservation, Reservation, ajouter, chevauche, creneaux_libres,
                          rapport_hebdomadaire, taux_occupation)

LUNDI = date(2026, 10, 12)


def resa(salle, jour, h1, m1, h2, m2, formateur="Nadia"):
    return Reservation(salle, datetime(2026, 10, jour, h1, m1), datetime(2026, 10, jour, h2, m2), formateur)


PLANNING = [
    resa("Turing", 12, 9, 0, 12, 30),
    resa("Turing", 12, 14, 0, 17, 0, "Sophie"),
    resa("Turing", 13, 9, 0, 18, 0),
    resa("Turing", 15, 13, 30, 15, 15, "Karim"),
    resa("Lovelace", 14, 10, 0, 11, 0, "Karim"),
    resa("Lovelace", 16, 9, 0, 17, 15, "Sophie"),
    resa("Lovelace", 19, 9, 0, 18, 0, "Karim"),
]


# Étape 1 -------------------------------------------------------------------

def test_chevauche_meme_salle():
    assert chevauche(resa("Turing", 12, 9, 0, 11, 0), resa("Turing", 12, 10, 0, 12, 0))


def test_chevauche_reservation_contenue():
    assert chevauche(resa("Turing", 12, 9, 0, 17, 0), resa("Turing", 12, 10, 0, 11, 0))


def test_ne_chevauche_pas_quand_les_reservations_se_touchent():
    assert not chevauche(resa("Turing", 12, 9, 0, 11, 0), resa("Turing", 12, 11, 0, 12, 0))


def test_ne_chevauche_pas_dans_deux_salles_differentes():
    assert not chevauche(resa("Turing", 12, 9, 0, 11, 0), resa("Lovelace", 12, 9, 0, 11, 0))


def test_ajouter_renvoie_un_planning_trie_sans_modifier_l_original():
    planning = [resa("Turing", 12, 14, 0, 15, 0)]
    nouveau = ajouter(planning, resa("Turing", 12, 9, 0, 10, 0))
    assert [r.debut.hour for r in nouveau] == [9, 14]
    assert len(planning) == 1


def test_ajouter_accepte_deux_reservations_qui_se_touchent():
    planning = ajouter([resa("Turing", 12, 9, 0, 11, 0)], resa("Turing", 12, 11, 0, 12, 0))
    assert len(planning) == 2


def test_ajouter_refuse_un_conflit():
    with pytest.raises(ConflitDeReservation):
        ajouter([resa("Turing", 12, 9, 0, 11, 0)], resa("Turing", 12, 10, 30, 12, 0))


@pytest.mark.parametrize("mauvaise", [
    resa("Turing", 12, 11, 0, 11, 0),
    resa("Turing", 12, 11, 0, 10, 0),
    resa("Turing", 12, 8, 0, 10, 0),
    resa("Turing", 12, 17, 0, 19, 0),
    Reservation("Turing", datetime(2026, 10, 12, 16, 0), datetime(2026, 10, 13, 10, 0), "Nadia"),
])
def test_ajouter_refuse_des_horaires_invalides(mauvaise):
    with pytest.raises(ValueError):
        ajouter([], mauvaise)


def test_taux_occupation():
    assert taux_occupation(PLANNING, "Turing", LUNDI) == 0.72
    assert taux_occupation(PLANNING, "Turing", date(2026, 10, 13)) == 1.0
    assert taux_occupation(PLANNING, "Turing", date(2026, 10, 14)) == 0.0


# Étape 3 -------------------------------------------------------------------

def test_creneaux_libres_entre_deux_reservations():
    assert creneaux_libres(PLANNING, "Turing", date(2026, 10, 15))[0] == (time(9, 0), time(13, 30))


def test_creneaux_libres_fin_de_journee():
    assert creneaux_libres(PLANNING, "Turing", LUNDI) == [(time(12, 30), time(14, 0)), (time(17, 0), time(18, 0))]


def test_creneaux_libres_journee_vide_et_journee_pleine():
    assert creneaux_libres(PLANNING, "Turing", date(2026, 10, 14)) == [(time(9, 0), time(18, 0))]
    assert creneaux_libres(PLANNING, "Turing", date(2026, 10, 13)) == []


# Étape 4 : test de caractérisation, il fige le résultat actuel avant le refactoring ---

RAPPORT_ATTENDU = """Semaine du 12/10/2026
Salle Lovelace
  lundi : 0 %
  mardi : 0 %
  mercredi : 11 %
  jeudi : 0 %
  vendredi : 92 %
  semaine : 21 %
Salle Turing
  lundi : 72 %
  mardi : 100 %
  mercredi : 0 %
  jeudi : 19 %
  vendredi : 0 %
  semaine : 38 %"""


def test_rapport_hebdomadaire_inchange():
    assert rapport_hebdomadaire(PLANNING, LUNDI) == RAPPORT_ATTENDU
