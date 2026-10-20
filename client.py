"""Client sincrono per un modello locale (LM Studio, JSON su HTTP).

Senza argomenti: una sola chiamata con domanda fissa. Con --chat: ciclo di conversazione.
"""
import argparse
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
    """Costruisce il corpo JSON della richiesta."""
    return {
        "model": model,
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": max_tokens,
        "stream": False,
    }


def send_request(base_url, payload):
    """POST su {base_url}/chat/completions; restituisce il testo della risposta."""
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            json=payload,
            timeout=(5, 120),
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
    data = response.json()
    choice = data["choices"][0]
    return choice["message"]["content"], choice.get("finish_reason")


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
    print(reply)
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
            reply, finish_reason = send_request(base_url, build_payload(model, messages, MAX_TOKENS_CHAT))
        except KeyboardInterrupt:
            print()
            break
        if not reply.strip():
            messages.pop()
            warn_if_incomplete(reply, finish_reason)
            continue
        messages.append({"role": "assistant", "content": reply})
        print(f"Gemma> {reply}")
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
