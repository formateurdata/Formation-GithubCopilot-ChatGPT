"""Exemples de tests à exécuter avec la commande de chat /run-test."""

import pytest

from livraison import frais_de_port


@pytest.mark.parametrize(
    "montant, attendu",
    [(0, 4.90), (49.99, 4.90), (50, 0.0), (50.01, 0.0), (100, 0.0)],
)
def test_frais_de_port(montant, attendu):
    assert frais_de_port(montant) == attendu
