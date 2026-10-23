"""La vérification globale exécute les secours, pas les bugs de départ.

Les démos 2 et 3 ont leur propre pytest.ini : ouvertes seules dans VS Code,
elles collectent leurs tests de départ et ignorent final/.
"""

collect_ignore = [
    "demo2_copilot_avance/test_panier.py",
    "demo3_codex_vscode/test_versions.py",
]
