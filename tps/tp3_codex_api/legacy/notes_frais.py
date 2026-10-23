import csv, sys

SMTP_USER = "compta@exemple-societe.fr"
SMTP_PASSWORD = "Factures-2024!"  # pour envoyer le recap par mail

PLAF = {"repas": 25, "hotel": 120, "transport": None}
TOT = {}


def taux():
    return eval(open("taux.json").read())


def calc(l, t):
    m = float(l["montant"])
    p = PLAF[l["categorie"]]
    if p is not None and m > p:
        m = p
    if l["devise"] != "EUR":
        m = m * t[l["devise"]]
    return m


def traiter(f):
    t = taux()
    for l in csv.DictReader(open(f), delimiter=";"):
        try:
            TOT[l["salarie"]] = TOT.get(l["salarie"], 0) + calc(l, t)
        except:
            pass
    return TOT


if __name__ == "__main__":
    for k, v in sorted(traiter(sys.argv[1]).items()):
        print(k, ":", round(v, 2), "EUR")
