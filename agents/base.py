import ollama

def call_ollama(model: str, prompt: str, system_prompt: str = "") -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    try:
        resp = ollama.chat(model=model, messages=messages, stream=False)
        return resp["message"]["content"]
    except Exception as e:
        return f"Ollama hatası: {str(e)}. Model '{model}' kurulu mu? ('ollama pull {model}')"

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()