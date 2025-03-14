# --- IMPORT SECTION ---
# Importiamo tutte le librerie necessarie per il nostro lavoro
import joblib
import numpy as np  # Per operazioni matematiche avanzate, come array e manipolazione dei dati
import pandas as pd  # Per la gestione dei dati in formato tabellare (DataFrame)
import matplotlib.pyplot as plt  # Per creare grafici e visualizzazioni
from sklearn.model_selection import train_test_split  # Per dividere il dataset in training e test set
from sklearn.preprocessing import StandardScaler  # Per la normalizzazione dei dati
from sklearn.ensemble import RandomForestClassifier  # Modello di Random Forest
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, roc_auc_score, f1_score  # Per valutare il modello
import seaborn as sns  # Per visualizzazioni più avanzate (come heatmap)
from imblearn.over_sampling import SMOTE  # Per la gestione del bilanciamento delle classi (oversampling)
from imblearn.pipeline import Pipeline  # Per applicare un pipeline di preprocessing
import os  # Per impostare variabili di ambiente, utile per evitare warning

# Impostiamo il numero massimo di core da utilizzare per evitare avvisi sul consumo eccessivo di risorse
os.environ["LOKY_MAX_CPU_COUNT"] = "4"

# --- MAIN CODE ---
# Carichiamo il dataset dal file CSV con separatore ";"
data = pd.read_csv('Bank_Marketing_1.csv', sep=";")

# Visualizziamo la distribuzione delle classi nella colonna target "deposit" (0=No, 1=Sì)
print("Distribuzione delle classi nella colonna target:")
print(data.iloc[:, -1].value_counts())

# Rimuoviamo le colonne che non sono rilevanti per il nostro modello
data = data.drop(data.columns[[8, 9, 11, 13, 14]], axis=1)

# Separiamo le variabili indipendenti (features) e la variabile dipendente (target)
X = data.iloc[:, :-1]  # Tutte le colonne tranne l'ultima
y = data.iloc[:, -1].values  # Solo l'ultima colonna che rappresenta il target (deposit)

# Suddividiamo il dataset in un training set (80%) e un test set (20%) con stratificazione per mantenere la stessa distribuzione di classi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101, stratify=y)

# Applichiamo la codifica one-hot per le variabili categoriche (trasformandole in variabili numeriche binarie)
X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)

# Mostriamo le prime 5 righe del dataset per una rapida ispezione
print(f"\nEcco le prime 5 righe del dataset:\n{data.head()}")

# Normalizziamo le variabili numeriche per far sì che abbiano media 0 e deviazione standard 1
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Eseguiamo il fit sul training set
X_test_scaled = scaler.transform(X_test)  # Applicamo la stessa trasformazione sul test set

# --- SMOTE (oversampling per bilanciare le classi) ---
# SMOTE genera dati sintetici per bilanciare le classi nel training set
smote = SMOTE(sampling_strategy=1.0, random_state=101)  # Vogliamo un rapporto di 1.0 tra la classe minoritaria e la maggioritaria

# Creiamo un training set bilanciato usando SMOTE
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

# Definiamo i pesi delle classi per il modello, aumentando il peso della classe minoritaria (class 1 = 'Sì')
class_weights = {0: 1, 1: 3.5}  # Peso più alto per la classe minoritaria (Sì)

# --- Creazione e Addestramento del Modello Random Forest ---
# Random Forest è un modello di machine learning che utilizza una foresta di alberi decisionali
model = RandomForestClassifier(
    n_estimators=100,        # Numero di alberi da usare nel modello
    max_depth=20,            # Profondità massima di ogni albero
    min_samples_split=5,     # Numero minimo di campioni per fare uno split in un albero
    min_samples_leaf=4,      # Numero minimo di campioni per una foglia
    max_features="sqrt",     # Consideriamo la radice quadrata del numero di feature per ogni albero
    class_weight=class_weights, # Gestiamo il bilanciamento delle classi usando i pesi definiti
    random_state=101         # Per garantire la riproducibilità dei risultati
)

# Addestriamo il modello con il training set bilanciato
model.fit(X_train_resampled, y_train_resampled)

# --- Previsione e Valutazione del Modello ---
# Previsione sul test set
y_pred = model.predict(X_test_scaled)

# Calcoliamo le metriche di valutazione per il modello
accuracy = accuracy_score(y_test, y_pred)  # Percentuale di predizioni corrette
f1 = f1_score(y_test, y_pred)  # F1-score, bilancia precision e recall
auc_score = roc_auc_score(y_test, model.predict_proba(X_test_scaled)[:, 1])  # AUC-ROC per misurare la qualità del modello

# Stampa dei risultati
print(f"\nL'accuratezza del modello è: {accuracy * 100:.2f} %")

# Report di classificazione per valutare precision, recall e f1-score per ogni classe
print(f"\nClassification report:\n{classification_report(y_test, y_pred)}")

# --- Visualizzazione della Confusion Matrix ---
# La confusion matrix ci permette di vedere quante predizioni sono state corrette o errate per ciascuna classe
conf_matrix = confusion_matrix(y_test, y_pred)

# Creiamo una heatmap per visualizzare la confusion matrix
plt.figure(figsize=(6, 6))

# Creazione della heatmap con una palette di colori più vivace
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Non Investono (0)', 'Investono (1)'],
            yticklabels=['Non Investono (0)', 'Investono (1)'], annot_kws={"size": 16}, cbar_kws={'label': 'Frequenza'})

# Titolo migliorato
plt.title('Confusion Matrix (Con SMOTE)', fontsize=18)

# Etichette per gli assi
plt.xlabel('Predetto', fontsize=14)
plt.ylabel('Reale', fontsize=14)

# Aggiungi un padding per evitare sovrapposizione delle etichette
plt.tight_layout()

# Mostra il grafico
plt.show()

# --- Visualizzazione dell'Importanza delle Feature ---
# Gli alberi decisionali della Random Forest ci permettono di capire quali feature sono più importanti per fare le previsioni
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))

# Titolo del grafico
plt.title('Feature Importances', fontsize=18)

# Grafico a barre con l'importanza delle feature
plt.bar(range(X_train_scaled.shape[1]), importances[indices], align='center', color='dodgerblue')

# Etichette per le feature con rotazione
plt.xticks(range(X_train_scaled.shape[1]), X_train.columns[indices], rotation=45, ha='right', fontsize=12)

# Etichette per l'asse y e x
plt.xlabel('Feature', fontsize=14)
plt.ylabel('Importanza', fontsize=14)

# Mostra il grafico
plt.tight_layout()  # Aggiunge spazio per etichette più lunghe
plt.show()

# --- Visualizzazione delle Predizioni Uniche ---
# Verifichiamo quante predizioni corrette ed errate sono state fatte
print("Predizioni corrette ed errate che sono state fatte:", np.unique(y_pred, return_counts=True))

# --- Visualizzazione delle Previsioni Corrette ed Errate ---
# Visualizziamo un grafico che mostra quante predizioni sono corrette e quante errate per ciascuna classe
labels = ['Non Investono (reale-predetto)', 'Investono (reale-predetto)']
correct_predictions = [np.sum((y_test == 0) & (y_pred == 0)), np.sum((y_test == 1) & (y_pred == 1))]
incorrect_predictions = [np.sum((y_test == 0) & (y_pred == 1)), np.sum((y_test == 1) & (y_pred == 0))]

# Creiamo un grafico a barre per le previsioni corrette ed errate
x = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(8, 6))
bar_width = 0.35

ax.bar(x - bar_width / 2, correct_predictions, bar_width, label='Corrette', color=['blue', 'blue'])
ax.bar(x + bar_width / 2, incorrect_predictions, bar_width, label='Errate', color=['lightblue', 'lightblue'])

ax.set_xlabel('Classi')
ax.set_ylabel('Conteggio')
ax.set_title('Previsioni per Classe')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.show()

joblib.dump(model, 'random_forest_model.pkl')  # Salva il modello
joblib.dump(scaler, 'scaler.pkl')  # Salva lo scaler
joblib.dump(X_train.columns, 'columns.pkl')  # Salva le colonne

# # --- Previsione per un Nuovo Cliente ---
# # Creiamo un esempio di un nuovo cliente per vedere come il modello fa una previsione
# df_nuovo_cliente = pd.DataFrame([[
#     # 58, 'management', 'married', 'tertiary', 0, 2143, 1, 0, 'may', 1, 'unknown' # -> è un NO reale
#     # 59, 'admin', 'married', 'secondary', 0, 2343, 1, 0, 'may', 0, 'unknown' # -> è un SI reale
# ]], columns=[
#     "age", "job", "marital", "education", "default", "balance", "housing", "loan", "month", "campaign", "poutcome"
# ])
#
# # Applichiamo la codifica one-hot per questo nuovo esempio
# df_nuovo_cliente = pd.get_dummies(df_nuovo_cliente)
#
# # Allineiamo le colonne con il training set (aggiungiamo colonne mancanti e le ordiniamo)
# df_nuovo_cliente = df_nuovo_cliente.reindex(columns=X_train.columns)
#
# # Scala il nuovo esempio
# nuovo_cliente_scaled = scaler.transform(df_nuovo_cliente)
#
# # Previsione per il nuovo cliente
# previsione = model.predict(nuovo_cliente_scaled)
#
# # Stampa del risultato della previsione
# if previsione[0] == 1:
#     print("Il modello prevede che il cliente risponderà: Sì")
# else:
#     print("Il modello prevede che il cliente risponderà: No")