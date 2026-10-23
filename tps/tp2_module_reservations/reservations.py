"""Réservations des salles de formation (TP2).

Une salle se réserve par créneaux, dans une seule journée, entre 9 h et 18 h.
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

OUVERTURE = time(9, 0)
FERMETURE = time(18, 0)


@dataclass(frozen=True)
class Reservation:
    salle: str
    debut: datetime
    fin: datetime
    formateur: str


class ConflitDeReservation(Exception):
    """Levée quand une réservation chevauche une réservation existante de la même salle."""


# ---------------------------------------------------------------------------
# Étape 1 : à faire écrire par Copilot (supprimer chaque raise NotImplementedError)


def chevauche(a: Reservation, b: Reservation) -> bool:
    """Vrai si a et b concernent la même salle et se chevauchent dans le temps.

    Deux réservations qui se touchent (a.fin == b.debut) ne se chevauchent pas.
    """
    raise NotImplementedError


def ajouter(planning: list[Reservation], nouvelle: Reservation) -> list[Reservation]:
    """Renvoie un nouveau planning, trié par début, qui contient `nouvelle`.

    Le planning reçu n'est pas modifié.
    Lève ValueError si nouvelle.fin <= nouvelle.debut, ou si la réservation ne tient pas
    dans une seule journée entre OUVERTURE et FERMETURE.
    Lève ConflitDeReservation si elle chevauche une réservation existante.
    """
    raise NotImplementedError


def taux_occupation(planning: list[Reservation], salle: str, jour: date) -> float:
    """Part de la journée d'ouverture (9 h - 18 h) où la salle est réservée.

    Résultat entre 0 et 1, arrondi à 2 décimales. Une journée sans réservation donne 0.0.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Étape 3 : fonction fournie, elle contient un bug


def creneaux_libres(planning: list[Reservation], salle: str, jour: date) -> list[tuple[time, time]]:
    """Créneaux libres de la salle ce jour-là, entre OUVERTURE et FERMETURE, dans l'ordre.

    Une journée sans réservation donne [(OUVERTURE, FERMETURE)].
    """
    reservations = sorted((r for r in planning if r.salle == salle and r.debut.date() == jour),
                          key=lambda r: r.debut)
    libres = []
    curseur = OUVERTURE
    for r in reservations:
        if r.debut.time() > curseur:
            libres.append((curseur, r.debut.time()))
        curseur = r.fin.time()
    return libres


# ---------------------------------------------------------------------------
# Étape 4 : fonction fournie, à refactoriser sans changer son résultat


def rapport_hebdomadaire(planning, lundi):
    lignes = []
    lignes.append("Semaine du " + lundi.strftime("%d/%m/%Y"))
    salles = []
    for r in planning:
        if r.salle not in salles:
            salles.append(r.salle)
    salles.sort()
    for s in salles:
        lignes.append("Salle " + s)
        total = 0
        for i in range(5):
            j = lundi + timedelta(days=i)
            minutes = 0
            for r in planning:
                if r.salle == s and r.debut.date() == j:
                    minutes = minutes + (r.fin - r.debut).seconds // 60
            t = minutes / 540
            total = total + minutes
            noms = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]
            lignes.append("  " + noms[i] + " : " + str(round(t * 100)) + " %")
        lignes.append("  semaine : " + str(round(total / (540 * 5) * 100)) + " %")
    return "\n".join(lignes)



def charger_csv(chemin) -> list[Reservation]:
    """Lit salle;debut;fin;formateur, avec des dates ISO, en passant par ajouter()."""
    # TODO : utiliser le bloc d'aide de la partie 6 et faire relire la validation par Copilot.
    raise NotImplementedError
