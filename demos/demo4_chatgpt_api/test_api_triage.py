"""Teste l'intégration du triage sans clé ni réseau."""

import json
from types import SimpleNamespace

import pytest

from triage_support import TriageTicket, classer_ticket

TICKET = {"reference": "SUP-2041", "objet": "Paiement", "message": "Deux débits pour une commande."}


class FauxClient:
    def __init__(self, triage):
        self.triage = triage
        self.appels = []
        self.responses = SimpleNamespace(parse=self._parse)

    def _parse(self, **arguments):
        self.appels.append(arguments)
        return SimpleNamespace(output_parsed=self.triage)


def test_transmet_le_ticket_et_recupere_un_classement():
    triage = TriageTicket(categorie="paiement", priorite="haute", resume="Deux débits signalés.")
    client = FauxClient(triage)
    assert classer_ticket({**TICKET, "note_interne": "ne pas transmettre"}, client, "modele-test") == triage
    assert len(client.appels) == 1
    appel = client.appels[0]
    assert json.loads(appel["input"]) == TICKET
    assert appel["model"] == "modele-test"
    assert appel["text_format"] is TriageTicket
    assert appel["store"] is False
    assert "Priorité haute" in appel["instructions"]


def test_reponse_absente_refusee():
    with pytest.raises(ValueError, match="Aucun triage structuré"):
        classer_ticket(TICKET, FauxClient(None))


def test_categorie_inconnue_refusee():
    client = FauxClient({"categorie": "remboursement", "priorite": "haute", "resume": "Deux débits."})
    with pytest.raises(ValueError):
        classer_ticket(TICKET, client)


def test_erreur_api_transmise():
    def echouer(**arguments):
        raise RuntimeError("API indisponible")

    with pytest.raises(RuntimeError, match="API indisponible"):
        classer_ticket(TICKET, SimpleNamespace(responses=SimpleNamespace(parse=echouer)))
