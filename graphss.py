# graphss
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

url = "https://www.earj.com.br/university-acceptances/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

text = 'Class of 2023 Acceptances'
for i in soup.find_all('h2'):
    if(i.string == text):
        pointer = i
        break

# encontrar os países
for paises in pointer.find_all_next("a", {'role': 'button'}):
    print(paises)

dict_universidades = {'País':[], 'Universidade':[]}
# encontra os países apenas da seção depois de 2023
for paises in pointer.find_all_next("a", {'role': 'button'}):
    tabela = paises['href'][1:]
    pais = paises.text
    st.write(pais)
    div = paises.find_next('div', {'id': tabela})
    for universidade in div.find_all("li"):
        st.write(universidade.text)
        dict_universidades['País'].append(pais)
        dict_universidades['Universidade'].append(universidade.text)
    st.write()

df = pd.DataFrame.from_dict(dict_universidades)

df

df= pd.DataFrame.from_dict(dict_universidades)
if df is not None:
    if "País" in df.columns:  # Verifica se a coluna "País" existe no DataFrame
        regiões_especificas = ['United States', 'United Kingdom', 'Europe', 'Canada', 'Brazil']
        região_selecionada = st.selectbox("Pick a region", regiões_especificas)
        df_filtrado = df[df['País'] == região_selecionada]
        if not df_filtrado.empty:
            st.write("Dados Filtrados")
            st.dataframe(df_filtrado)
            st.write("Chart")
            chart_data = df_filtrado.groupby("Universidade").size()
            st.bar_chart(chart_data)
        else:
            st.write("Dado não encontrado")
    else:
        st.write("Coluna 'País' não encontrada no Data Frame")
