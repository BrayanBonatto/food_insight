#---------------------------------------------------------------------------------------------
#                                  IMPORT DAS BIBLIOTECAS
#---------------------------------------------------------------------------------------------

import pandas as pd
import streamlit as st
import inflection
import numpy as np
import plotly.express as px
from PIL import Image
from millify import millify
import plotly.express as px

#---------------------------------------------------------------------------------------------
#                                       FUNÇÕES ESCOPO VISÃO
#---------------------------------------------------------------------------------------------

def votes_per_restaurant(df):    
    most_votes = (df.loc[:,['restaurant_name','votes']].groupby('restaurant_name').sum().sort_values('votes').reset_index())
    most_votes_10 = most_votes.tail(10)
    fig = px.bar(most_votes_10, x = 'votes', y = 'restaurant_name', text = most_votes_10['votes'].apply(lambda x: millify(x)))                                                               
    fig.update_traces(textposition='outside',marker_color='rgb(226, 100, 59)')
    fig.update_layout(xaxis_title = 'Número total de votos', yaxis_title = 'Restaurantes', height = 470, width = 600, margin=dict(l=50, r=15, b=30, t=60))
    return fig

def high_price_food(df):   
    high_cost_for_two = (df.loc[:,['restaurant_id','restaurant_name','converted_to_dollar']].groupby('restaurant_name').max()
                                                                                            .sort_values(by=['converted_to_dollar','restaurant_id'], ascending = [True, True]).reset_index())
    high_cost_for_two_10 = high_cost_for_two.tail(10)
    fig = px.bar(high_cost_for_two_10, x = 'converted_to_dollar', y = 'restaurant_name', text = 'converted_to_dollar')
    fig.update_traces(textposition='outside',marker_color='rgb(10, 35, 81)')  
    fig.update_layout(xaxis_title = 'Valores (em Dolar)', yaxis_title = 'Restaurantes',height = 470, width = 600, margin=dict(l=50, r=15, b=30, t=60))
    return fig

def high_rate_high_votes(df):    
    high_avg_rate = (df.loc[:,['country_name', 'restaurant_name','aggregate_rating', 'votes' ]].groupby('restaurant_name').max()
                                                                                                                          .sort_values(by=['aggregate_rating','votes'], ascending = [False, False]).reset_index())
    high_avg_rate_10 = high_avg_rate.head(10)
    high_avg_rate_10 = high_avg_rate_10.reindex(columns=['country_name', 'restaurant_name', 'aggregate_rating', 'votes'])
    high_avg_rate_10 = high_avg_rate_10.rename(columns={'country_name': 'País', 'restaurant_name': 'Nome do Restaurante', 'aggregate_rating':'Nota Média', 'votes':'Avaliações'})
    return high_avg_rate_10

def brazilian_food_low(df):   
    lines = (df['cuisines'] == 'Brazilian') & (df['aggregate_rating'] != 0.0) & (df['country_name'] != 'Brazil')
    low_rate_brazilian_food = df.loc[lines,['country_name','cuisines', 'restaurant_name','aggregate_rating']].sort_values('aggregate_rating').reset_index(drop= True).round(2)
    low_rate_brazilian_food_3 = low_rate_brazilian_food.head(3)
    low_rate_brazilian_food_3 = low_rate_brazilian_food_3.rename(columns={'country_name': 'País', 'cuisines': 'Culinária', 'restaurant_name':'Nome do Restaurante', 
                                                                          'aggregate_rating':'Nota Média', 'converted_to_dollar':'Preço (em Dólar)'})
    return low_rate_brazilian_food_3

def brazilian_food_low_2(df):
    lines = (df['cuisines'] == 'Brazilian') & (df['aggregate_rating'] != 0.0) & (df['country_name'] != 'Brazil')
    low_rate_brazilian_food_from_br = df.loc[lines,['country_name','cuisines', 'restaurant_name','aggregate_rating']].sort_values('aggregate_rating').reset_index(drop= True).round(2)
    low_rate_brazilian_food_from_br_3 = low_rate_brazilian_food_from_br.head(3)
    low_rate_brazilian_food_from_br_3 = low_rate_brazilian_food_from_br_3.rename(columns = {'country_name':'País', 'cuisines':'Culinária', 'restaurant_name':'Nome do Restaurante', 
                                                                                            'aggregate_rating':'Nota Média'})
    return low_rate_brazilian_food_from_br_3

def online_rate(df):   
    rest_online_order = df.loc[:, ['has_online_delivery', 'votes']].groupby('has_online_delivery').mean().reset_index()
    fig = px.pie(rest_online_order, values = 'votes', color = 'has_online_delivery', names =rest_online_order['has_online_delivery'], color_discrete_map={'Yes': 'rgb(226, 100, 59)' , 'No': 'rgb(10, 35, 81)'})
    fig.update_layout(legend=dict(font=dict(size=17)),width = 500, margin=dict(l=50, r=15, b=0, t=60))
    fig.update_traces(textposition='inside', textinfo='percent', textfont=dict(size=19))
    return fig

def book_price(df):   
    rest_booking = df.loc[:,['has_table_booking', 'converted_to_dollar']].groupby(['has_table_booking']).mean().round(2).reset_index()
    fig = px.pie(rest_booking, values = 'converted_to_dollar', color = 'has_table_booking', names = 'has_table_booking', color_discrete_map={'Yes': 'rgb(226, 100, 59)' , 'No': 'rgb(10, 35, 81)'})
    fig.update_layout(legend=dict(font=dict(size=17)),width = 500,margin=dict(l=50, r=15, b=0, t=60)) 
    fig.update_traces(textposition='inside', textinfo='percent', textfont=dict(size=19))  
    return fig

def japan_bbq_price(df):   
    lines = (df['cuisines'] == 'Japanese') & (df['country_name'] == 'USA') | (df['cuisines'] == 'BBQ') & (df['country_name'] == 'USA')
    japa_bbq = df.loc[lines,['cuisines','converted_to_dollar']].groupby('cuisines').mean().reset_index()
    fig = px.pie(japa_bbq , values = 'converted_to_dollar', color = 'cuisines', names = 'cuisines', color_discrete_map={'Japanese': 'rgb(226, 100, 59)' , 'BBQ': 'rgb(10, 35, 81)'})
    fig.update_layout(legend=dict(font=dict(size=17)),width = 500, margin=dict(l=0, r=15, b=0, t=60))
    fig.update_traces(textposition='inside', textinfo='percent', textfont=dict(size=19))  
    return fig
    
#---------------------------------------------------------------------------------------------
#                                       FUNÇÕES ESCOPO GERAL
#---------------------------------------------------------------------------------------------

def titles(name):                                                       # Adiciona o título centralizado   
    st.markdown(f"""
        <div style="text-align: center; font-size: 50px; font-weight: bold;">{name}</div>""", unsafe_allow_html=True)

def sidebar():                                                          # Monta a barra lateral no Streamlit  
    with st.sidebar:
        st.title('Food Tech Insights')
        image = Image.open('logo.jpg')
        st.sidebar.image(image, width = 287)
        st.sidebar.markdown("""---""")         
        
def clean_code(df):                                                     # Limpa o Código dos 'NaN', exclui colunas com valores únicos e Troca 0 por 'Não' e 1 por 'Sim'   
    df['cuisines'] = df['cuisines'].replace("NaN", np.nan)
    df = df.dropna(subset = 'cuisines')
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    
    df.drop('switch_to_order_menu', axis=1, inplace=True)
    df.drop('country_code', axis=1, inplace=True)
    df.drop(index=385, inplace=True)
    df.drop(index=[6049,6050], inplace=True)
    
    df['has_online_delivery'] = df['has_online_delivery'].replace({0: 'No', 1: 'Yes'})
    df['has_table_booking'] = df['has_table_booking'].replace({0: 'No', 1: 'Yes'})
    df['is_delivering_now'] = df['is_delivering_now'].replace({0: 'No', 1: 'Yes'})
    return(df)

def rename_columns(dataframe):                                          # Renomeia as colunas do Dataframe para otimização
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def converter_para_dolar(row):                                          # Converte o valor médio gasto para duas pessoas em diferentes moedas para dólares americanos (USD).
    moeda = row['currency']                                             # Retorna:   float: O valor convertido em dólares americanos (USD).
    moeda = row['currency']                                             
    valor = row['average_cost_for_two']
    return valor * taxas_cambio[moeda]

#---------------------------------------------------------------------------------------------
#                                        TRANSFORMAÇÃO 
#---------------------------------------------------------------------------------------------

# Dicionário de 'Moeda: valor' para converter para Dólar
taxas_cambio = {
    'Botswana Pula(P)': 0.0747,                                         # 1 BWP = 0.0747 USD
    'Brazilian Real(R$)': 0.1953,                                       # 1 BRL = 0.1953 USD
    'Dollar($)': 1.0,                                                   # 1 USD = 1.0 USD
    'Emirati Diram(AED)': 0.2723,                                       # 1 AED = 0.2723 USD
    'Indian Rupees(Rs.)': 0.0120,                                       # 1 INR = 0.0120 USD
    'Indonesian Rupiah(IDR)': 0.000064,                                 # 1 IDR = 0.000064 USD
    'NewZealand($)': 0.5980,                                            # 1 NZD = 0.5980 USD
    'Pounds(£)': 1.2160,                                                # 1 GBP = 1.2160 USD
    'Qatari Rial(QR)': 0.2747,                                          # 1 QAR = 0.2747 USD
    'Rand(R)': 0.0520,                                                  # 1 ZAR = 0.0520 USD
    'Sri Lankan Rupee(LKR)': 0.0031,                                    # 1 LKR = 0.0031 USD
    'Turkish Lira(TL)': 0.0375                                          # 1 TRY = 0.0375 USD
}

# Dicionário de 'Código: País' para fazer a transformação no DF
countries = {
    1: "India",         14: "Australia",  
    30: "Brazil",       37: "Canada", 
    94: "Indonesia",    148: "New Zeland", 
    162: "Philippines", 166: "Qatar", 
    184: "Singapure",   189: "South Africa", 
    191: "Sri Lanka",   208: "Turkey", 
    214: "E. Arabes", 
    215: "England",     216: "USA"}

#---------------------------------------------------------------------------------------------
#                             INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO
#---------------------------------------------------------------------------------------------

tab = pd.read_csv('zomato.csv')                                         #Leitura do arquivo
df = tab.copy()                                                         #Copia de segurança
df = rename_columns(df)                                                 #Renomeando colunas
df['converted_to_dollar'] = df.apply(converter_para_dolar, axis=1)      #Corventendo todos os preços para $ Dollar            
df['country_name'] = df['country_code'].map(countries)                  #Pondo nomes nos Países
df = clean_code(df)                                                     #Limpando o código

#===========================================
#              BARRA LATERAL
#===========================================

st.set_page_config(layout="wide")                                       # Comando para usar todo o espaço do Streamlit

sidebar()
with st.sidebar:
    all_country = ['Philippines', 'Brazil', 'Australia', 'USA', 'Canada','Singapure', 'E. Arabes', 
                   'India', 'Indonesia', 'New Zeland','England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey']
    
    country = st.multiselect('Países', all_country,all_country )        # Filtro de multiselect dos Países (Default: todos)
    linhas_country = df['country_name'].isin(country)
    df = df.loc[linhas_country,:]

    st.sidebar.markdown("""---""") 

    if country:
        filtered_cities = df[df["country_name"].isin(country)]["city"].unique()
        city = st.selectbox("Selecione uma Cidade (opcional)", options=[""] + list(filtered_cities))
        
        # Aplica o filtro de cidade, se alguma for selecionada
        if city:
            linhas_city = df['city'] == city
            df = df.loc[linhas_city, :]
    
    st.sidebar.markdown("""---""")   
    
    nota = st.slider('Selecione uma faixa de Notas', 0.0, 5.0, 5.0)     # Filtro slider de faixa de notas médias (Default: 5.0)
    linhas_nota = df['aggregate_rating'] <= nota
    df = df.loc[linhas_nota,:]
    
    preco = st.slider('Selecione uma faixa de preço', 0, 800, 800)      #Filtro Slider de faixa de preço médio dos pratos para 2 (Valores convertidos para Dólar) Default: 800
    linhas_preco = df['converted_to_dollar'] <= preco
    df = df.loc[linhas_preco,:]
    
    st.sidebar.markdown("""---""")
    st.sidebar.markdown('### Powered by BB')

#===========================================
#              LAYOUT PRINCIPAL
#===========================================

titles('Visão Restaurantes')
st.markdown('''___''')
#___________________________________________________________________________________________________________________________________________________________

st.container()

col1, col2 = st.columns(2)

with col1:
    st.markdown('##### Número total de votos por restaurante')
    fig = votes_per_restaurant(df)
    st.plotly_chart(fig, use_container_width = True)
    
with col2:
    st.markdown('##### Restaurantes com os pratos para 2 mais caros')
    fig = high_price_food(df)
    st.plotly_chart(fig, use_container_width = True)
#___________________________________________________________________________________________________________________________________________________________

st.container()
st.markdown('''___''')
col1, col2 = st.columns(2)

with col1:
    st.markdown('##### Top 10 -  Maior Nota com Mais Votos por Restaurante')
    high_avg_rate_10 = high_rate_high_votes(df)
    st.dataframe(high_avg_rate_10, use_container_width = True)

with col2:
    #___________________________________________________________________________________________________________________________________________________________

    st.container()
    st.markdown('##### Restaurantes de Culinária Brasileira                                    com Menor Nota Média')
    low_rate_brazilian_food_3 = brazilian_food_low(df)                                                                   
    st.dataframe(low_rate_brazilian_food_3, use_container_width = True)
    #___________________________________________________________________________________________________________________________________________________________

    st.container()
    st.markdown('##### Restaurantes Culinária Brasileira do Brasil com menor nota média')    
    low_rate_brazilian_food_from_br_3 = brazilian_food_low_2(df)
    st.dataframe(low_rate_brazilian_food_from_br_3, use_container_width = True)
#___________________________________________________________________________________________________________________________________________________________

st.container()
st.markdown('''___''')
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('##### Restaurantes com Pedidos Online são os que Possuem Mais Avaliações?')    
    fig = online_rate(df)
    st.plotly_chart(fig)

with col2:
    st.markdown('##### Restaurantes com Reserva são os que Possuem Maior Preço Médio?')    
    fig = book_price(df)
    st.plotly_chart(fig)
    
with col3:
    st.markdown('##### Maior Preço Médio: Comida Japonesa X Churrasco (EUA)')   
    fig = japan_bbq_price(df)
    st.plotly_chart(fig)
    





































