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
| D — Disciplina dei commit | **Parziale, decisione ancora aperta** — vedi "Stato della cronologia Git" sotto. Non confondere con il punto precedente (regola di collaborazione): quella è chiusa, questa no. |
| E — Sincronizzazione documentazione | **Parziale.** `claude.md` corretto (4 punti: obiettivo, stato client.py, checklist di approvazione, rimozione contenuto di task) e riordinato gerarchicamente. **`README.md` non ancora toccato** — non documenta `--chat` né lo stack `requests`/`python-dotenv`. Unico punto rimasto. |
| Estensione 2 — Streaming | **Mai implementata.** Confermato leggendo il codice: `build_payload()` ha `"stream": False` fisso, nessuna gestione di eventi SSE. Non bloccante per il criterio minimo del docente (slide 29), ma assente. |
| Promemoria pulizia finale codice | Dopo D (decisione) ed E (README.md) — vedi fondo di `TODO.MD`. |

Dettaglio di ciascun modulo (sintomo, causa, correzione prevista): **vedi `TODO.MD`**, non duplicato qui.

## Stato della cronologia Git — leggere con attenzione, due situazioni distinte da non confondere

Il repository ha un remoto: `origin → https://github.com/CyberMark93/client.git`.

**Situazione 1 — `76ceef7` (problema originale del Modulo D, irrisolto).** Questo commit storico bundla Estensione 1 (input da terminale) ed Estensione 3 (history in memoria) in una sola diff, saltando l'Estensione 2 (streaming). **È già pushato su `origin/main`.** Due opzioni discusse e non ancora scelte:
- *Opzione 1*: riscrivere la cronologia (rebase interattivo per separare le due estensioni — non banale, il codice della terza riusa strutturalmente quello della prima) e poi **force-push su `origin/main`**. Rischioso: se qualcun altro ha già fetchato questo repo, la sua copia diverge. Da non eseguire senza una conferma esplicita e separata, specifica per il force-push.
- *Opzione 2*: non toccare `76ceef7`, accettarlo come debito tecnico documentato. Il criterio minimo del docente (slide 29, "Estensione 1 completata, verificata e salvata con un commit") è comunque soddisfatto nella sostanza anche da questo commit bundlato.
- **Nessuna delle due è stata scelta.** Non presumere l'Opzione 2 solo perché è quella "di default" — l'utente non ha ancora risposto a questa domanda specifica.

**Situazione 2 — `bf068d9` (commit di processo di questa sessione, RISOLTA, non un problema).** I 5 commit fatti durante questa sessione per i Moduli A/C/E (migrazione dipendenze, fix gestione errori, correzioni `claude.md`, nuovi file `TODO.MD`/`HOW-TO-USE.md`/`HANDOFF.md`) erano stati fatti atomici, poi **squashati deliberatamente in un unico commit** `bf068d9` su richiesta esplicita dell'utente, con un `git reset --soft HEAD~5` + ricommit (sicuro: nessuno dei 5 era stato pushato). **Non è un errore da correggere** — è una scelta consapevole dell'utente, distinta dal problema di `76ceef7`. `bf068d9` non è ancora pushato (`main` è 1 commit avanti a `origin/main`).

## File di processo creati in questa collaborazione

- `TODO.MD` — tracciamento moduli, da tenere sincronizzato ad ogni checkpoint.
- `HOW-TO-USE.md` — guida funzionale del client, aggiornata ad ogni cambio di comportamento osservabile.
- `HANDOFF.md` — questo file.

Nessuno dei tre è parte della consegna formativa richiesta dal docente (slide 31 del PDF: `client.py`, `README.md`, `requirements.txt`, `.env.example`, `CLAUDE.md`, commit) — sono supporto di processo per la collaborazione, non materiale da presentare.

## Attenzione per la prossima sessione

- Non richiedere di nuovo conferme già ottenute: Moduli A e C sono chiusi, non riaprirli senza un motivo esplicito dell'utente.
- **Non eseguire `git commit` di propria iniziativa** — vedi la regola di collaborazione in cima. Proporre le modifiche, lasciare che sia l'utente a committarle, salvo richiesta esplicita contraria in quella sessione.
- Prima di proporre codice per D (decisione) o E (`README.md`), rileggere la sezione pertinente di `TODO.MD`.
- Se l'utente chiede "a che punto siamo", la risposta è nelle tabelle sopra, non da ricostruire rileggendo tutta la conversazione precedente.
- Se emerge di nuovo il tema "riscrivere la storia di `76ceef7`", ripresentare il rischio del force-push prima di agire — non è stato accettato in precedenza, solo spiegato.
