# HANDOFF.md

> Scopo: permettere di riprendere questo lavoro in una **nuova conversazione** quando l'utilizzo del contesto della sessione corrente si avvicina al 40% (soglia di sicurezza scelta dall'utente, non dal codice — nessun meccanismo automatico la rileva: è l'utente a notarla dall'indicatore dell'interfaccia).

## Come usarlo

1. Quando l'utilizzo di contesto è vicino al 40%, chiedi "aggiorna HANDOFF.md" **prima** di chiudere la sessione — la sezione "Stato del progetto" sotto va riallineata all'ultimo modulo davvero completato.
2. Apri una nuova conversazione nella stessa cartella di progetto (`c:\Users\Marco\Desktop\agent`).
3. Primo messaggio: "Leggi HANDOFF.md e TODO.MD e riprendi da lì."
4. Il nuovo assistente ricostruisce il contesto da questo file + `TODO.MD` + lo stato reale dei file — non serve ripetere la storia della conversazione precedente.

## Decisioni già prese — non rimetterle in discussione

- **Metodologia**: allineamento modulo per modulo (A → C → D → E, ordine scelto per dipendenza tecnica — C usa le eccezioni di `requests` introdotte in A). Un modulo alla volta, checkpoint esplicito "Modulo X: completo. Confermi?" prima di avanzare al successivo.
- **Fonte di verità per gli obiettivi del corso**: `LLM_Lez_3.pdf` (Dr. Paolo Addis, ITS Alto Adriatico, Deep Learning e LLM, Lezione 3). **Non è un file nel repository** — è stato allegato in chat dall'utente. Se serve ricontrollare uno slide specifico in una nuova sessione, chiedere all'utente di riallegarlo.
- **Stile di collaborazione richiesto** (da `C:\Users\Marco\.claude\CLAUDE.md`, istruzioni permanenti dell'utente): tono tecnico, diretto, gate di verifica (fonte/dati/conflitti/bottleneck/ottimizzazione) prima di proporre soluzioni, spiegazione in tre parti (cosa farò / perché / rischio aperto) prima di agire, nessuna azione autonoma senza conferma.
- **Scope**: nessuna GUI, nessun'interfaccia web, nessuna dipendenza non motivata. Un piano che espande il perimetro (es. aggiunge un'app web) va ridotto prima dell'esecuzione (criterio del `CLAUDE.md` di progetto).

## Stato del progetto (ultimo aggiornamento: vedi cronologia Git per la data reale)

| Modulo | Stato |
|---|---|
| A — Stack di dipendenze (`requests`+`python-dotenv`, rename `MODEL`→`LM_MODEL`) | **Completato, confermato dall'utente.** Verificato end-to-end (server giù + risposta reale). |
| C — Gestione errori HTTP (distinguere Timeout/ConnectionError/HTTPError) | Da fare. |
| D — Disciplina dei commit (un commit per estensione; il commit storico `feat: client LM Studio (singola + chat)` bundla due estensioni) | Da fare. Richiede una decisione dell'utente non ancora presa: riscrivere la cronologia Git (distruttivo) oppure adottare la disciplina solo da ora in poi. |
| E — Sincronizzazione documentazione (`CLAUDE.md`/`README.md` non riflettono ancora `--chat` né lo stack `requests`) | Da fare, per ultimo — deve riflettere lo stato finale dopo A+C+D. |
| Promemoria pulizia finale codice | Dopo C, D, E — vedi fondo di `TODO.MD`. |

Dettaglio di ciascun modulo (sintomo, causa, correzione prevista): **vedi `TODO.MD`**, non duplicato qui.

## File di processo creati in questa collaborazione

- `TODO.MD` — tracciamento moduli, da tenere sincronizzato ad ogni checkpoint.
- `HOW-TO-USE.md` — guida funzionale del client, aggiornata ad ogni cambio di comportamento osservabile.
- `HANDOFF.md` — questo file.

Nessuno dei tre è parte della consegna formativa richiesta dal docente (slide 31 del PDF: `client.py`, `README.md`, `requirements.txt`, `.env.example`, `CLAUDE.md`, commit) — sono supporto di processo per la collaborazione, non materiale da presentare.

## Attenzione per la prossima sessione

- Non richiedere di nuovo conferme già ottenute: il Modulo A è chiuso, non riaprirlo senza un motivo esplicito dell'utente.
- Prima di proporre codice per C/D/E, rileggere la sezione pertinente di `TODO.MD` — contiene già il sintomo esatto e la riga di codice coinvolta.
- Se l'utente chiede "a che punto siamo", la risposta è in questa tabella, non da ricostruire rileggendo tutta la conversazione precedente.
