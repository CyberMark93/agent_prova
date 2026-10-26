- Obiettivo: client Python per un modello locale esposto da LM Studio; nessuna interfaccia grafica, nessun framework. Due modalità: chiamata singola (comportamento base) e --chat (cronologia della conversazione in memoria del processo, persa alla chiusura).

- comportamento richiesto:(
1 Leggere indirizzo del server e identificativo del modello dalla configurazione.
2 Preparare un'istruzione in italiano e una domanda tecnica fissa.
3 Inviare la richiesta a LM Studio e stampare il testo della risposta.
4 Mostrare un messaggio comprensibile se il server non è raggiungibile.)

- client.py implementa la chiamata singola e la modalità --chat; non è più uno scheletro.
- README.md descrive la preparazione dell'ambiente.
- requirements.txt contiene le dipendenze concordate.

- Avvio dalla radice: .\.venv\Scripts\python.exe client.py (aggiungere --chat per la modalità conversazionale).
- Verifica manuale: domanda fissa, confronto delle risposte, server fermo e ripristinato.

- Usare PowerShell nei comandi per Windows.
- Preferire Python sincrono e modifiche circoscritte.
- Non inserire segreti, pesi o ambiente virtuale in Git.
- Non sono presenti test automatici in questo checkpoint.

- fammi le domande necessarie alla costruzione del progetto rispetto a ciò che non sai e lavoreremo step by step e io convalido ad ogni step.

- Checklist di approvazione per ogni piano proposto (da applicare ad ogni modifica, non un fatto fissato una volta per tutte):
  - File coinvolti motivati rispetto all'obiettivo del modulo in corso.
  - Dipendenze già concordate: requests, python-dotenv. Un'aggiunta oltre queste richiede motivazione esplicita e conferma — non è vietata a priori, va discussa caso per caso.
  - Prove eseguibili e verificate prima di dichiarare il modulo completo.
  - Un piano che espande il perimetro oltre l'obiettivo dichiarato (es. GUI, applicazione web) va ridotto prima dell'esecuzione.
