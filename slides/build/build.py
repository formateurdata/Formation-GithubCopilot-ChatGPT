"""Génère slides/formation.pptx à partir du template.

Usage :
  uv run python slides/build/build.py
  uv run python slides/build/build.py --rapport   (ordre des clics, sans arrêt sur erreur)
"""

import importlib
import json
import sys
from pathlib import Path

from deck import ROOT, Deck

OUTPUT_DIR = ROOT / "slides"
BUILD_DIR = Path(__file__).parent
NOM = "formation"


def animation_report(deck):
    lines = []
    for number, steps in deck.animation_report:
        lines.append(f"Slide {number} : {len(steps)} clic(s)")
        lines.extend(f"  [Clic {i}] {text}" for i, text in enumerate(steps, start=1))
    return "\n".join(lines) + "\n"


def build(report_only=False):
    deck = Deck()
    importlib.import_module(NOM).build(deck)
    deck._finish_slide()
    (BUILD_DIR / f"{NOM}_animations.txt").write_text(animation_report(deck), encoding="utf-8")
    if report_only:
        print(f"{NOM} : rapport d'animation écrit, {len(deck.problems)} problème(s)")
        for problem in deck.problems:
            print(f"  {problem}")
        return
    if deck.problems:
        sys.exit(f"{NOM} non généré :\n  " + "\n  ".join(deck.problems))
    output = OUTPUT_DIR / f"{NOM}.pptx"
    deck.save(output)
    # Extraits de code des slides, relus par check_snippets.py
    snippets = [{"slide": slide, "source": source, "runnable": runnable, "lang": lang}
                for slide, source, runnable, lang in deck.snippets]
    (BUILD_DIR / f"{NOM}_snippets.json").write_text(
        json.dumps(snippets, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{output.relative_to(ROOT)} : {len(deck.prs.slides)} slides, {len(snippets)} extraits de code")


if __name__ == "__main__":
    build("--rapport" in sys.argv[1:])
