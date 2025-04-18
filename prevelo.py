import streamlit as st
import requests
from bs4 import BeautifulSoup

# Função para buscar links de times na página de busca
def search_teams(query):
    url = f"https://footballdatabase.com/search.php?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Evita bloqueios
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    teams = []
    # Busca todos os links que contêm "clubs-ranking"
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "clubs-ranking" in href:
            team_name = link.text.strip()
            team_url = "https://footballdatabase.com" + href
            if team_name:  # Garante que o nome do time não está vazio
                teams.append((team_name, team_url))
    return teams

# Função para buscar o rating Elo (coluna "Points")
def get_elo_rating(team_url, team_name):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(team_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                club = cols[1].text.strip()
                if team_name.lower() in club.lower():
                    points = cols[2].text.strip()
                    return int(points) if points.isdigit() else None
    return None

# Interface Streamlit
st.title("Busca de Rating Elo - FootballDatabase")

# Passo 1: Input do nome do time
team_query = st.text_input("Digite o nome do time (ex.: Racing)", "")

if team_query:
    # Passo 2: Busca e lista os links encontrados
    teams = search_teams(team_query)
    if teams:
        st.write("Links encontrados para sua busca:")
        for team_name, team_url in teams:
            st.write(f"- {team_name}: {team_url}")
    else:
        st.error("Nenhum time encontrado. O site pode estar bloqueando a requisição ou a busca não retornou resultados.")
