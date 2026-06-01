from .base import call_ollama, load_prompt
from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "supervisor.md"
SUPER_PROMPT = load_prompt(PROMPT_PATH)

def supervisor_decision(question: str) -> str:
    filled = SUPER_PROMPT.format(question=question)
    resp = call_ollama("llama3", filled)
    resp = resp.strip().lower()
    if "rapor" in resp:
        return "rapor"
    elif "analiz" in resp:
        return "analiz"
    elif "uyari" in resp:
        return "uyari"
    elif "planlama" in resp:
        return "planlama"
    return "rapor"