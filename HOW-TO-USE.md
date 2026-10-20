# HOW-TO-USE

> Manutenzione: questo file descrive il funzionamento **effettivo** del codice allo stato attuale. Va aggiornato nello stesso turno in cui cambia un comportamento osservabile di `client.py`, `requirements.txt` o `.env.example` — non a posteriori. Per lo stato di avanzamento dei moduli di allineamento al corso, vedi `TODO.MD`.

## Cos'è questo progetto

Un client Python sincrono con una sola responsabilità: inviare una richiesta a un modello LLM in esecuzione locale su **LM Studio** e stamparne la risposta testuale. Non è un agente (nessun tool-calling, nessuna pianificazione), non contiene pesi del modello, non ha interfaccia grafica.

## Prerequisiti

- **LM Studio** installato, con un modello compatibile scaricato e **caricato** (attualmente configurato: `google/gemma-4-e2b`).
- **Python 3** con supporto a `venv`.

## Preparazione dell'ambiente (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Dipendenze reali installate: `requests` (trasporto HTTP) e `python-dotenv` (lettura `.env`), versioni pinned in `requirements.txt`.

```powershell
Copy-Item .env.example .env
notepad .env
```

Variabili obbligatorie in `.env`:

| Variabile | Significato | Esempio |
|---|---|---|
| `LM_BASE_URL` | Indirizzo del server LM Studio | `http://localhost:1234/v1` |
| `LM_MODEL` | ID del modello, esattamente come restituito da `GET /v1/models` | `google/gemma-4-e2b` |

Avvio del server:

```powershell
lms server start
lms server status
```

## Esecuzione

**Modalità singola** (domanda fissa, una sola chiamata):

```powershell
.\.venv\Scripts\python.exe client.py
```

Invia `SYSTEM_PROMPT` ("Rispondi in italiano.") + `QUESTION` ("Che cosa controllare se Python segnala FileNotFoundError?"), stampa il testo di risposta.

**Modalità chat** (ciclo di conversazione):

```powershell
.\.venv\Scripts\python.exe client.py --chat
```

Legge domande da terminale (`input()`), mantiene la cronologia della conversazione in una lista Python in memoria (persa alla chiusura del processo), la reinvia per intero a ogni turno. Uscita con la parola `esci` o `Ctrl+C`.

## Comportamento sui limiti di token

`MAX_TOKENS_SINGLE` / `MAX_TOKENS_CHAT` = 512. Se la risposta arriva vuota o troncata (`finish_reason == "length"`), il client stampa un avviso esplicito invece di restituire silenziosamente testo incompleto — rilevante perché il modello configurato consuma parte del budget in ragionamento interno prima del testo finale visibile.

## Messaggi di errore — cosa significano

| Messaggio | Causa | Cosa controllare |
|---|---|---|
| `File di configurazione non trovato: ...` | `.env` assente | Copiare `.env.example` in `.env` |
| `Config mancante: LM_BASE_URL, LM_MODEL` | Una o entrambe le variabili sono vuote/assenti in `.env` | Aprire `.env` e compilarle |
| `Server non raggiungibile su ... Avvialo con: lms server start` | LM Studio non è in ascolto, oppure URL/porta errati | `lms server status`; verificare `LM_BASE_URL` |

**Limite noto, in lavorazione (Modulo C di `TODO.MD`):** un errore HTTP del server (es. ID modello inesistente, richiesta malformata) produce al momento un traceback Python grezzo, non un messaggio comprensibile — il ramo che lo gestisce nel codice lo rilancia senza stamparlo. Non confondere questo caso con "server non raggiungibile": il server qui risponde, ma con un errore.

## Limiti noti allo stato attuale

- Nessuno streaming: la risposta arriva tutta insieme a generazione completata, non a frammenti.
- La cronologia della chat vive solo nella memoria del processo: nessun file, nessun database, persa a ogni riavvio.
- Nessuna persistenza, nessun tool-calling, nessuna lettura di file esterni da parte del modello.

## Relazione con README.md

`README.md` descrive la preparazione dell'ambiente ma, al momento, non riflette ancora la migrazione a `requests`/`python-dotenv` né la modalità `--chat` (sincronizzazione pianificata nel Modulo E di `TODO.MD`). In caso di discrepanza tra i due documenti, questo file è quello tenuto aggiornato ad ogni modifica di comportamento.
