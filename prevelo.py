import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para buscar dados de uma página
def scrape_page(page_number):
    url = f"https://footballdatabase.com/ranking/world/{page_number}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Evita bloqueios
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Encontra a tabela
    table = soup.find("table")
    if not table:
        return None
    
    rows = table.find_all("tr")[1:]  # Ignora o cabeçalho
    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            rank = cols[0].text.strip()
            club_country = cols[1].text.strip()
            points = cols[2].text.strip()
            change = cols[3].text.strip()
            data.append([rank, club_country, points, change])
    return data

# Coleta dados de todas as páginas
all_data = []
for page in range(1, 61):  # De 1 a 60, conforme as páginas
    print(f"Coletando página {page}...")
    page_data = scrape_page(page)
    if page_data:
        all_data.extend(page_data)

# Cria um DataFrame e salva em CSV
if all_data:
    df = pd.DataFrame(all_data, columns=["Rank", "Club / Country", "Points", "1-yr change"])
    df.to_csv("football_rankings.csv", index=False)
    print("CSV salvo como football_rankings.csv")
else:
    print("Nenhum dado coletado.")
