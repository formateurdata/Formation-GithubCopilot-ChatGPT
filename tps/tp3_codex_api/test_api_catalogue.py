"""Acceptation de la partie catalogue : faux client, aucune clé et aucun réseau."""

import copy
import json
from types import SimpleNamespace

import pytest

from catalogue import FicheProduit, ajouter_article, generer_fiche

ARTICLE = {"reference": "BOI-02", "nom": "Boîte Empil",
           "caracteristiques": {"matiere": "polypropylène", "couleur": "transparent"}}


class FauxClient:
    def __init__(self, fiche=None, erreur=None):
        self.fiche = fiche
        self.erreur = erreur
        self.appels = []
        self.responses = SimpleNamespace(parse=self._parse)

    def _parse(self, **arguments):
        self.appels.append(arguments)
        if self.erreur:
            raise self.erreur
        return SimpleNamespace(output_parsed=self.fiche)


def fiche_exemple():
    return FicheProduit(titre="Boîte Empil", description="Une boîte en polypropylène.",
                        points_forts=["Couleur transparente"])


def test_generer_transmet_uniquement_les_faits_publics():
    client = FauxClient(fiche_exemple())
    article = {**ARTICLE, "cout_achat": "3 EUR", "note_interne": "marge confidentielle"}
    fiche = generer_fiche(article, client, modele="modele-test")
    assert fiche == fiche_exemple()
    assert len(client.appels) == 1
    appel = client.appels[0]
    assert json.loads(appel["input"]) == ARTICLE
    assert appel["model"] == "modele-test"
    assert appel["text_format"] is FicheProduit
    assert appel["store"] is False
    assert appel["instructions"]


def test_aucune_fiche_sur_reponse_absente():
    with pytest.raises(ValueError, match="Aucune fiche structurée"):
        generer_fiche(ARTICLE, FauxClient())


def test_ajout_declenche_une_generation_et_conserve_l_existant():
    existant = {"reference": "CAB-01", "fiche": {"description": "Texte déjà validé"}, "statut": "valide"}
    catalogue = [existant]
    avant = copy.deepcopy(catalogue)
    client = FauxClient(fiche_exemple())
    resultat = ajouter_article(catalogue, ARTICLE, client, modele="modele-test")
    assert catalogue == avant
    assert resultat is not catalogue
    assert resultat[0] == existant
    assert len(resultat) == 2
    assert resultat[1] == {**ARTICLE, "fiche": fiche_exemple().model_dump(), "statut": "brouillon"}
    assert len(client.appels) == 1
    assert client.appels[0]["model"] == "modele-test"


def test_doublon_refuse_sans_depense_api():
    client = FauxClient(fiche_exemple())
    with pytest.raises(ValueError, match="déjà présente"):
        ajouter_article([ARTICLE], ARTICLE, client)
    assert client.appels == []


def test_echec_api_ne_modifie_pas_le_catalogue():
    catalogue = [{"reference": "CAB-01", "statut": "valide"}]
    avant = copy.deepcopy(catalogue)
    client = FauxClient(erreur=RuntimeError("API indisponible"))
    with pytest.raises(RuntimeError, match="API indisponible"):
        ajouter_article(catalogue, ARTICLE, client)
    assert catalogue == avant


@pytest.mark.parametrize("champ", ["reference", "nom", "caracteristiques"])
def test_article_incomplet_refuse_avant_appel(champ):
    article = {k: v for k, v in ARTICLE.items() if k != champ}
    client = FauxClient(fiche_exemple())
    with pytest.raises(ValueError):
        generer_fiche(article, client)
    assert client.appels == []
