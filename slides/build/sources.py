"""Références des sources citées dans les notes du formateur (relevé du 09/10/2026)."""

PLAN = "plan/programme-GHCG.md (page PLB)"
DEROULE = "plan/deroule.md"

VSCODE = "https://code.visualstudio.com/docs/"
GITHUB = "https://docs.github.com/en/copilot/"
OPENAI = "https://developers.openai.com/api/docs/"
# Documentation Codex : developers.openai.com/codex redirige vers learn.chatgpt.com/docs (relevé du 09/10/2026)
CODEX = "https://learn.chatgpt.com/docs/"
RELEVE = "relevé du 09/10/2026"


def vsc(page, titre):
    return f"documentation VS Code, {titre} ({VSCODE}{page}), {RELEVE}"


def gh(page, titre):
    return f"documentation GitHub Copilot, {titre} ({GITHUB}{page}), {RELEVE}"


def oai(page, titre):
    return f"documentation API OpenAI, {titre} ({OPENAI}{page}), {RELEVE}"


def codex(page, titre):
    return f"documentation Codex, {titre} ({CODEX}{page}), {RELEVE}"


AIDE_CHATGPT = ("centre d'aide OpenAI, Data controls in ChatGPT "
                "(https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt), "
                f"{RELEVE}")

MEMOIRE = ("centre d'aide OpenAI, Memory in ChatGPT "
           "(https://help.openai.com/en/articles/8590148-memory-in-chatgpt), vérifié le 22/10/2026")
TEMPORAIRE = ("centre d'aide OpenAI, Temporary chat in ChatGPT "
              "(https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt), vérifié le 22/10/2026")
FACTURATION = ("centre d'aide OpenAI, Managing billing for ChatGPT and the API platform "
               "(https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform), "
               "vérifié le 22/10/2026")
EXCLUSION = ("documentation GitHub, Content exclusion "
             "(https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/content-exclusion), "
             "vérifié le 22/10/2026")
