"""Tests d'acceptation du TP1 : ne pas les modifier."""

import pytest

from premiers_pas import est_email_valide, est_palindrome, formater_euros


@pytest.mark.parametrize("texte, attendu", [
    ("Engage le jeu que je le gagne", True),
    ("Esope reste ici et se repose", True),
    ("A man, a plan, a canal: Panama!", True),
    ("Copilot", False),
    ("", True),
])
def test_est_palindrome(texte, attendu):
    assert est_palindrome(texte) is attendu


@pytest.mark.parametrize("montant, attendu", [
    (1234.5, "1 234,50 EUR"),
    (0, "0,00 EUR"),
    (-7, "-7,00 EUR"),
    (1234567.891, "1 234 567,89 EUR"),
    (999.999, "1 000,00 EUR"),
])
def test_formater_euros(montant, attendu):
    assert formater_euros(montant) == attendu


@pytest.mark.parametrize("adresse, attendu", [
    ("alice@exemple.fr", True),
    ("a.b-c@sous.domaine.org", True),
    ("alice@exemple", False),
    ("@exemple.fr", False),
    ("alice@@exemple.fr", False),
    ("alice @exemple.fr", False),
    ("alice@.fr", False),
    ("alice@exemple.", False),
])
def test_est_email_valide(adresse, attendu):
    assert est_email_valide(adresse) is attendu
