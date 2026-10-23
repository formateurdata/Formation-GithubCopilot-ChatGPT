import csv
import sys


def norm(t):
    t = t.replace(" ", "").replace(".", "")
    if t.startswith("+33"):
        t = t[3:]
    return int(t)


def charger(f, vus=[]):
    res = []
    for l in csv.DictReader(open(f, encoding="utf-8"), delimiter=";"):
        try:
            e = l["email"].strip()
            if e in vus:
                continue
            vus.append(e)
            res.append({"nom": l["nom"].strip().title(), "email": e, "tel": norm(l["telephone"])})
        except:
            pass
    return res


if __name__ == "__main__":
    for c in charger(sys.argv[1]):
        print(c["nom"], c["email"], c["tel"])
