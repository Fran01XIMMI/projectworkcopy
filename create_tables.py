import mysql.connector
from mysql.connector import Error

try:
    # Connessione al database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Inserisci il tuo nome utente
        password="",  # Inserisci la tua password
        database="bank_marketing"  # Inserisci il nome del tuo database
    )

    if conn.is_connected():
        print("Connesso al database.")

    # Creazione di un cursore
    cursor = conn.cursor()

    # Creazione della tabella jobs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id_job INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            average_salary DECIMAL(10,2) NOT NULL
        );
    """)
    print("Tabella 'jobs' creata con successo.")

    # Creazione della tabella deposit
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deposit (
            id_deposit INT AUTO_INCREMENT PRIMARY KEY,
            term_deposit ENUM('0', '1') NOT NULL
        );
    """)
    print("Tabella 'deposit' creata con successo.")

    # Creazione della tabella contact_history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_history (
            id_history INT AUTO_INCREMENT PRIMARY KEY,
            day_of_week INT NOT NULL,
            month CHAR(5) NOT NULL,
            duration INT NOT NULL
        );
    """)
    print("Tabella 'contact_history' creata con successo.")

    # Creazione della tabella campaigns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id_campaign INT AUTO_INCREMENT PRIMARY KEY,
            campaign INT NOT NULL,
            p_days INT NOT NULL,
            previous INT NOT NULL,
            p_outcome ENUM("failure", "unknown", "nonexistent", "success", "other")
        );
    """)
    print("Tabella 'campaigns' creata con successo.")

    # Creazione della tabella wallet
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            id_wallet INT AUTO_INCREMENT PRIMARY KEY,
            credit_default ENUM('0', '1') NOT NULL,
            balance DECIMAL(10, 2) NOT NULL,
            housing_loan ENUM('0', '1') NOT NULL,
            personal_loan ENUM('0', '1') NOT NULL
        );
    """)
    print("Tabella 'wallet' creata con successo.")

    # Creazione della tabella client con ON DELETE CASCADE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client (
            id_client INT AUTO_INCREMENT PRIMARY KEY,
            age INT NOT NULL,
            job_id INT NOT NULL,
            marital ENUM("divorced", "married", "single", "unknown") NOT NULL,
            education ENUM("primary", "secondary", "tertiary", "unknown", "other") NOT NULL,
            contact ENUM("cellular", "telephone", "unknown") NOT NULL,
            wallet_id INT NOT NULL,
            history_id INT NOT NULL,
            campaign_id INT NOT NULL,
            deposit_id INT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs(id_job),
            FOREIGN KEY (wallet_id) REFERENCES wallet(id_wallet) ON DELETE CASCADE,
            FOREIGN KEY (history_id) REFERENCES contact_history(id_history) ON DELETE CASCADE,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id_campaign) ON DELETE CASCADE,
            FOREIGN KEY (deposit_id) REFERENCES deposit(id_deposit) ON DELETE CASCADE
        );
    """)
    print("Tabella 'client' creata con successo.")

    # Commit delle modifiche
    conn.commit()

except Error as e:
    print(f"Errore durante la creazione delle tabelle: {e}")

finally:
    # Chiusura della connessione
    if conn.is_connected():
        cursor.close
