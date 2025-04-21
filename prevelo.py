import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

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

# Função para coletar dados de todas as páginas e gerar CSV
def generate_csv():
    all_data = []
    for page in range(1, 61):  # De 1 a 60
        with st.spinner(f"Coletando página {page} de 60..."):
            page_data = scrape_page(page)
            if page_data:
                all_data.extend(page_data)
            else:
                st.warning(f"Não foi possível coletar dados da página {page}.")
    
    if all_data:
        df = pd.DataFrame(all_data, columns=["Rank", "Club / Country", "Points", "1-yr change"])
        # Converte o DataFrame para CSV em memória
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        csv_data = buffer.getvalue().encode('utf-8')
        return csv_data
    return None

# Interface Streamlit
st.title("Gerar CSV com Ratings Elo - FootballDatabase")

st.write("Clique no botão abaixo para coletar os ratings Elo de todos os times e baixar o CSV.")

if st.button("Gerar e Baixar CSV"):
    csv_data = generate_csv()
    if csv_data:
        st.success("CSV gerado com sucesso!")
        st.download_button(
            label="Baixar football_rankings.csv",
            data=csv_data,
            file_name="football_rankings.csv",
            mime="text/csv"
        )
    else:
        st.error("Falha ao gerar o CSV. O site pode estar bloqueando a requisição.")

# Seção para buscar ratings usando um CSV (opcional, caso o usuário já tenha o CSV)
st.write("---")
st.write("Ou carregue um CSV existente para buscar ratings Elo:")
csv_file = st.file_uploader("Carregue o CSV com os ratings Elo", type="csv")
team_query = st.text_input("Digite o nome do time (ex.: Racing)", "")

if team_query and csv_file:
    elo = get_elo_rating(team_query, csv_file)
    if elo is not None:
        st.write(f"Rating Elo (Points): {elo}")
    else:
        st.error("Time não encontrado no CSV. Verifique o nome ou o arquivo.")
elif not csv_file and team_query:
    st.warning("Por favor, carregue o arquivo CSV para buscar ratings.")

# Função para buscar o rating Elo no CSV (já implementada anteriormente)
def get_elo_rating(team_name, csv_file):
    if csv_file:
        df = pd.read_csv(csv_file)
        team_row = df[df["Club / Country"].str.contains(team_name, case=False, na=False)]
        if not team_row.empty:
            elo = float(team_row["Points"].iloc[0])
            return elo
    return None
