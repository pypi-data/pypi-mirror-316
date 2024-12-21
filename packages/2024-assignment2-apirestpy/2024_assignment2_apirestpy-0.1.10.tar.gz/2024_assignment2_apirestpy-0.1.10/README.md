# CI/CD PIPELINE - Assignment 2

## Gruppo MVPs
I componenti del gruppo MVPs sono:
- Alessandro Verdi 886134
- Gabriele Maggi 886197

_Il lavoro è stato svolto in pair-programming quindi la commit history è poco rilevante._

## Documentazione App
L'applicazione selezionata consiste in uno script Python progettato per avviare un'API REST semplice che sfrutta metodi GET e POST. Il README dell'applicazione si può trovare: [readme app](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/README_APP.md)


## Immagine Docker
L'immagine docker in cui sarà testata la pipeline.
``` yml
image: python:3.9-slim
```
## Defaults
Per l'ottimizzazione di default viene attivato l'enviromment virtuale e viene inserita in cache la cartella contenente l'enviromment con i pacchetti installati.
```yml
default:
  before_script:
    - source $VENV_PATH/bin/activate
  cache:
    key: pip-cache
    paths:
      - $VENV_DIR/
```
## Stages
Le fasi principali della pipeline sono: 
``` yml
stages:  
  - build # crezione dell'ambiente
  - verify # analisi statica e dinamica
  - test # test di unità e di performance
  - versioning # in caso di release incrementa la versione precedente 
  - package # compila il pacchetto .tar.gz per pypi
  - release_step # rilascia su pypi la nuova versione
  - docs # generazione della documentazione
```
### Build
Consiste nella creazione dell'ambiente virtuale python e dell'installazione delle dipendenze richieste dall'applicazione e dai tool della pipeline.

#### Crezione dell'ambiente:
``` yml
 before_script:
   # Creazione ambiente virutale
   - python -m venv $VENV_PATH
   - source $VENV_PATH/bin/activate
```
#### Installazione dipendenze APP/Pipeline
``` yml
  script:
    - pip install --upgrade pip
    # installazione dipendenze app
    - pip install -r requirements.txt
    # installazione dipendenze pipeline
    - pip install mkdocs prospector bandit pytest setuptools wheel twine locust memory-profiler
```
> In caso del bumpversion non viene installato qui per non rallentare ulteriormente la pipeline essendo che viene utilizzato solo nel branch master

##### Artifacts
Viene ritornato come artifacts l'ambiente virutale per mantenere i pacchetti installati attraverso i vari stages.
``` yml
  artifacts:
    paths:
      - $VENV_PATH # ambiente virtuale salvato come artifact
    expire_in: 1 day
```

### Verify 
È la fase di analisi statica e dinamica del codice. Le due analisi vengono eseguite in parallelo perchè non hanno dipendenze in comune.

#### Analisi statica
L'analisi statica viene effettuata utilizzando strumenti Python specifici: 
- Prospector, per valutare la qualità del codice
- Bandit, per analizzarne la sicurezza
``` yml
 script:
    - prospector app.py
 # ...
 script:
    - bandit -r app.py
```


#### Analisi dinamica
L'analisi dinamica avviene tramite gli strumenti Locust e Mprof per la verifica runtime dell'applicazione sotto un carico di utenti. Vengono successivamente eseguiti 2 script per verificare che il tempo di risposta medio e il picco di memoria utilizzata non superino una certa soglia, in caso contrario il job fallisce. Questo è pensato per poterlo poi estendere con altri tipi di test come un'analisi dell'andamento della memoria, al fine di verificare se ci sono variabili non de-allocate all'interno del programma che occupano costantemente memoria.

Locust è un tool interessante perchè permette di analizzare dinamicamente l'applicazione con un numero arbitrario di utenti, potenzialmente anche molto elevato nell'ordine dei milioni. Il numero di utenti è settato tramite: 
```--user <numero_di_utenti>``` 
 e nell'esempio è pari a 5 utenti.

 Mprof invece è utilizzato come memory profiler durante l'esecuzione di Locust. 
```yml
  script:
    - nohup mprof run -o memory_logs.dat app.py &
    - locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users 5 --spawn-rate 5 --run-time 30s --csv=locust_report --html=locust_report.html
    - python ./scripts/locusta_check.py #tempo di risposta
    - python ./scripts/memory_check.py #memory peak
```
Infine i risultati di Locust e mprof sono analizzati tramtie due script python che controllano se non superano soglie predeterminate. In questo caso si è inserita una soglia arbitraria di risposta media di 5ms e un massimo di uso di memoria di 35 MiB.

##### Artifacts
Questa fase ritorna gli artifact sotto forma di file CSV, una rappresentazione grafica come pagina HTML e un file .dat relativo all'utilizzo della memoria.

```yml
  artifacts:
    paths:
      - locust_report_stats.csv
      - locust_report_failures.csv
      - locust_report_stats_history.csv
      - locust_report.html
      - memory_logs.dat
    expire_in: 1 day
```

### Test 
In questa fase vengono svolti dei test di unità e performance tramite lo strumento pytest. I test di performance differiscono dalla fase di analisi dinamica del codice perchè in questo caso si testa una singola risposta e non sotto un carico di utenti. I test di unità e performance possono essere eseguiti in parallelo in quanto non c'è alcuna dipendenza tra i due tipi di test.  

#### Test di unità
Vengono eseguiti i test del file [test_app.py](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/test_app.py) e viene ritornato il risultato come XML nel formato standard JUNIT. I test di unità sono relativi al corretto funzionamento dell'applicazione e richiamano le API controllando che la risposta sia quella attesa.
``` yml
  script:
    - pytest test_app.py --junit-xml=unit_test_report.xml
    - echo "Unit tests passed"
```

##### Artifacts
Il risultato è salvato come artifact e ritornato anche come reports in modo da essere caricato sulla pagina di test di GitLab.
```yml
  artifacts:
    paths:
      - ./unit_test_report.xml
    reports:
       junit: ./unit_test_report.xml
```

##### Rules
Per i test di unità è stata pensata una rule che esegue il job solo nel caso in cui il file [app.py](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/app.py) venga modificato. In modo da ottimizzare i tempi di esecuzione della pipeline ed evitare test in caso non ci siano cambiamenti (assumendo che siano passati nelle commit precedenti).
```yml
   rules: # solo in caso venga modificato il file app.py vengono effettuati
    - changes:
      - app.py
```

#### Test di performance
Vengono eseguiti i test del file [test_performance.py](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/test_performance.py) e ritornato il risultato come XML nel formato standard JUNIT.
``` yml
  script:
    - pytest test_performance.py --junit-xml=unit_test_report.xml
    - echo "Performance tests passed"
```

##### Artifacts
Il risultato è salvato come artifact e ritornato anche come report in modo da essere caricato sulla pagina di test di GitLab.
```yml
  artifacts:
    paths:
      - ./perf_test_report.xml
    reports:
       junit: ./perf_test_report.xml 
```

##### Rules
I test di performance vengono eseguiti sempre, poiché potrebbero esistere dipendenze con altri file che potrebbero influire sulle prestazioni. Ad esempio: cambi di risorse, json in risposta più grande, ecc.

### Versioning
In questa fase si aggiorna il file [setup.py](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/setup.py), modificando il numero di versione in automatico quando si esegue una modifica sul master triggerando una nuova release.
L'aggiornamento del master comporta un cambio di versione e la creazione automatica di un tag di release che porterà a una nuova release.
In questo caso si è deciso solo di incrementare il numero di versione senza gestirla nella maniera più corretta con major|minor|patch. 

``` yml
before_script:
    - apt-get update && apt-get install -y git 
    - git config --global user.email "ci@release.bot"
    - git config --global user.name "CI_Bot"
    - git fetch --prune --tags
    - git tag -l | xargs git tag -d # elimino in caso siano rimasti vecchi tag
    - git fetch --prune --tags
  script:
    - pip install bumpversion
    # ...
    - bumpversion --tag --commit patch
  after_script:
    - git push https://oauth2:${REPO_ACCESS}@gitlab.com/mvps2775149/2024_assignment2_apirestpy.git --tags
    - git push https://oauth2:${REPO_ACCESS}@gitlab.com/mvps2775149/2024_assignment2_apirestpy.git HEAD:master -o ci.skip

```
La modifica della versione, va a modificare il file [setup.py](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/setup.py) che però deve essere aggiornato anche nella repository remota per cui si va a svolgere una push (su ```HEAD:master```) in modo da aggiornare il file e saltando l'esecuzione della pipeline per non entrare in loop (```-o ci.skip```).
Inoltre questo aggiornamento va a far partire la release ufficiale andndo a pushare anche il tag creato corrispondente alla release che in un job successivo andrà a svolgere le operazioni di pubblicazione.

In questo modo si possono sfruttare diverse branch di sviluppo in cui si può sviluppare/modificare l'applicazione e si mantiene la master come default quando si applicano le nuove modifiche testate separatamente, nel momento in cui si decidono di applicare a un release si fa una merge con il master e questo andrà a creare un nuovo release in automatico.

##### Rules
Il job viene eseguito solo se ci si trova sulla branch master.
``` yml
  only:
    - master
```
##### Artifacts
``` yml
artifacts:
  paths:
    - setup.py
  expire_in: 1 hour
```

### Packages
In questa fase si andrà a creare il package python.
``` yml
script:
   - python setup.py sdist bdist_wheel
```

##### Artifacts
Ritornando come artifacts la posizione del package.
Gli artifacts vengono salvati  solamente se il packaging avviene con successo e durano finchè non vengono sovrascritti.
``` yml
  artifacts:
    when: on_success
    paths:
      - ./dist/ # Posizione dei packages whl e .tar.gz
```

### Release
La fase di release svolge il release sul repository PyPi e sul registro di GitLab.

#### PyPi
La release avviene tramite il tool TWINE.
``` yml
  script:
    - TWINE_PASSWORD=${PYPI_TOKEN} TWINE_USERNAME=__token__ python -m twine upload dist/*
```
#### GitLab
Su gitlab è richiesta l'immagine docker contenente gli strumenti per svolgere la release.

``` yml
image: registry.gitlab.com/gitlab-org/release-cli:latest
# ...
release:       
    tag_name: '$CI_COMMIT_TAG'               
    description: 'Release: $CI_COMMIT_TAG - v0.$CI_PIPELINE_IID'
    ref: '$CI_COMMIT_SHA'                         
    assets:
      links:
        - name: 'PyPi Release'
          url: 'https://pypi.org/project/2024-assignment2-apirestpy/$CI_COMMIT_TAG/'

```

##### Rules
La release del package avviene solamente su un tag grazie alla rule:
``` yml
  rules: 
    - if: $CI_COMMIT_TAG
```
> questo tag è inserito nella fase di bumpversion in automatico.


### Docs 
Viene generata la documentazione su GitLab Pages della branch master. 
``` yml
  script:
  - mkdocs build --verbose
  - mv site public
```
Compilando i file nella cartella './docs':
- [./docs/api-reference.md](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/docs/api-reference.md)
- [./docs/getting-started.md](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/docs/getting-started.md)
- [./docs/index.md](https://gitlab.com/mvps2775149/2024_assignment2_apirestpy/-/blob/master/docs/index.md)

##### Artifacts
Fornendo in output la path dove trovare le pagine web solo in caso di successo dello stage. 
``` yml
  artifacts:
    paths:
    - public
    when: on_success
```

### TO DO
1. Aggiungere deploy
2. inserimento di una migliore gestione delle versioni di release
