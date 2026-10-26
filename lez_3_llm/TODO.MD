# TODO — Allineamento al materiale del docente (Lezione 3)

Riferimento: confronto tra `client.py`/repository attuale e `LLM_Lez_3.pdf`. Ordine di lavorazione per dipendenza tecnica, un modulo alla volta, con conferma esplicita prima di passare al successivo.

## 1. Modulo A — Stack di dipendenze — [x] COMPLETATO, confermato

- `requests==2.34.2` e `python-dotenv==1.2.4` pinned in `requirements.txt` (prima: zero dipendenze, solo `urllib`).
- `client.py`: `urllib.request`/`urllib.error` sostituiti da `requests` + `load_dotenv()`.
- Chiave di configurazione rinominata `MODEL` → `LM_MODEL` in `.env` e `.env.example` (conformità al template di slide 18).
- Verificato end-to-end: percorso server-non-raggiungibile (messaggio pulito) e percorso risposta-reale (testo ricevuto da `google/gemma-4-e2b`).

## 2. Modulo C — Gestione errori HTTP — [x] COMPLETATO, confermato

- **Problema attuale**: in `send_request()`, `requests.exceptions.HTTPError` viene catturato e subito rilanciato (`raise`) — nessun messaggio comprensibile. Un 4xx/5xx del server produce un traceback grezzo, non un errore leggibile.
- **Problema attuale**: `requests.exceptions.RequestException` è gestito in blocco unico → un timeout reale (server vivo ma lento) viene riportato come "server non raggiungibile", messaggio fuorviante.
- **Fatto** (rif. slide 24 del PDF): tre rami distinti in `send_request()` — `Timeout`, `ConnectionError`, `HTTPError` (con `status_code` e corpo della risposta) — `timeout` passato a tupla `(5, 120)`. Verificato singolarmente contro il server reale: connessione rifiutata, timeout forzato artificialmente, ID modello inesistente (400 con corpo leggibile). Nessun traceback in nessuno dei tre casi.

## 3. Modulo D — Disciplina dei commit — [x] COMPLETATO — Opzione 2 scelta in via definitiva

- **Problema originale**: il commit `76ceef7 feat: client LM Studio (singola + chat)` bundla Estensione 1 (input da terminale) ed Estensione 3 (history in memoria) in un solo commit, saltando l'Estensione 2 (streaming, implementata solo dopo — vedi sezione dedicata sotto) e senza diff isolabili per estensione — in contrasto con slide 29/31 ("un commit per estensione verificata").
- [x] **Opzione 2 applicata**: da questa sessione in avanti, un commit per unità logica. Esempio: `b90131b refactor(client)` (Modulo A), `1d4793f docs(claude)` (correzioni claude.md), `fccb75e docs` (nuovi file di processo) — tre commit distinti invece di uno bundlato, nonostante la richiesta iniziale fosse "un commit intelligente di tutto il progetto".
- [x] **Opzione 1 scartata in via definitiva**: il commit storico `76ceef7` resta bundlato su `origin/main`. Decisione esplicita dell'utente (non default): nessuna riscrittura di cronologia, nessun force-push.

## 4. Modulo E — Sincronizzazione documentazione — [x] COMPLETATO, confermato

- [x] `CLAUDE.md` non dichiara più "nessuna cronologia" — obiettivo riscritto per riconoscere `--chat`.
- [x] `CLAUDE.md` ora contiene le righe "dopo la prima esecuzione verificata" (comando di avvio, nota di verifica manuale) richieste da slide 11.
- [x] `CLAUDE.md`: regola dipendenze + criterio di approvazione unificati in una checklist riusabile per ogni piano, non più un fatto storico fissato ("nessuna nuova dipendenza" letta alla lettera contraddiceva il Modulo A già confermato).
- [x] Rimossa da `CLAUDE.md` la domanda FileNotFoundError + criteri di riuscita (contenuto di task, non convenzione di progetto per la tassonomia di slide 10) — la domanda resta documentata in `HOW-TO-USE.md`; i criteri sono già coperti in sostanza dalla tabella errori lì presente.
- [x] `README.md` riscritto: dipendenze `requests`/`python-dotenv`, variabile `LM_MODEL`, modalità `--chat`, risposta in streaming, esecuzione con l'interprete della venv. Rimanda a `HOW-TO-USE.md` per i dettagli funzionali (errori, limiti, comportamento sui token).

## 5. Estensione 2 — Streaming — [x] COMPLETATA, confermata (fuori sequenza A/C/D/E)

- **Problema originale**: mai implementata (audit iniziale: `build_payload()` aveva `"stream": False` fisso, nessuna gestione di eventi SSE).
- **Fatto** (rif. slide 27 del PDF): `send_request()` ora invia `"stream": true`, apre la risposta con `requests.post(..., stream=True)`, legge `iter_lines()` fino a `data: [DONE]`, stampa ogni frammento (`flush=True`) e accumula testo + `finish_reason`. `run_single`/`run_chat` non ristampano più il blocco intero (duplicherebbe l'output già stampato a frammenti) — `run_chat` passa `prefix="Gemma> "`.
- Verificato: modalità singola con budget di token alzato temporaneamente (risposta completa, formattata, nessun troncamento), modalità `--chat` con input pipe (prefisso corretto, uscita pulita con `esci`). Ripristinato `MAX_TOKENS_SINGLE` dopo il test.
- Conseguenza per il Modulo D: delle tre estensioni del Blocco 8, ora solo 1 e 3 restano bundlate nel commit storico `76ceef7` — lo streaming (2) non c'entra con quel debito, è stato implementato e committato separatamente in questa sessione.

---

## Promemoria — pulizia finale del codice (dopo il completamento di C, D, E)

Obiettivo dichiarato: consegna al prof **funzionante e ridotta al minimo necessario** — non un esercizio di stile, non funzionalità non richieste.

Prima di consegnare, verificare puntualmente:

- **Nessun codice morto o vestigiale**: niente rami `except` che catturano e rilanciano senza fare nulla (il bug del Modulo C, se non ancora corretto, è l'esempio).
- **Nessuna funzionalità oltre lo scopo dichiarato** in `CLAUDE.md`/PDF (es. se qualcosa è stato aggiunto "perché poteva servire" e non è nei criteri di riuscita, va tolto o giustificato esplicitamente).
- **Coerenza documento↔codice**: ogni file (`CLAUDE.md`, `README.md`, `requirements.txt`) deve descrivere esattamente ciò che il codice fa oggi, non ciò che faceva prima o ciò che potrebbe fare.
- **Tracciabilità degli errori**: per ogni modifica di questo elenco, la diff (`git diff`) resta la fonte primaria per capire cosa è stato cambiato e perché — usarla per isolare manualmente, se preferito, i singoli interventi prima di accettarli definitivamente.
