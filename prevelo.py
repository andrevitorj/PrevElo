import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Função para buscar links de times na página de busca
def search_teams(query):
    # Configura o Selenium para rodar em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://footballdatabase.com/search.php?q={query}"
    
    try:
        driver.get(url)
        # Aguarda o carregamento da página
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        teams = []
        
        # Busca links de clubes
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "clubs-ranking" in href:
                team_name = link.text.strip()
                team_url = "https://footballdatabase.com" + href
                if team_name:
                    teams.append((team_name, team_url))
        
        return teams
    finally:
        driver.quit()

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
