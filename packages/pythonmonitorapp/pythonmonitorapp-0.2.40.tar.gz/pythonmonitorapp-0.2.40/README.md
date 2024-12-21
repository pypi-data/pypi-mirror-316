Questa è la **quarta repository**.

Il contenuto di questa repository corrisponde alla versione definitiva della pipeline e del progetto.

Per prendere visione di tutte le precedenti esecuzioni della pipeline (occorse durante la sua costruzione) è possibile consultare:
- la [prima repository](https://gitlab.com/m.ferioli/2024_assignment2_pythonmonitorapp) con la relativa [sezione pipelines](https://gitlab.com/m.ferioli/2024_assignment2_pythonmonitorapp/-/pipelines)
- la [seconda repository](https://gitlab.com/Giu06/2024_assignment2_pythonmonitorapp) con la relativa [sezione pipelines](https://gitlab.com/Giu06/2024_assignment2_pythonmonitorapp/-/pipelines)
- la [terza repository](https://gitlab.com/Pynci/2024_assignment2_pythonmonitorapp_3) con la relativa [sezione pipelines](https://gitlab.com/Pynci/2024_assignment2_pythonmonitorapp_3/-/pipelines)

# Costruzione di una Pipeline CD/CI - il caso “Python monitor app”

**Assignment 2** svolto dal gruppo FPV:
- Marco Ferioli, 879277
- Luca Pinciroli, 885969
- Giulia Raffaella Vitale, 885938

## Report del lavoro svolto

### 1. Progetto selezionato ed operazioni di modifica
Il progetto selezionato è una semplice web application realizzata in Python, che permette di monitorare in real-time il funzionamento della CPU e dei processi in esecuzione sul proprio computer.

Al fine di costruire la pipeline CI / CD sono state effettuate delle modifiche preliminari sul progetto. In particolare sono state aggiornate e aggiunte diverse dipendenze presenti all’interno del file `requirements.txt` e sono stati introdotti i file `setup.py` e `.bumpversion.cfg` per effettuare alcune delle operazioni della pipeline. 


### 2. Definizione degli stages
L’implementazione della pipeline CI/CD per un applicativo Python prevede anzitutto la costituzione di un file di configurazione Yaml, di norma denominato `.gitlab-ci.yml`. Tale file contiene le istruzioni che GitLab deve utilizzare al fine di eseguire automaticamente i task della pipeline. La pipeline è strutturata in sei stages: build, verify, test, package, release, docs. Ciascuno degli stage è specificato all’interno di `stages`:

```yaml
stages:
    - build
    - verify
    - test
    - package
    - release
    - docs
```

### 3. Cache
Al fine di rendere efficiente l’uso delle risorse ed evitare che le operazioni siano ridondanti, è stata predisposta una cache nel quale è stato salvato l’ambiente virtuale usato dalla pipeline.

Nei stage successivi allo stage `build`, il contenuto della cache viene recuperato dall’istruzione globale `before_script` ed utilizzato al fine di velocizzare le operazioni svolte.

```yaml
default:
    cache:
        paths:
            - src/.venv

before_script:
    - if [ "$CI_JOB_STAGE" != "build" ]; then . src/.venv/bin/activate; fi
```


### 4. Build

In quanto linguaggio interpretato, Python non richiede una fase di compilazione; di conseguenza, questo stage si limita alla creazione dell’ambiente virtuale e all'installazione delle dipendenze del progetto.

```yaml
build_app:
    stage: build
    script:
        - apt-get update && apt-get install -y python3-venv
        - python3 -m venv src/.venv 
        - pip install -r src/requirements.txt 
```

All’interno del job vengono eseguiti tre differenti step: il primo si occupa dell'installazione degli strumenti necessari all’esecuzione del progetto, il secondo crea l’ambiente virtuale utilizzato per il task, mentre il terzo effettua l’installazione delle dipendenze necessarie.

### 5. Verify
Verify è lo stage utilizzato per il controllo di stile e sicurezza, al fine di assicurare che il codice segua standard di qualità uniformi.

Nell’esecuzione di tale stage sono state effettuate due tipologie di **analisi statica** (senza esecuzione del codice), ossia l’analisi della qualità del codice e l’analisi della sicurezza.

L’analisi della qualità del codice utilizza **Prospector**, un tool che informa riguardo la presenza di possibili errori, potenziali problemi e violazioni di convenzioni:

```yaml
code_quality: 
    stage: verify
    script:
        - prospector src --output-format json > prospector-report.json
    artifacts:
        paths:
            - prospector-report.json
        when: on_failure
    allow_failure: true
```

L’analisi sulla sicurezza usa invece **Bandit**, un tool progettato per trovare problemi comuni di sicurezza nel codice Python:

```yaml
security_scan:
    stage: verify
    script:
        - bandit -r src --severity-level low -f json -o bandit-report.json
    artifacts:
        paths:
            - bandit-report.json
        when: on_failure
    allow_failure: true
```

In entrambi i casi, viene usato il comando `allow_failure: true`, il quale consente di segnalare errori di stile del codice senza bloccare l’intero processo della pipeline.
Nel caso siano presenti errori, questi verranno salvati in un file json come artefatto, al fine di poterli consultare.

Per quanto riguarda l’**analisi dinamica** del codice, all’interno della pipeline vengono effettuate due operazioni: un controllo sul test-coverage ed uno sulla vulnerabilità delle dipendenze installate.

Per la prima operazione è stato utilizzato il seguente frammento di codice:

```yaml
coverage_dynamic_analysis:
    stage: verify
    script:
        - pytest --cov=src --cov-report=xml:coverage.xml --cov-fail-under=80
    artifacts:
        paths:
            - coverage.xml
```

L’obiettivo è verificare che il codice dei file all’interno della cartella `src` sia ben coperto dai test; viene inoltre stabilita una soglia minima di coverage tramite il tag `cov-fail-under`. 
Viene infine prodotto l’artifact `coverage.xml`, contenente il livello di copertura.

Per mettere in atto la seconda operazione, è stato invece utilizzato il seguente frammento di codice:

```yaml
dependency_check:
    stage: verify
    script:
        - apt-get update && apt-get install -y openjdk-11-jre curl unzip
        - curl -sSL https://github.com/jeremylong/DependencyCheck/releases/download/v8.3.1/dependency-check-8.3.1-release.zip -o dependency-check.zip
        - ls -lh dependency-check.zip
        - unzip dependency-check.zip -d dependency-check
        - ls -lh dependency-check/dependency-check/bin
        - dependency-check/dependency-check/bin/dependency-check.sh --project FlaskApp --scan src --out dependency-check-report.html
    artifacts:
        paths:
            - dependency-check-report.html
        when: always

```
L'obiettivo del codice eseguito è quello di identificare eventuali vulnerabilità all’interno delle dipendenze installate, contribuendo a migliorare la sicurezza del progetto.

Il funzionamento del job si basa sull’utilizzo dei seguenti componenti:
- `openjdk-11-jre`\
Rappresenta il Java Runtime Environment necessario per eseguire il tool OWASP dependency-check.
- `curl` e `unzip`\
Sono pacchetti utili per scaricare e decomprimere la release del tool.

Tramite `curl` ed `unzip` viene scaricato lo strumento di analisi delle dipendenze, che viene successivamente de-compresso dal formato `.zip`.
A questo punto è possibile eseguire `dependency-check`, che successivamente produce un artefatto contenente le vulnerabilità individuate.

### 6. Test
Lo stage `test` consente di avviare automaticamente i test presenti nel progetto, in modo tale da verificare che l’applicazione superi i test prima di effettuare la release, assicurandosi così che ogni componente operi come previsto. 

Per eseguire i test è stato utilizzato il comando `pytest`:

```yaml
unit_tests:
    stage: test
    script:
        - pytest -v src/app/tests/test_api.py
        - pytest -v src/app/tests/test_views.py

performance_tests:
    stage: test
    needs: [unit_tests]
    script:
        - pytest -v src/app/tests/test_performance.py
```

L’esecuzione dei test è stata predisposta per fare in modo che i test di performance vengano eseguiti solo nel caso in cui i test di unità vadano a buon fine.
Per effettuare tale operazione viene utilizzata la parola chiave `needs`; i due job sono quindi eseguiti in sequenza.

### 7. Package
Lo stage package consente la costruzione del pacchetto dell’applicazione, salvato come artefatto, in modo tale da renderlo disponibile negli stage successivi della pipeline.

Prima di procedere alla creazione del pacchetto, occorre aggiornare la versione del progetto, in modo tale da effettuare correttamente la release. A tale scopo è stato utilizzato il tool **bump2Version**, configurato nel file `.bumpversion.cfg`. Il tool è stato utilizzato all’interno del job `bump-version`, che reperisce il tag contenente la versione del progetto, la incrementa usando bump2Version e aggiorna di conseguenza sia il file `setup.py` che il tag stesso. 

```yaml
bump-version:
    stage: package
    before_script:
        - apt-get update && apt-get install -y git 
        - . src/.venv/bin/activate
        - git fetch origin
        - git checkout main
        - git fetch --tags 
        - git describe --tags --abbrev=0 || echo "v0.0.0" 
        - git config user.name "CI Bot" 
        - git config user.email "ci-bot@example.com" 
        - git remote set-url origin https://oauth2:$CI_PUSH_TOKEN@gitlab.com/Pynci/2024_assignment2_pythonmonitorapp_3.git
    script:
        - pip install bump2version
        - bump2version patch --message "Bump version"
        - git push origin $(git rev-parse --abbrev-ref HEAD) --tags
    artifacts:
        paths:
            - setup.py  
```

L’aggiornamento della versione comporta due commit; al fine di evitare che vengano avviate due pipeline a seguito dei commit, sono state definite delle `rules` all’interno di `workflow` che impediscono l’avvio di una nuova pipeline se il commit che la genera non rispetta i criteri indicati.

```yaml
workflow:
  rules:
    - if: '$CI_COMMIT_TAG'
      when: never 
    - if: '$CI_COMMIT_MESSAGE =~ /Bump version/'
      when: never 
    - when: always
```

Per la creazione del package invece si utilizza il file `setup.py` per creare pacchetti Python, `sdist` genera un archivio sorgente (tipicamente `.tar.gz`) contenente i file del progetto, mentre `bdist_wheel` genera un file binario `.whl` (Wheel) che può essere installato più velocemente rispetto all'archivio sorgente.

```yaml
package:
    stage: package
    script:
        - python setup.py sdist bdist_wheel  
    artifacts:
        paths:
            - dist/*.whl
            - dist/*.tar.gz 
```

### 8. Release
Il job release nella pipeline CI/CD è progettato per rilasciare il codice come pacchetto Python su **PyPI** (Python Package Index).

```yaml
release:
    stage: release
    script:
        - pip install twine
        - twine upload dist/* -u "__token__" -p "$PYPI_TOKEN"
    only:
        - main
    dependencies:
        - package
```

Al fine di effettuare tale operazione è stato utilizzato **Twine**.
Lo strumento viene installato e successivamente viene utilizzato per caricare la release su PyPI sfruttando un token.
Le variabili sono state definite in settings -> CI/CD. 

Questo job dipende dal risultato del job package, in quanto quest’ultimo deve andare a buon fine per poter rilasciare il prodotto.
Inoltre viene eseguito solamente se il branch attivo è `main`, in modo tale da evitare rilasci accidentali su branch secondari.

### 9. Docs
Al fine di generare e pubblicare la documentazione durante l’esecuzione della pipeline, il principale strumento utilizzato è stato **Sphinx**.

```yaml
documentation:
    stage: docs
    before_script:
        - apt-get update && apt-get install -y make
        - . src/.venv/bin/activate
    script:
        - rm -rf docs/build
        - sphinx-quickstart docs --quiet --project "Python Monitor App" --author "Gruppo FPV" --release "0.1" --makefile --sep
        - echo "import os" >> docs/source/conf.py
        - echo "import sys" >> docs/source/conf.py
        - echo "sys.path.insert(0, os.path.abspath('../../src/'))" >> docs/source/conf.py
        - echo "extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.autodoc.typehints']" >> docs/source/conf.py
        - sphinx-apidoc -o docs/source src/
        - cd docs
        - make html
        - mkdir -p ../public
        - cp -r build/html/* ../public
    artifacts:
        paths:
            - public

pages:
    stage: docs
    needs: [documentation]
    script:
        - echo "Sito generato in public, pronto per GitLab Pages"
    artifacts:
        paths:
            - public 
```

Il progetto non è stato predisposto dall’autore per la scrittura della documentazione, infatti la dipendenza di Sphinx non era inizialmente presente.

Per ovviare a questo problema il job documentation si occupa di inizializzare il contenuto della directory docs con i file di configurazione di Sphinx.

Lo strumento viene quindi avviato tramite il comando apidoc e viene prodotta la documentazione automaticamente dal codice, la quale viene successivamente pubblicata nella sezione pages di GitLab.

In questo modo è possibile generare e pubblicare automaticamente la documentazione del progetto ad ogni commit, al fine di renderla consultabile a tutti gli sviluppatori che lavorano sul sistema.


### 10. Risultato finale
Ecco come appaiono gli stage con i rispettivi job all’interno dell’ambiente GitLab:

![pipeline](https://iili.io/2NAooYJ.png)

Come è possibile notare, tutti i job predisposti vengono completati con successo, ad eccezione di `security_scan` che produce un warning.