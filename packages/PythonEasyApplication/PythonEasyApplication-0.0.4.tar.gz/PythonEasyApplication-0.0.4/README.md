# Introduzione


## Componenti del gruppo

- Jacopo        Levati      885971
- Filippo       Besana      879205
- Matteo Carlo  Comi        886035


## Contesto

Progettazione e implementazione della pipeline per PythonEasyProject, un'applicazione Python basata su un'architettura semplice 
composta da Back-End e Front-End. Il Back-End, sviluppato in Python, è responsabile della gestione di una stringa che viene 
successivamente trasmessa al Front-End per essere visualizzata all'interno di una pagina HTML.

L'obiettivo principale di questo lavoro è la pipeline, concentrandosi sulla descrizione e sull'organizzazione degli stage che la
costituiscono.

Per ulteriori dettagli, il repository del progetto è disponibile qui: [link](https://gitlab.com/lemon9693650/pythoneasyproject.git).


# Applicazione: PythonEasyProject

L'applicazione invia una stringa a una pagina `HTML` e, quando gli utenti accedono all'applicazione web, la visualizza 
e la stampa a video. Una volta eseguita l'applicazione `app.py`, possiamo visualizzare la pagina web presso l'indirizzo 
`http://127.0.0.1:5000/`.


# Stages della pipeline:

- [**Build**](#build)

-  [**Verify**](#verify)  

-  [**Unit-Test**](#unit-test)

-  [**Integration-Test**](#integration-test)

-  [**Package**](#package)

-  [**Release**](#release)

-  [**Docs**](#docs)


## Configurazione della cache

La cache viene utilizzata per archiviare temporaneamente file intermedi o risultati, permettendone il riutilizzo in seguito senza doverli ricreare o ricalcolare.

Nelle pipeline CI/CD (Continuous Integration/Continuous Deployment), la cache svolge un ruolo importante, consentendo di salvare 
dipendenze, risultati dei test o altri file temporanei. Questo approccio ottimizza l'efficienza complessiva riducendo i tempi di 
esecuzione e il consumo di risorse.

Ad esempio, la `directory venv/`, che rappresenta l'ambiente virtuale Python, contiene le dipendenze del progetto e può essere condivisa 
tra i diversi stage della pipeline. Questo garantisce un'installazione coerente delle dipendenze e accelera i processi successivi.


## Build

In questa prima fase viene creato un ambiente virtuale Python, chiamato `venv`, utilizzando il comando `python -m venv venv`. Tale ambiente è una directory dedicata, pensata per gestire in modo autonomo le dipendenze del progetto.

Dopo l’inizializzazione, l’ambiente virtuale viene attivato con il comando `source venv/bin/activate`, assicurando così che le operazioni successive avvengano all’interno di questo contesto isolato.

A questo punto si procede all’installazione delle dipendenze contenute nel file `requirements.txt`. Attraverso il comando `pip install -r requirements.txt` vengono lette ed installate tutte le librerie necessarie, incluse le versioni specificate, all’interno dell’ambiente virtuale.

## Verify

Per implementare questo stage sono stati utilizzati i multi-jobs, che consentono di eseguire contemporaneamente due moduli. 
Grazie a questo approccio è possibile gestire le operazioni in modo più ordinato ed efficiente, riducendo i tempi totali, soprattutto nel caso di attività più complesse o impegnative.

In particolare, questo stage si focalizza sulla verifica del codice sorgente, assicurando la qualità e l'affidabilità del progetto.

### Prospector

Uno dei moduli utilizzati è Prospector, uno strumento di analisi statica per il codice Python. Questo tool è in grado di individuare
diversi tipi di problemi, tra cui violazioni di stile, errori sintattici, eccessiva complessità del codice e utilizzo di variabili non 
dichiarate. Dopo aver completato l’installazione, si procede all’esecuzione del comando prospector per avviare il processo di verifica.

### Bandit

Il secondo comando, `pip install bandit`, permette di integrare Bandit, un tool focalizzato sulla sicurezza del codice Python. Bandit è 
in grado di identificare potenziali vulnerabilità, come falle di sicurezza o un uso scorretto delle funzioni di crittografia. Una volta 
completata l’installazione, l’esecuzione del comando `bandit -r PythonEasyProject/app.py` consente di analizzare in modo ricorsivo il 
codice sorgente presente nel file `app.py`. L’opzione `-r`, infatti, abilita la scansione completa dell’intero file, evidenziando eventuali problemi di sicurezza.


## Unit-Test

Questa parte della pipeline è dedicata all’esecuzione dei test unitari. I test unitari vengono utilizzati per verificare il corretto funzionamento di singole parti del codice, come funzioni o classi, in maniera isolata, assicurando così che ogni componente funzioni come previsto indipendentemente dal resto dell’applicazione.

L’esecuzione dei test avviene tramite il comando `pytest PythonEasyProject/tests/unit_test.py`. Questo fa sì che il framework di 
testing `pytest` analizzi il file `unit_test.py` all’interno della directory `PythonEasyProject/tests`, riconoscendo automaticamente i 
test presenti al suo interno ed eseguendoli. Al termine, pytest fornisce un resoconto dettagliato dei risultati, facilitando la 
comprensione di eventuali problemi riscontrati.


## Integration-Test

Questa fase della pipeline CI/CD è dedicata all’esecuzione dei test di integrazione, il cui scopo è verificare il corretto 
funzionamento dell’intera applicazione, incluse le interazioni tra i vari componenti.

Il comando avviato esegue i test di integrazione definiti nel file `integration_test.py`, situato nella directory 
`PythonEasyProject/tests`. Ancora una volta si utilizza il framework pytest, che offre un ambiente consolidato per eseguire i test e 
fornire report chiari e dettagliati sull’esito delle verifiche.


## Package

Lo stage package si concentra sulla preparazione del progetto affinché possa essere confezionato e distribuito all’interno della
pipeline CI/CD. In questa fase, l’applicazione viene convertita in un formato facilmente distribuibile e installabile.

`Setuptools`: modulo Python che fornisce strumenti per definire, impacchettare e distribuire pacchetti. È comunemente utilizzato 
per creare pacchetti Python che possono essere facilmente installati tramite pip, il gestore dei pacchetti. 
Questo li rende accessibili e utilizzabili da altri sviluppatori.

`Wheel`: è un formato di distribuzione binaria dei pacchetti Python. Si tratta di un formato specifico per la distribuzione di 
librerie precompilate e può semplificare notevolmente il processo di installazione di pacchetti Python su un sistema.

Il comando python `setup.py sdist bdist_wheel`, invece, utilizza il file `setup.py` per creare i pacchetti di distribuzione. 
Genera un pacchetto di distribuzione sorgente (`SDIST`) e un pacchetto di distribuzione binario (`BDIST_WHEEL`). 
Entrambi questi pacchetti sono pronti per essere confezionati e distribuiti attraverso il sistema di gestione delle librerie Python, 
come `pip`.

Infine, la sezione artifacts ha il compito di conservare il contenuto della `directory dist`, che contiene i pacchetti appena creati. 
Questi risultati finali saranno così disponibili per utilizzi futuri o per la pubblicazione.


## Release

In questa fase della pipeline si procede alla pubblicazione del pacchetto Python su PyPI,  
utilizzando `twine`, uno strumento che semplifica e rende sicuro l’upload dei pacchetti.  
Dopo aver attivato  l’ambiente virtuale con `source venv/bin/activate`, si esegue il comando: 
`twine upload –username $PYPI_USERNAME –password $PYPI_PASSWORD dist/*`
Tramite questo comando, i pacchetti generati, presenti nella directory `dist/`, vengono caricati su PyPI.
L’autenticazione dell’utente è gestita in modo sicuro, utilizzando le variabili d’ambiente `$PYPI_USERNAME` e `$PYPI_PASSWORD`, fornite 
come variabili protette nel sistema di CI/CD. In questo modo si assicura che le credenziali non siano esposte nel codice o nei log.


## Docs

Questo job si occupa di produrre e pubblicare la documentazione del progetto. A differenza degli stage precedenti, il nome di questo 
job è pages anziché docs. Questo perché GitLab, se individua un job denominato pages, crea e avvia automaticamente un job aggiuntivo 
chiamato deploy:release nel quale viene effettuato l'upload della cartella public su GitLab Pages.

Per generare la documentazione, si utilizza il comando `pdoc src/ -o public`, sfruttando lo strumento pdoc per analizzare i file 
presenti nella directory `src/` del progetto PythonEasyProject e produrre la relativa documentazione, che viene poi salvata nella 
directory public. Come già detto in precedenza, la sezione artifacts serve per conservare la cartella public appena generata, 
rendendola disponibile per le fasi successive.

