"""Calcul des remboursements de notes de frais (corrigé du TP3).

Les règles métier sont dans SPEC.md : conversion en euros, puis plafond par dépense,
rejet signalé des catégories inconnues.

Usage : uv run python legacy/notes_frais.py donnees/notes_septembre.csv
"""

import csv
import json
import math
import sys
from pathlib import Path

PLAFONDS = {"repas": 25.00, "hotel": 120.00, "transport": None}
# Chemin relatif au script, pour que le calcul marche quel que soit le dossier courant
FICHIER_TAUX = Path(__file__).resolve().parent.parent / "taux.json"


def charger_taux(chemin: Path = FICHIER_TAUX) -> dict[str, float]:
    """Lit les taux de conversion vers l'euro (JSON : {"USD": 0.92, ...})."""
    with open(chemin, encoding="utf-8") as fichier:
        return json.load(fichier)


def lire_montant(texte: str) -> float:
    """Convertit "12,50" ou "12.50" en nombre. Lève ValueError si le montant est illisible, non fini ou négatif."""
    montant = float(texte.strip().replace(",", "."))
    if not math.isfinite(montant) or montant < 0:
        raise ValueError(f"montant invalide : {texte}")
    return montant


def montant_rembourse(categorie: str, montant: float, devise: str, taux: dict[str, float]) -> float:
    """Montant remboursé en euros : conversion d'abord, plafond ensuite, arrondi au centime.

    Lève ValueError si la catégorie ou la devise est inconnue.
    """
    if categorie not in PLAFONDS:
        raise ValueError(f"catégorie inconnue : {categorie}")
    if devise not in taux:
        raise ValueError(f"devise inconnue : {devise}")
    en_euros = montant * taux[devise]
    plafond = PLAFONDS[categorie]
    if plafond is not None:
        en_euros = min(en_euros, plafond)
    return round(en_euros, 2)


def traiter(chemin_csv, taux: dict[str, float]) -> tuple[dict[str, float], list[str]]:
    """Totaux remboursés par salarié, et liste des dépenses rejetées avec leur motif."""
    totaux: dict[str, float] = {}
    rejets: list[str] = []
    with open(chemin_csv, encoding="utf-8", newline="") as fichier:
        for numero, ligne in enumerate(csv.DictReader(fichier, delimiter=";"), start=2):
            try:
                rembourse = montant_rembourse(ligne["categorie"], lire_montant(ligne["montant"]),
                                              ligne["devise"], taux)
            except ValueError as erreur:
                rejets.append(f"ligne {numero}, {ligne['salarie']} : {erreur}")
                continue
            totaux[ligne["salarie"]] = round(totaux.get(ligne["salarie"], 0) + rembourse, 2)
    return totaux, rejets


def formater_euros(montant: float) -> str:
    """123.4 -> "123,40 EUR"."""
    return f"{montant:.2f}".replace(".", ",") + " EUR"


def main(chemin_csv: str) -> None:
    totaux, rejets = traiter(chemin_csv, charger_taux())
    for salarie in sorted(totaux):
        print(f"{salarie} : {formater_euros(totaux[salarie])}")
    if rejets:
        print("Dépenses rejetées :")
        for rejet in rejets:
            print(f"- {rejet}")


if __name__ == "__main__":
    main(sys.argv[1])
