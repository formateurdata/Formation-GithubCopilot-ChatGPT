"""Tests d'acceptation du TP3 : ne pas les modifier.

Les tests du script hérité l'exécutent comme un utilisateur (boîte noire) : la structure
interne de votre correction est libre. La partie API se vérifie aussi séparément
avec test_api_catalogue.py, sans clé ni réseau.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ICI = Path(__file__).resolve().parent
SCRIPT = ICI / "legacy" / "notes_frais.py"
DONNEES = ICI / "donnees" / "notes_septembre.csv"


def lancer(dossier_courant: Path) -> str:
    resultat = subprocess.run([sys.executable, str(SCRIPT), str(DONNEES)], cwd=dossier_courant,
                              capture_output=True, text=True, timeout=30)
    assert resultat.returncode == 0, resultat.stderr
    return resultat.stdout


# Étapes 2 et 4 : le script applique SPEC.md -------------------------------------

@pytest.mark.parametrize("ligne_attendue", [
    "Diallo : 48,92 EUR",   # 25,00 (repas plafonné) + 23,92 (26 USD convertis, sous le plafond)
    "Martin : 180,30 EUR",  # 18,00 + 120,00 (hotel plafonné après conversion) + 42,30
    "Nguyen : 251,40 EUR",  # 21,40 (virgule décimale) + 230,00
])
def test_totaux_conformes_a_la_spec(ligne_attendue):
    assert ligne_attendue in lancer(ICI).splitlines()


def test_categorie_inconnue_signalee():
    sortie = lancer(ICI)
    assert "taxi" in sortie


def test_fonctionne_depuis_un_autre_dossier():
    assert "Martin : 180,30 EUR" in lancer(ICI / "legacy").splitlines()


# Étape 1 : les failles relevées en revue sont corrigées ----------------------------

def test_plus_de_eval():
    assert "eval(" not in SCRIPT.read_text(encoding="utf-8")


def test_plus_de_mot_de_passe_en_clair():
    assert "Factures-2024!" not in SCRIPT.read_text(encoding="utf-8")
