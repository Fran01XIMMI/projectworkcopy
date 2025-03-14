import requests
from bs4 import BeautifulSoup
import csv

# Jobs
lavori = ['Admin','blue+collar','entrepreneur','housemaid','management','retired','self+employed','services','student','technician','unemployed','unknown']
# Adding the title of the columns
with open('average_salary.csv', 'a') as file:
      writer = csv.writer(file)
      writer.writerow(['Job', 'Average_Salary'])

# URL base per il job search
for lavoro in lavori:
  url = f"https://www.talent.com/salary?job={lavoro}&location="

  # Simulare un browser (User-Agent)
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }

  # Fare la richiesta
  response = requests.get(url, headers=headers)

  # Parsare la pagina HTML
  soup = BeautifulSoup(response.text, "html.parser")
  div = soup.find("div", class_="c-card__stats-mainNumber timeBased")

  # Estrai il testo se il div è stato trovato
  if div:
      print(f"{lavoro}:", div.text.strip())
      dati = div.text.strip()
      with open('average_salary.csv', 'a') as file:
        writer = csv.writer(file)
        if '+' in lavoro:
          lavoro = lavoro.replace('+', '-')
        writer.writerow([lavoro, dati])
  else:
      print("Elemento non trovato")