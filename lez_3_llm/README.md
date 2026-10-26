# client

Client Python sincrono per un modello locale esposto da LM Studio.
Il dialogo avviene in JSON su HTTP (`POST /v1/chat/completions`); la risposta arriva in streaming, stampata a frammenti.

Due modalità:
- **singola** (default): una domanda fissa, una sola chiamata.
- **`--chat`**: ciclo di conversazione, cronologia mantenuta in memoria del processo (persa alla chiusura).

## Preparazione dell'ambiente (PowerShell)

1. Ambiente virtuale e dipendenze (`requests` per il trasporto HTTP, `python-dotenv` per la lettura di `.env`):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Configurazione. Copia l'esempio e compila `LM_MODEL` con un ID restituito da `/v1/models`:

   ```powershell
   Copy-Item .env.example .env
   ```

   Variabili obbligatorie in `.env`: `LM_BASE_URL` (default LM Studio: `http://localhost:1234/v1`) e `LM_MODEL`.

3. Server LM Studio:

   ```powershell
   lms server start
   lms server status
   ```

4. Esecuzione:

   ```powershell
   .\.venv\Scripts\python.exe client.py
   .\.venv\Scripts\python.exe client.py --chat
   ```

## Note

- `.env`, `.venv/` e i pesi dei modelli non vanno in Git.
- Non sono presenti test automatici in questo checkpoint.
- Guida funzionale completa (comportamento, messaggi di errore, limiti noti): `HOW-TO-USE.md`.
