"""Tests de la partie import CSV du TP2 : ne pas les modifier."""

from pathlib import Path

import pytest

ICI = Path(__file__).resolve().parent


def test_charger_csv_trie_les_reservations():
    from reservations import charger_csv
    planning = charger_csv(ICI / "reservations.csv")
    assert len(planning) == 4
    assert [(r.salle, r.debut.day, r.debut.hour) for r in planning] == [
        ("Turing", 12, 9), ("Lovelace", 12, 14), ("Turing", 12, 14), ("Turing", 13, 9)]


def test_charger_csv_detecte_un_conflit():
    from reservations import ConflitDeReservation, charger_csv
    with pytest.raises(ConflitDeReservation):
        charger_csv(ICI / "reservations_conflit.csv")
