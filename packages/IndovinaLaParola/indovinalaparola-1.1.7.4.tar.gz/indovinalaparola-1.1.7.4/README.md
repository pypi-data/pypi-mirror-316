



# Processo e Sviluppo del Software
Assignment 2 - DevOps - Gruppo Gasa \
Realizzato da: ( Nome, Mtr, e-mail)
- Bishara Giovanni, 869532, g.bishara@campus.unimib.it
- Mocellin Andrea, 869218, a.mocellin1@campus.unimib.it\

In questo file readme descriviamo l'assigment 2 del corso "Processo e Sviluppo del Software"\
Università degli Studi Milano Bicocca \
AA. 2024/2025


## L’Applicazione
Indovina la Parola è un gioco interattivo in cui l'obiettivo è indovinare una parola segreta scegliendo lettere una per volta. \
All'avvio del gioco viene mostrato all'utente un menu di tre scelte, la prima per giocare, la seconda per visualizzare il migliore score,
e la terza per uscire. \
Con l'input "1" si avvia il gioco, mostrando degli underscore che sostituiscono le lettere della parola da indovinare,
ogni volta che l'utente inserisce una lettera corretta, se giusta la parola si aggiorna mostrando la lettera nelle posizioni indovinate,
mentre se sbagliate diminuiscono i tentativi disponibili.\
Il gioco termina quando l'utente indovina la parola o esaurisce i tentativi a disposizione.
[Link alla Repository](https://gitlab.com/gasa9965349/gasa)


## Il Codice
App è stata sviluppata nel linguaggio di programmazione "Python", 
il codice sorgente dell’applicazione è organizzato nei seguenti file:

IndovinaLaParola.py: Il file principale dell’applicazione\
main.py: Il file da avviare che gestisce il menu iniziale a fa la chiamata al gioco.


## La Pipeline
``` 
image: python:latest

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -V
  - pip install virtualenv
  - virtualenv venv
  - source venv/bin/activate  #Attiva l'ambiente virtuale per il resto della pipeline

stages:
  - build
  - verify
  - test
  - package
  - release
  - docs

build:
  stage: build
  script:
    - echo "Fase di build installazione delle dipendenze."
    - pip install prospector bandit
    - pip install pytest
    - pip install setuptools
    - pip install wheel
    - pip install --upgrade build
    - pip install twine
    - pip install mkdocs
    - echo "Dependencies installed."

verify:
  stage: verify
  script:
    - bandit -r ./IndovinaLaParola.py
    - prospector ./IndovinaLaParola.py --no-autodetect 

test:
  stage: test
  script:
    - echo "Fase di test esecuzione dei test automatici."
    - pytest  

package:
  stage: package
  script:
    - python -m build
  artifacts:
    paths:
      - dist/*  

release:
  stage: release
  script:
   - twine upload dist/* -u __token__ -p $PYPI_TOKEN  
  

docs:
  stage: docs
  script:
    - mkdocs build
    - cp -r ./site ../public
  artifacts:
    paths:
      - public 
 
```

## Build
Lo stage di Build è stato configurato nel file .gitlab-ci.yml per installare le dipendenze necessarie al progetto. In particolare, sono stati eseguiti i comandi per installare setuptools, wheel, build e mkdocs utilizzando pip. Non sono stati riscontrati problemi nell'installazione delle dipendenze, ma è stato necessario utilizzare la cache per velocizzare i passaggi successivi, memorizzando le dipendenze di pip e l'ambiente virtuale creato in precedenza con virtualenv.
## Verify 
### Test Unitari
Lo stage dei test unitari è stato implementato per eseguire i test automatici sul codice del progetto. Sono stati scritti test nel file Unit_Test_IndovinaLaParola.py utilizzando il framework pytest. L'esecuzione di pytest verifica che le singole unità del codice funzionino come previsto. Questo stage è essenziale per garantire che il comportamento di base del progetto sia corretto.

### Test di Integrazione
Lo stage di test di integrazione esegue i test per verificare che le diverse parti del sistema interagiscano correttamente tra di loro. I test di integrazione sono stati creati nel file Integration_Test_IndovinaLaParola.py e vengono eseguiti utilizzando pytest. Questo stage dipende dallo stage dei test unitari, assicurandosi che prima di tutto le unità individuali funzionino correttamente prima di testare le interazioni tra di esse.

## Package
Lo stage di Package è stato implementato per creare il pacchetto del progetto. È stato utilizzato il comando python -m build, che genera il pacchetto utilizzando la libreria build insieme a setuptools e wheel. L'output del comando viene salvato come artefatto nella cartella dist/, che contiene i file generati dalla build, e che sono necessari per lo stage successivo (Release).
## Release
Lo stage di Release è stato configurato per caricare il pacchetto su PyPI utilizzando twine. Dopo la creazione del pacchetto nella fase di packaging, il comando twine upload dist/* carica i file generati su PyPI. Per garantire la sicurezza, il token di autenticazione viene gestito tramite variabili d'ambiente e non esposto nella pipeline. In questo modo, il pacchetto viene caricato su PyPI, rendendolo disponibile per l'installazione da parte degli utenti finali.
## Docs
Lo stage di Docs è responsabile per la generazione e la pubblicazione della documentazione del progetto. Viene utilizzato mkdocs per costruire il sito di documentazione. Il comando mkdocs build --clean crea il sito, che viene poi copiato nella cartella public/ tramite il comando cp -r site/* public/. La documentazione viene poi pubblicata su GitLab Pages, rendendo il sito web della documentazione disponibile pubblicamente.