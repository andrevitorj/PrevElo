import streamlit as st
import requests
from bs4 import BeautifulSoup

# Função para buscar times disponíveis
def search_teams(query):
    url = f"https://footballdatabase.com/search.php?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    teams = []
    # Busca links na página de resultados
    for result in soup.find_all("a", href=True):
        href = result["href"]
        if "clubs-ranking" in href and result.text.strip():  # Garante que é um link de clube e tem texto
            team_name = result.text.strip()
            team_url = "https://footballdatabase.com" + href
            teams.append((team_name, team_url))
    return teams

# Função para buscar o rating Elo (coluna "Points")
def get_elo_rating(team_url, team_name):
    response = requests.get(team_url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                club = cols[1].text.strip()  # Coluna "Club"
                if team_name.lower() in club.lower():  # Verifica se o nome do time corresponde
                    points = cols[2].text.strip()  # Coluna "Points"
                    return int(points) if points.isdigit() else None
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
            selected_name = selected_team.split(" (")[0]  # Extrai o nome do time
            selected_url = next(url for name, url in teams if f"{name} ({url.split('/')[-1]})" == selected_team)
            
            # Passo 4: Busca e exibe o rating Elo
            elo = get_elo_rating(selected_url, selected_name)
            if elo is not None:
                st.write(f"Rating Elo (Points): {elo}")
            else:
                st.error("Rating Elo não encontrado para este time.")
    else:
        st.error("Nenhum time encontrado.")
