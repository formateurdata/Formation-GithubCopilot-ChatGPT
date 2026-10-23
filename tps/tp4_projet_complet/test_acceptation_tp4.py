"""Tests d'acceptation du TP4 : ne pas les modifier."""

from pathlib import Path

import pytest

from changelog import Commit, analyser_ligne, generer_changelog, lire_commits

ICI = Path(__file__).resolve().parent


@pytest.mark.parametrize("ligne, attendu", [
    ("9f2c1ab|2026-10-08|feat(api)!: supprime la route /v1",
     Commit("9f2c1ab", "2026-10-08", "feat", "api", "supprime la route /v1", True)),
    ("1d4a389|2026-10-03|feat: mode sombre",
     Commit("1d4a389", "2026-10-03", "feat", None, "mode sombre", False)),
    ("2e5b49a|2026-10-04|fix: un créneau oublié",
     Commit("2e5b49a", "2026-10-04", "fix", None, "un créneau oublié", False)),
    ("aaaaaaa|2026-10-01|refactor!: renomme le module",
     Commit("aaaaaaa", "2026-10-01", "refactor", None, "renomme le module", True)),
])
def test_analyser_ligne_conforme(ligne, attendu):
    assert analyser_ligne(ligne) == attendu


@pytest.mark.parametrize("ligne", [
    "4a7d6bc|2026-10-06|Merge branch 'main' into feature/export",
    "4a7d6bc|2026-10-06|Feat: majuscule non conforme",
    "4a7d6bc|2026-10-06|feat sans deux-points",
    "4a7d6bc|feat: champ manquant",
])
def test_analyser_ligne_non_conforme(ligne):
    assert analyser_ligne(ligne) is None


def test_lire_commits_separe_reconnus_et_rejetes():
    commits, rejetees = lire_commits((ICI / "commits.txt").read_text(encoding="utf-8"))
    assert len(commits) == 9
    assert rejetees == ["4a7d6bc|2026-10-06|Merge branch 'main' into feature/export"]
    assert commits[0].hash == "9f2c1ab"


def test_lire_commits_ignore_les_lignes_vides():
    commits, rejetees = lire_commits("\n1d4a389|2026-10-03|feat: mode sombre\n\n")
    assert len(commits) == 1 and rejetees == []


CHANGELOG_ATTENDU = """## 2.0.0 - 2026-10-09

### Changements incompatibles

- **api** : supprime l'ancienne route /v1/reservations (9f2c1ab)

### Nouveautés

- **export** : export CSV des réservations (5b8e7cd)
- mode sombre de l'interface (1d4a389)

### Corrections

- **export** : les dates du CSV sont au format ISO (8e1b0cd)
- un créneau de fin de journée n'était pas proposé (2e5b49a)

### Performances

- **planning** : index sur la date de début (3f6c5ab)

### Documentation

- guide d'installation sous Windows (7d0a9ef)
"""


def test_generer_changelog_complet():
    commits, _ = lire_commits((ICI / "commits.txt").read_text(encoding="utf-8"))
    assert generer_changelog(commits, "2.0.0", "2026-10-09") == CHANGELOG_ATTENDU


def test_generer_changelog_omet_les_sections_vides():
    commits = [Commit("1d4a389", "2026-10-03", "feat", None, "mode sombre")]
    assert generer_changelog(commits, "1.1.0", "2026-10-09") == (
        "## 1.1.0 - 2026-10-09\n\n### Nouveautés\n\n- mode sombre (1d4a389)\n")


def test_generer_changelog_sans_commit_retenu():
    commits = [Commit("0c39278", "2026-10-02", "test", None, "couverture")]
    assert generer_changelog(commits, "1.0.1", "2026-10-09") == "## 1.0.1 - 2026-10-09\n"
