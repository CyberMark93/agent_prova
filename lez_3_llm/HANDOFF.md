# HANDOFF.md

> Scopo: permettere di riprendere questo lavoro in una **nuova conversazione** quando l'utilizzo del contesto della sessione corrente si avvicina al 40% (soglia di sicurezza scelta dall'utente, non dal codice — nessun meccanismo automatico la rileva: è l'utente a notarla dall'indicatore dell'interfaccia).

## Come usarlo

1. Quando l'utilizzo di contesto è vicino al 40%, chiedi "aggiorna HANDOFF.md" **prima** di chiudere la sessione — la sezione "Stato del progetto" sotto va riallineata all'ultimo modulo davvero completato.
2. Apri una nuova conversazione nella stessa cartella di progetto (`c:\Users\Marco\Desktop\agent`).
3. Primo messaggio: "Leggi HANDOFF.md e TODO.MD e riprendi da lì."
4. Il nuovo assistente ricostruisce il contesto da questo file + `TODO.MD` + lo stato reale dei file — non serve ripetere la storia della conversazione precedente.

## Decisioni già prese — non rimetterle in discussione

- **Metodologia**: allineamento modulo per modulo (A → C → D → E, ordine scelto per dipendenza tecnica — C usa le eccezioni di `requests` introdotte in A). Un modulo alla volta, checkpoint esplicito "Modulo X: completo. Confermi?" prima di avanzare al successivo.
- **Regola di collaborazione cambiata in questa sessione, prevale su ogni abitudine precedente**: **da qui in avanti i commit Git li esegue l'utente manualmente.** L'assistente non esegue più `git commit` di propria iniziativa né su richiesta generica di "procedi" — propone e modifica i file, ma l'azione di commit resta dell'utente, salvo richiesta esplicita e puntuale contraria in quella specifica sessione. Non derivare questa regola dal codice: non è scritta da nessuna parte nel repository, vive solo qui.
- **Fonte di verità per gli obiettivi del corso**: `LLM_Lez_3.pdf` (Dr. Paolo Addis, ITS Alto Adriatico, Deep Learning e LLM, Lezione 3). **Non è un file nel repository** — è stato allegato in chat dall'utente. Se serve ricontrollare uno slide specifico in una nuova sessione, chiedere all'utente di riallegarlo.
- **Stile di collaborazione richiesto** (da `C:\Users\Marco\.claude\CLAUDE.md`, istruzioni permanenti dell'utente): tono tecnico, diretto, gate di verifica (fonte/dati/conflitti/bottleneck/ottimizzazione) prima di proporre soluzioni, spiegazione in tre parti (cosa farò / perché / rischio aperto) prima di agire, nessuna azione autonoma senza conferma.
- **Scope**: nessuna GUI, nessun'interfaccia web, nessuna dipendenza non motivata oltre `requests`/`python-dotenv` (già concordate). Un piano che espande il perimetro (es. aggiunge un'app web) va ridotto prima dell'esecuzione.

## Stato del progetto

| Modulo | Stato |
|---|---|
| A — Stack di dipendenze (`requests`+`python-dotenv`, rename `MODEL`→`LM_MODEL`) | **Completato, confermato.** Verificato end-to-end (server giù + risposta reale). |
| C — Gestione errori HTTP (Timeout/ConnectionError/HTTPError distinti) | **Completato, confermato.** `timeout` passato a tupla `(5, 120)`. Tutti e tre i rami verificati singolarmente contro il server reale: connessione rifiutata, timeout forzato artificialmente, ID modello inesistente (400 con corpo leggibile). |
| D — Disciplina dei commit | **Completato, confermato.** Opzione 2 scelta in via definitiva: `76ceef7` resta com'è, nessuna riscrittura di storia. |
| E — Sincronizzazione documentazione | **Completato, confermato.** `claude.md` corretto (4 punti: obiettivo, stato client.py, checklist di approvazione, rimozione contenuto di task) e riordinato gerarchicamente. `README.md` riscritto: dipendenze reali, `LM_MODEL`, `--chat`, streaming, esecuzione da venv. |
| Estensione 2 — Streaming | **Completata, confermata.** `send_request()` ora stampa i frammenti via `iter_lines()`/SSE invece di restituire il blocco intero. Verificata in entrambe le modalità. Non fa parte del bundle problematico di `76ceef7` (implementata e committata separatamente in questa sessione). |
| Promemoria pulizia finale codice | Tutti i moduli (A/C/D/E) ed Estensione 2 sono chiusi — prossimo passo, vedi fondo di `TODO.MD`. |

Dettaglio di ciascun modulo (sintomo, causa, correzione prevista): **vedi `TODO.MD`**, non duplicato qui.

## Stato della cronologia Git

Il repository ha un remoto: `origin → https://github.com/CyberMark93/client.git`.

**`76ceef7` (storico, risolto per decisione esplicita, non riaprire).** Bundla Estensione 1 (input da terminale) ed Estensione 3 (history in memoria) in una sola diff, saltando l'Estensione 2 (streaming, arrivata dopo e committata a parte). È già pushato su `origin/main`. **Decisione presa: Opzione 2** — nessuna riscrittura, nessun force-push, resta così com'è come debito tecnico accettato (il criterio minimo del docente, slide 29, è comunque soddisfatto nella sostanza). Non riproporre la riscrittura salvo l'utente la riapra esplicitamente.

**Commit di processo di questa sessione (non un problema, scelta deliberata).** 5 commit atomici (Moduli A/C + nuovi file di processo) sono stati squashati su richiesta esplicita dell'utente in `bf068d9` (`git reset --soft HEAD~5` + ricommit — sicuro, nessuno era pushato). Dopo quello sono arrivati `a4a0ca0` (HANDOFF.md), `1baaf66` (streaming), `f317314` (sync docs). **`main` locale è ora 4 commit avanti a `origin/main`** (`bf068d9`, `a4a0ca0`, `1baaf66`, `f317314`), nessuno pushato. Nessuna richiesta di push ricevuta finora.

## File di processo creati in questa collaborazione

- `TODO.MD` — tracciamento moduli, da tenere sincronizzato ad ogni checkpoint.
- `HOW-TO-USE.md` — guida funzionale del client, aggiornata ad ogni cambio di comportamento osservabile.
- `HANDOFF.md` — questo file.

Nessuno dei tre è parte della consegna formativa richiesta dal docente (slide 31 del PDF: `client.py`, `README.md`, `requirements.txt`, `.env.example`, `CLAUDE.md`, commit) — sono supporto di processo per la collaborazione, non materiale da presentare.

## Attenzione per la prossima sessione

- Non richiedere di nuovo conferme già ottenute: Moduli A, C, D, E e l'Estensione 2 (streaming) sono tutti chiusi, non riaprirli senza un motivo esplicito dell'utente.
- **Non eseguire `git commit` di propria iniziativa** — vedi la regola di collaborazione in cima. Proporre le modifiche, lasciare che sia l'utente a committarle, salvo richiesta esplicita contraria in quella sessione.
- Prossimo passo pianificato: pulizia finale del codice (checklist in fondo a `TODO.MD`), poi la consegna è completa.
- Se l'utente chiede "a che punto siamo", la risposta è nelle tabelle sopra, non da ricostruire rileggendo tutta la conversazione precedente.
- Se emerge di nuovo il tema "riscrivere la storia di `76ceef7`", ripresentare il rischio del force-push prima di agire — non è stato accettato in precedenza, solo spiegato.
