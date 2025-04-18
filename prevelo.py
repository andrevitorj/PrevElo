import streamlit as st
import requests
from bs4 import BeautifulSoup

# Função para buscar times disponíveis
def search_teams(query):
    url = f"https://footballdatabase.com/search.php?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    teams = []
    for result in soup.find_all("a", href=True):
        if "clubs-ranking" in result["href"]:
            team_name = result.text.strip()
            team_url = "https://footballdatabase.com" + result["href"]
            teams.append((team_name, team_url))
    return teams

# Função para buscar o rating Elo (coluna "Points")
def get_elo_rating(team_url):
    response = requests.get(team_url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Encontra a tabela que contém "Points"
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                # Verifica se a coluna "Club" contém o nome do time
                club = cols[1].text.strip()
                # Extrai o "Points" da terceira coluna
                points = cols[2].text.strip()
                if points.isdigit():
                    return int(points)
    return None

# Interface Streamlit
st.title("Busca de Rating Elo - FootballDatabase")

# Passo 1: Input do nome do time
team_query = st.text_input("Digite o nome do time (ex.: Racing)", "")

if team_query:
    # Passo 2: Busca e exibe lista de times encontrados
    teams = search_teams(team_query)
    if teams:
        team_options = [f"{name} ({url.split('/')[-1]})" for name, url in teams]
        selected_team = st.selectbox("Escolha o time:", team_options)
        
        # Passo 3: Usuário escolhe o time
        if selected_team:
            # Extrai a URL correspondente ao time selecionado
            selected_url = next(url for name, url in teams if f"{name} ({url.split('/')[-1]})" == selected_team)
            
            # Passo 4: Busca e exibe o rating Elo
            elo = get_elo_rating(selected_url)
            if elo is not None:
                st.write(f"Rating Elo (Points): {elo}")
            else:
                st.error("Rating Elo não encontrado para este time.")
    else:
        st.error("Nenhum time encontrado.")
