# ProjectGroup

Bank Marketing è un'applicazione web basata su Flask che permette di eseguire operazioni CRUD (Create, Read, Update, Delete) sugli utenti bancari. Inoltre, l'app integra un modello di Machine Learning per prevedere la probabilità che un utente effettui un deposito


# Funzionalità Applicazione
L'app permette di gestire gli utenti bancari attraverso:
* Creazione di un nuovo utente
* Visualizzazione dei dati degli utenti
* Modifica delle informazioni esistenti
* Eliminazione di un utente
* Machine Learning
* L'utente può inserire i propri dati e ottenere una previsione sulla probabilità di lasciare un deposito, grazie a un modello di Machine Learning addestrato sui dati bancari.

# Librerie Utilizzate

* flask
* os
* matplotlib
* seaborn
* io
* functools
* pandas
* joblib
* mysql.connector
* import base64

# Step preliminari per utilizzare l'applicazione

1) Creare un database denominato "Bank_Marketing"
2) Una volta che il Database esiste, eseguire la funzione "create_tables" all'interno della cartella PROGETTO_FINALE
3) Una volta che le tabelle sono state create utilizzare la funzione "insert_values" per popolare le tabelle con tutti i record disponibili nel CSV.
4) Avviare "app.py" all'interno della cartella "new_web_template" e aprire il link che viene creato in console.
5) Il sito è pronto all'uso e reso disponibile per operazioni CRUD e prediction machine learning.
