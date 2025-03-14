import csv
import mysql.connector
from mysql.connector import Error

def recupera_dati_completi(query):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_marketing"
        )
        if connection.is_connected():
            cursor = connection.cursor()  # Restituisce risultati come dizionari

            # Eseguiamo la query
            cursor.execute(query)

            # Recupero dei dati
            result = [elem for elem in cursor.fetchall()]

            cursor.close()
            return result
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()
def esegui_query_parametrizzata_many(query, parametri):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_marketing"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.executemany(query, parametri)
            connection.commit()
            cursor.close()
            print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()
def esegui_query_parametrizzata(query, parametri):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_marketing"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query, parametri)
            connection.commit()
            cursor.close()
            print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()
def esegui_query(query):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_marketing"
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Split the query by semicolons and execute each statement
            statements = query.split(';')
            for statement in statements:
                if statement.strip():  # Only execute non-empty statements
                    cursor.execute(statement)
            connection.commit()
            cursor.close()
            print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()
def recupera_dati_completi_parametrizzata(query,parametri):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_marketing"
        )
        if connection.is_connected():
            cursor = connection.cursor()  # Restituisce risultati come dizionari

            # Eseguiamo la query
            cursor.execute(query,parametri)

            # Recupero dei dati
            result = [elem for elem in cursor.fetchall()]

            cursor.close()
            return result
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()
def recupera_dati_lista(query):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_marketing"
        )
        if connection.is_connected():
            cursor = connection.cursor()  # Restituisce risultati come dizionari

            # Eseguiamo la query
            cursor.execute(query)

            # Recupero dei dati
            result = [elem[0] for elem in cursor.fetchall()]

            cursor.close()
            return result
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()