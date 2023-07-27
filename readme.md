# Istruzioni per l'uso dello script Comparatore di Modelli

Questo script è progettato per confrontare e valutare la qualità di due modelli di intelligenza artificiale, GPT-3.5 Turbo e Vertex AI. Lo script può essere adattato con semplicità ad altri modelli attraverso API. Genera una serie di prompt, poi chiama entrambi i modelli per generare risposte a questi prompt. Infine, valuta le risposte e determina quale modello ha fornito la risposta migliore.

## Video Youtube

Video Youtube con una mia conclusione e istruzioni per usare il file:

[Google Bard è meglio di ChatGPT? Modelli a confronto! (PARTE 1)](https://youtu.be/ix1HHrTvczo)

## Prerequisiti

Per utilizzare questo script, è necessario avere installato Python sul proprio computer. Inoltre, è necessario avere accesso a entrambi i modelli di intelligenza artificiale, GPT-3.5 Turbo e Vertex AI.

## Installazione

1. Clona il repository GitHub sul tuo computer locale utilizzando il comando `git clone`.
2. Naviga nella directory del progetto utilizzando il comando `cd`.
3. Installa le dipendenze richieste utilizzando il comando `pip install -r requirements.txt`.

## Configurazione

Per far funzionare Vertex AI, è necessario fare login con gcloud da CLI con il comando `gcloud auth application-default login`. Prima di eseguire questo comando, è necessario attivare le API da Google Cloud Console. Puoi installare gcloud da [qui](https://cloud.google.com/sdk/docs/install).

### Impostazione della chiave API di OpenAI

Per utilizzare il modello GPT-3.5 Turbo, è necessario impostare la variabile di ambiente `OPENAI_API_KEY` con la tua chiave API di OpenAI. Ci sono due modi per farlo:

1. **Impostazione della variabile di ambiente:** Puoi impostare la variabile di ambiente `OPENAI_API_KEY` nel tuo sistema operativo. Il metodo per farlo varia a seconda del sistema operativo che stai utilizzando. Ad esempio, su un sistema Unix-like, puoi utilizzare il comando `export OPENAI_API_KEY='your-key'` nel tuo shell prima di eseguire lo script.

2. **Impostazione della chiave API nello script:** Alternativamente, puoi impostare la chiave API direttamente nello script Python. Per farlo, aggiungi la seguente riga di codice all'inizio dello script, sostituendo `'your-key'` con la tua chiave API:

```python
import os
os.environ['OPENAI_API_KEY'] = 'your-key'
```

## Esecuzione dello script

Iniziare modificando lo script con il proprio `GCLOUD_PROJECT_ID` all'interno del file.

Per eseguire lo script, utilizza il comando `python generazione_sintetica.py` nella directory del progetto.

## Risultati

Lo script creerà un file di output chiamato `output.txt` che conterrà i risultati del test. Questo file includerà i prompt utilizzati, le risposte generate da ciascun modello, il modello vincente per ciascun prompt e il motivo della vittoria.

## Input manuali

È anche possibile valutare varie AI con prompt specifici tramite `input_manuali.py`. Lanciato questo file, chiederà di inserire un prompt sul quale valuterà i due modelli.

## Supporto

Se incontri problemi durante l'uso di questo script, apri un problema nel repository GitHub e faremo del nostro meglio per aiutarti.