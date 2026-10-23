"""Générateur de CHANGELOG à partir de l'historique Git (TP4).

Usage : uv run python changelog.py commits.txt 2.0.0 [--date 2026-10-09]
Le fichier commits.txt est produit par :
    git log --pretty=format:"%h|%ad|%s" --date=short > commits.txt

Les signatures et les docstrings ci-dessous sont le contrat d'interface convenu avec
l'équipe : les tests d'acceptation s'appuient dessus. Le corps des fonctions est à écrire.
"""

import argparse
import datetime
import sys
from dataclasses import dataclass
from pathlib import Path

# Sections du changelog, dans l'ordre d'affichage, après les changements incompatibles
SECTIONS = [("feat", "Nouveautés"), ("fix", "Corrections"), ("perf", "Performances"), ("docs", "Documentation")]
TITRE_INCOMPATIBLES = "Changements incompatibles"


@dataclass(frozen=True)
class Commit:
    hash: str
    date: str
    type: str
    portee: str | None
    description: str
    incompatible: bool = False


def analyser_ligne(ligne: str) -> Commit | None:
    """Analyse une ligne "hash|date|message" produite par git log.

    Le message suit Conventional Commits : "type(portee)!: description", où la portée
    et le "!" (changement incompatible) sont facultatifs et le type est en minuscules.
    Renvoie None si la ligne n'a pas trois champs ou si le message ne respecte pas ce format.

    >>> analyser_ligne("9f2c1ab|2026-10-08|feat(api)!: supprime la route /v1")
    Commit(hash='9f2c1ab', date='2026-10-08', type='feat', portee='api', description='supprime la route /v1', incompatible=True)
    """
    raise NotImplementedError


def lire_commits(texte: str) -> tuple[list[Commit], list[str]]:
    """Analyse chaque ligne non vide du texte.

    Renvoie les commits reconnus et les lignes rejetées, chacun dans l'ordre du texte.
    """
    raise NotImplementedError


def generer_changelog(commits: list[Commit], version: str, date: str) -> str:
    """Section Markdown d'une version, prête à coller en tête de CHANGELOG.md.

    - Titre : "## <version> - <date>".
    - Sections "### <titre>", dans l'ordre : TITRE_INCOMPATIBLES, puis celles de SECTIONS.
    - Un commit incompatible apparaît seulement dans TITRE_INCOMPATIBLES, quel que soit son type.
    - Les types absents de SECTIONS (chore, test, ci...) sont ignorés, sauf s'ils sont incompatibles.
    - Une ligne par commit : "- **portee** : description (hash)", ou "- description (hash)" sans portée.
    - Les commits gardent l'ordre de la liste ; une section vide n'apparaît pas.
    - Une ligne vide après chaque titre et après chaque liste.
    """
    raise NotImplementedError


def main(arguments: list[str] | None = None) -> None:
    analyseur = argparse.ArgumentParser(description="Génère la section CHANGELOG d'une version.")
    analyseur.add_argument("fichier", type=Path, help="sortie de git log au format %%h|%%ad|%%s")
    analyseur.add_argument("version", help="numéro de la version, par exemple 2.0.0")
    analyseur.add_argument("--date", default=datetime.date.today().isoformat())
    options = analyseur.parse_args(arguments)
    commits, rejetees = lire_commits(options.fichier.read_text(encoding="utf-8"))
    print(generer_changelog(commits, options.version, options.date), end="")
    for ligne in rejetees:
        print(f"Ligne ignorée (format non conforme) : {ligne}", file=sys.stderr)


if __name__ == "__main__":
    main()
