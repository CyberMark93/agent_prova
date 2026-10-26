"""Client sincrono per un modello locale (LM Studio, JSON su HTTP).

Senza argomenti: una sola chiamata con domanda fissa. Con --chat: ciclo di
conversazione. La risposta arriva sempre in streaming, stampata a frammenti.
"""
import argparse
import json
import os
import sys
import requests
from dotenv import load_dotenv

SYSTEM_PROMPT = "Rispondi in italiano."
QUESTION = "Che cosa controllare se Python segnala FileNotFoundError?"
TEMPERATURE = 0.2
MAX_TOKENS_SINGLE = 512
MAX_TOKENS_CHAT = 512
EXIT_WORD = "esci"
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

def load_config(path=ENV_PATH):
    """Legge LM_BASE_URL e LM_MODEL da .env; esce con messaggio chiaro se mancano."""
    if not os.path.isfile(path):
        sys.exit(f"File di configurazione non trovato: {path}. Copia .env.example in .env e compilalo.")
    load_dotenv(path, override=False)
    base_url = os.environ.get("LM_BASE_URL")
    model = os.environ.get("LM_MODEL")
    if not base_url or not model:
        missing = [k for k, v in (("LM_BASE_URL", base_url), ("LM_MODEL", model)) if not v]
        sys.exit(f"Config mancante: {', '.join(missing)}. Compila il file .env.")
    return base_url.rstrip("/"), model

def build_payload(model, messages, max_tokens):
    """Costruisce il corpo JSON della richiesta (risposta in streaming)."""
    return {
        "model": model,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": max_tokens,
        "stream": True,
    }

def send_request(base_url, payload, prefix=""):
    """POST in streaming su {base_url}/chat/completions; stampa i frammenti via via
    e restituisce il testo completo e il finish_reason."""
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            json=payload,
            timeout=(5, 120),
            stream=True,
        )
    except requests.exceptions.Timeout:
        sys.exit("Attesa scaduta: controllare server, carico e tempi.")
    except requests.exceptions.ConnectionError:
        sys.exit(
            f"Connessione fallita su {base_url}: controllare server, URL e porta. "
            "Avvialo con: lms server start"
        )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        sys.exit(f"Errore HTTP: {response.status_code} {response.text}")

    print(prefix, end="", flush=True)
    testo = ""
    finish_reason = None
    with response:
        for riga in response.iter_lines():
            if not riga:
                continue
            riga = riga.decode("utf-8")
            if not riga.startswith("data: "):
                continue
            dati = riga[len("data: "):]
            if dati == "[DONE]":
                break
            chunk = json.loads(dati)["choices"][0]
            frammento = chunk.get("delta", {}).get("content") or ""
            if frammento:
                print(frammento, end="", flush=True)
                testo += frammento
            if chunk.get("finish_reason"):
                finish_reason = chunk["finish_reason"]
    print()
    return testo, finish_reason

def warn_if_incomplete(reply, finish_reason):
    """Segnala risposta vuota o troncata (il modello ragiona prima di rispondere)."""
    if not reply.strip():
        print("[Risposta vuota: token esauriti nel ragionamento. Riprova o alza MAX_TOKENS.]")
    elif finish_reason == "length":
        print("[Risposta troncata dal limite di token.]")

def run_single(base_url, model):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": QUESTION},
    ]
    reply, finish_reason = send_request(base_url, build_payload(model, messages, MAX_TOKENS_SINGLE))
    warn_if_incomplete(reply, finish_reason)

def run_chat(base_url, model):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print(f"Chat con {model}. Scrivi '{EXIT_WORD}' o premi Ctrl+C per uscire.")
    while True:
        try:
            text = input("Tu> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not text:
            continue
        if text.lower() == EXIT_WORD:
            break
        messages.append({"role": "user", "content": text})
        try:
            reply, finish_reason = send_request(
                base_url, build_payload(model, messages, MAX_TOKENS_CHAT), prefix="Gemma> "
            )
        except KeyboardInterrupt:
            print()
            break
        if not reply.strip():
            messages.pop()
            warn_if_incomplete(reply, finish_reason)
            continue
        messages.append({"role": "assistant", "content": reply})
        warn_if_incomplete(reply, finish_reason)

def main():
    parser = argparse.ArgumentParser(description="Client per modello locale (LM Studio).")
    parser.add_argument("--chat", action="store_true", help="avvia il ciclo di conversazione")
    args = parser.parse_args()
    base_url, model = load_config()
    if args.chat:
        run_chat(base_url, model)
    else:
        run_single(base_url, model)

if __name__ == "__main__":
    main()
