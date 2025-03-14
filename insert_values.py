from tqdm import tqdm
import csv

from funzioni_utili import esegui_query_parametrizzata_many, recupera_dati_completi_parametrizzata
from funzioni_utili import esegui_query

# Insert jobs
with open('average_salary.csv', encoding='utf-8') as f:
    lettore = csv.reader(f, delimiter=',')
    f.readline()
    lista_inserimento = []
    lista_lavori = []
    for riga in lettore:
        lavoro = riga[0]
        if lavoro not in lista_lavori:
            lista_lavori.append(lavoro)
            query = f"""INSERT INTO jobs(nome, average_salary) VALUES (%s, %s)"""
            valore = (riga[0], riga[1])
            lista_inserimento.append(valore)

    esegui_query_parametrizzata_many(query,lista_inserimento)

esegui_query("SET GLOBAL max_allowed_packet = 1073741824;")

# Insert client, deposit, campaigns, contact_history, wallet
with open('Bank_Marketing_1.csv', encoding='utf-8') as f:
    lettore = csv.reader(f, delimiter=';')
    f.readline()
    query = f"""INSERT INTO client(id_client, age, job_id, marital, education, contact, wallet_id, history_id, campaign_id, deposit_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    listaClienti = []
    listaWallet = []
    listaCampaign = []
    listaDeposit = []
    listaHistory = []
    diz_lavori = {}
    id = 1

    for riga in tqdm(lettore):
        job = riga[1]
        wallet = (riga[4], riga[5], riga[6], riga[7])
        campaign = (riga[12], riga[13], riga[14], riga[15])
        deposit = (riga[16],)
        history = (riga[9], riga[10], riga[11])
        id = str(id)
        listaWallet.append((id,) + wallet)
        listaDeposit.append((id,) + deposit)
        listaCampaign.append((id,) + campaign)
        listaHistory.append((id,) + history)
        id = int(id)
        if job in diz_lavori:
            job_id = diz_lavori[job]
        else:
            job_id = recupera_dati_completi_parametrizzata(f"""SELECT id_job FROM jobs
                    WHERE nome = %s""", (job,))[0][0]
            diz_lavori[job] = job_id

        valori = (id, riga[0], job_id, riga[2], riga[3], riga[8], id, id, id, id)
        listaClienti.append(valori)
        id += 1

    queryWallet = f"""INSERT INTO wallet(id_wallet , credit_default, balance, housing_loan, personal_loan) VALUES (%s, %s, %s, %s, %s)"""
    esegui_query_parametrizzata_many(queryWallet, listaWallet)
    queryDeposit = f"""INSERT INTO deposit(id_deposit, term_deposit) VALUES (%s, %s)"""
    esegui_query_parametrizzata_many(queryDeposit, listaDeposit)
    queryCampaign = f"""INSERT INTO campaigns(id_campaign, campaign, p_days, previous, p_outcome) VALUES (%s, %s, %s, %s, %s)"""
    esegui_query_parametrizzata_many(queryCampaign, listaCampaign)
    queryHistory = f"""INSERT INTO contact_history(id_history, day_of_week, month, duration) VALUES (%s, %s, %s, %s)"""
    esegui_query_parametrizzata_many(queryHistory, listaHistory)
    esegui_query_parametrizzata_many(query, listaClienti)
