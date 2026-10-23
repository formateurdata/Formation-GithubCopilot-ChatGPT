"""Exemple de tests unitaires générés avec ChatGPT à partir de SPEC.md (étape 4, corrigé).

Prompt utilisé : voir prompts_types.md. Les valeurs attendues viennent du tableau
d'exemples de la spécification, pas d'une exécution du code.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent / "legacy"))

from notes_frais import charger_taux, formater_euros, lire_montant, montant_rembourse  # noqa: E402

TAUX = {"EUR": 1.0, "USD": 0.92, "GBP": 1.17}


@pytest.mark.parametrize("categorie, montant, devise, attendu", [
    ("repas", 18.00, "EUR", 18.00),
    ("repas", 32.00, "EUR", 25.00),
    ("hotel", 110, "GBP", 120.00),
    ("repas", 26, "USD", 23.92),
    ("transport", 250, "USD", 230.00),
])
def test_exemples_de_la_spec(categorie, montant, devise, attendu):
    assert montant_rembourse(categorie, montant, devise, TAUX) == attendu


def test_categorie_inconnue():
    with pytest.raises(ValueError, match="taxi"):
        montant_rembourse("taxi", 15, "EUR", TAUX)


def test_devise_inconnue():
    with pytest.raises(ValueError):
        montant_rembourse("repas", 10, "CHF", TAUX)


@pytest.mark.parametrize("texte, attendu", [("12.50", 12.5), ("12,50", 12.5), (" 3 ", 3.0)])
def test_lire_montant(texte, attendu):
    assert lire_montant(texte) == attendu


@pytest.mark.parametrize("texte", ["-5", "douze", "", "nan", "inf", "-inf"])
def test_lire_montant_invalide(texte):
    with pytest.raises(ValueError):
        lire_montant(texte)


def test_formater_euros():
    assert formater_euros(180.3) == "180,30 EUR"


def test_taux_du_fichier():
    assert charger_taux() == TAUX
