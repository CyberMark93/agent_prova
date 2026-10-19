# client

Client Python sincrono con una sola chiamata a un modello locale esposto da LM Studio.
Il dialogo avviene in JSON su HTTP (`POST /v1/chat/completions`).

## Preparazione dell'ambiente (PowerShell)

1. Ambiente virtuale e dipendenze (nessun pacchetto esterno: solo libreria standard):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Configurazione. Copia l'esempio e compila `MODEL` con un ID restituito da `/v1/models`:

   ```powershell
   Copy-Item .env.example .env
   ```

   Variabili obbligatorie in `.env`: `LM_BASE_URL` (default LM Studio: `http://localhost:1234/v1`) e `MODEL`.

3. Server LM Studio:

   ```powershell
   lms server start
   lms server status
   ```

4. Esecuzione:

   ```powershell
   python client.py
   ```

## Note

- `.env`, `.venv/` e i pesi dei modelli non vanno in Git.
- Non sono presenti test automatici in questo checkpoint.
