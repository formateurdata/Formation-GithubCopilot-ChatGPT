"""Vérifie les extraits Python des slides : exécution des extraits autonomes, syntaxe des autres.

Usage : uv run python slides/build/check_snippets.py
Les extraits qui appellent l'API OpenAI ne sont pas exécutés (pas de clé) : syntaxe seulement.
"""

import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

PRELUDE = "import re\nimport pytest\n"


def check(name="formation"):
    snippets = json.loads((Path(__file__).parent / f"{name}_snippets.json").read_text(encoding="utf-8"))
    python = [item for item in snippets if item.get("lang", "python") == "python"]
    failures = 0
    with tempfile.TemporaryDirectory() as workdir:
        os.chdir(workdir)
        for item in python:
            try:
                if item["runnable"]:
                    exec(PRELUDE + item["source"], {"__name__": "__snippet__"})
                else:
                    compile(item["source"], f"slide {item['slide']}", "exec")
            except Exception:
                failures += 1
                print(f"--- slide {item['slide']} : ECHEC")
                print(item["source"])
                traceback.print_exc()
    runnable = sum(1 for item in python if item["runnable"])
    print(f"{name} : {len(python) - failures}/{len(python)} extraits Python sans erreur "
          f"({runnable} exécutés, {len(python) - runnable} vérifiés en syntaxe) ; "
          f"{len(snippets) - len(python)} extraits non Python (Markdown, JSON, shell) non vérifiés")
    return failures


if __name__ == "__main__":
    sys.exit(check())
