"""Le parcours applicatif écrit le brouillon seulement si la génération réussit."""

import json
import sys
from types import SimpleNamespace

import openai

from catalogue import FicheProduit, main


def preparer(tmp_path, monkeypatch, fiche):
    catalogue = tmp_path / "catalogue.json"
    article = tmp_path / "article.json"
    sortie = tmp_path / "brouillon.json"
    catalogue.write_text('[]', encoding="utf-8")
    article.write_text(json.dumps({"reference": "BOI-02", "nom": "Boîte",
                                  "caracteristiques": {"matiere": "polypropylène"}}), encoding="utf-8")
    client = SimpleNamespace(responses=SimpleNamespace(parse=lambda **arguments: SimpleNamespace(output_parsed=fiche)))
    monkeypatch.setattr(openai, "OpenAI", lambda: client)
    monkeypatch.setattr(sys, "argv", ["catalogue.py", str(catalogue), str(article), "--sortie", str(sortie)])
    return catalogue, article, sortie


def test_cli_ecrit_un_brouillon_sans_ecraser_les_sources(tmp_path, monkeypatch):
    fiche = FicheProduit(titre="Boîte", description="En polypropylène.", points_forts=["Polypropylène"])
    catalogue, article, sortie = preparer(tmp_path, monkeypatch, fiche)
    original = article.read_text()
    assert main() == 0
    resultat = json.loads(sortie.read_text())
    assert len(resultat) == 1
    assert resultat[0]["reference"] == "BOI-02"
    assert resultat[0]["statut"] == "brouillon"
    assert resultat[0]["fiche"]["description"] == "En polypropylène."
    assert catalogue.read_text() == "[]"
    assert article.read_text() == original


def test_cli_reponse_absente_sans_fichier_de_sortie(tmp_path, monkeypatch):
    catalogue, _, sortie = preparer(tmp_path, monkeypatch, None)
    assert main() == 2
    assert not sortie.exists()
    assert catalogue.read_text() == "[]"


def test_cli_refuse_une_sortie_identique_au_catalogue(tmp_path, monkeypatch):
    catalogue, _, _ = preparer(tmp_path, monkeypatch, None)
    monkeypatch.setattr(sys, "argv", [*sys.argv[:-1], str(catalogue)])
    assert main() == 2
    assert catalogue.read_text() == "[]"
