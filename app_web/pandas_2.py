import pandas as pd

# Carica il dataset
df = pd.read_csv('Bank_Marketing.csv', delimiter=';')

# Esempio di pulizia dei dati
df['deposit'] = df['deposit'].map({'yes': 1, 'no': 0})