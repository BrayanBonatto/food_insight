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
import plotly.express as ex

#---------------------------------------------------------------------------------------------
#                                       FUNÇÕES ESCOPO VISÃO
#---------------------------------------------------------------------------------------------

def rest_with_online_order(df):    
    most_online_order = df.loc[df['has_online_delivery'] == 'Yes', ['city', 'has_online_delivery']].groupby('city').count().sort_values('has_online_delivery').reset_index()
    most_online_order_10 = most_online_order.tail(10)
    fig = px.bar(most_online_order_10, x = 'has_online_delivery', y = 'city', text= 'has_online_delivery')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Restaurantes que aceitam pedidos online',yaxis_title='Cidade')
    return fig

def rest_with_book(df):
    most_booking = (df.loc[df['has_table_booking'] == 'Yes', ['city', 'has_table_booking']].groupby('city').count().sort_values('has_table_booking').reset_index())
    most_booking_10 = most_booking.tail(10)
    fig = px.bar(most_booking_10, x = 'has_table_booking', y = 'city', text ='has_table_booking' )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Restaurantes que fazem reservas',yaxis_title='Cidade')
    fig.update_traces(marker_color='rgb(226, 100, 59)')
    return fig

def rest_with_deliver_by_city(df):   
    most_deliver = (df.loc[df['is_delivering_now'] == 'Yes', ['city', 'is_delivering_now']].groupby('city').count().sort_values('is_delivering_now', ascending = False).reset_index())
    most_deliver_10 = most_deliver
    most_deliver_10 = most_deliver_10.rename(columns = {'city': 'Cidade', 'is_delivering_now':'Número de Restaurantes com Entregas'})
    return most_deliver_10

def type_cuisines(df):   
    most_different_cuisine = df.groupby('city').agg({'cuisines': 'nunique', 'country_name': 'first'}).sort_values('cuisines', ascending = False).reset_index()
    most_different_cuisine_10 = most_different_cuisine
    most_different_cuisine_10 = most_different_cuisine_10.rename(columns={'cuisines': 'Nº de Culinárias','country_name': 'País', 'city': 'Cidade'})
    most_different_cuisine_10 = most_different_cuisine_10.reindex(['País', 'Cidade', 'Nº de Culinárias'], axis = 1)
    return most_different_cuisine_10

def scatter_tot_rest(df):
    rating_rest = (df.loc[df['aggregate_rating'] >=4].groupby('city').agg(unique_restaurant_count=('restaurant_name', 'nunique'), average_rating=('aggregate_rating', 'mean'))
                                                                     .sort_values('unique_restaurant_count', ascending=False).reset_index())
    rating_rest_aux = rating_rest.head(10)
    fig = px.scatter(rating_rest_aux, x='unique_restaurant_count'  , y='average_rating', color='city',size = 'unique_restaurant_count', text= 'unique_restaurant_count' , size_max = 45) 
    fig.update_traces(textposition='middle right',  textfont_size=18)
    st.markdown('##### Top 10 Restaurantes com nota média acima de 4.0 por Cidade')
    fig.update_layout(xaxis_title = 'Número de Restaurantes ', yaxis_title = 'Nota Média', margin=dict(l=70, r=70, b=50, t=50),  legend=dict(font=dict(size=20)))
    return fig

def high_prices_by_city(df):
    highest_average_pricecity = df.loc[:,['city', 'converted_to_dollar']].groupby('city').max().sort_values('converted_to_dollar').reset_index()
    highest_average_pricecity_10 = highest_average_pricecity.tail(10)
    fig = px.bar(highest_average_pricecity_10, x ='converted_to_dollar', y = 'city', text = 'converted_to_dollar')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Preço Médio', yaxis_title='Cidade')
    fig.update_traces(marker_color='rgb(10, 35, 81)')
    return fig

def number_rest_by_city_2(df):
    rating_rest_bad = df.loc[df['aggregate_rating'] < 2.5, ['city', 'restaurant_name']].groupby('city').count().sort_values('restaurant_name').reset_index()
    rating_rest_bad_10 = rating_rest_bad.head(10)
    fig = px.bar(rating_rest_bad_10, x = 'restaurant_name', y = 'city', text = 'restaurant_name' )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Restaurantes', yaxis_title='Cidade')
    return fig

def number_rest_by_city(df):                                            
    tab_restaurant_per_city =df.loc[:,['restaurant_name', 'city', 'country_name']].groupby(['country_name','city']).count().sort_values('restaurant_name').reset_index()
    tab_restaurant_per_city_aux = tab_restaurant_per_city.tail(10)
    fig = px.bar(tab_restaurant_per_city_aux, x = 'restaurant_name', y = 'city', text = 'restaurant_name')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Restaurantes', yaxis_title='Cidade',)
    fig.update_traces(marker_color='rgb(226, 100, 59)')
    return fig

def dados_gerais():                                                     #Monta os 'Dados Gerais' Diretamente  
    with col1:
        st.subheader('Nº Restaurantes')
        st.metric('',value = df.loc[:,'restaurant_name'].nunique() )
    with col2:
        st.subheader('Nº Países')
        st.metric('',value = df.loc[:,'country_name'].nunique() )
    with col3:
        st.subheader('Nº Cidades')
        st.metric('' ,value = df.loc[:,'city'].nunique() )
    with col4:
        st.subheader('Nº Avaliações')
        st.metric('',value = millify(df.loc[:,'votes'].sum().round(), precision = 2) )
    with col5:
        st.subheader('Nº Culinárias')
        st.metric('',value = df.loc[:,'cuisines'].nunique() )



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
    214: "United Arab Emirates", 
    215: "England",     216: "United States of America"}

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

st.set_page_config(page_title = 'Visão Dados Gerais',layout="wide")                                       # Comando para usar todo o espaço do Streamlit

sidebar()
with st.sidebar:
    all_country = ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada','Singapure', 'United Arab Emirates', 
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

titles('Visão Dados Gerais')

#___________________________________________________________________________________________________________________________________________________________
st.container()
col1, col2, col3, col4, col5 = st.columns(5)
dados_gerais()

st.markdown("""---""")

titles('Visão Cidades')

#___________________________________________________________________________________________________________________________________________________________
st.container()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('##### Cidades com mais Restaurantes')
    fig = number_rest_by_city(df)
    st.plotly_chart(fig, use_container_width = True)

with col2:
    st.markdown('##### Nº de Restaurantes (Nota < 2.5)')
    fig = number_rest_by_city_2(df)
    st.plotly_chart(fig, use_container_width = True)

with col3:
    st.markdown('##### Cidades com Pratos par 2 Mais Caros')
    fig = high_prices_by_city(df)
    st.plotly_chart(fig, use_container_width = True)
    
#___________________________________________________________________________________________________________________________________________________________
st.container()

fig = scatter_tot_rest(df)
st.plotly_chart(fig, use_container_width = True)

#___________________________________________________________________________________________________________________________________________________________
st.container()
col1, col2 = st.columns(2)

with col1:
    st.markdown('##### Tabela com Número de Culinárias por Cidade')
    most_different_cuisine_10 = type_cuisines(df)
    st.dataframe(most_different_cuisine_10, use_container_width = True)
    
with col2:
    st.markdown('##### Número de Restaurantes que fazem entregas por Cidade')
    dfaux = rest_with_deliver_by_city(df)
    st.dataframe(dfaux, use_container_width = True)

#___________________________________________________________________________________________________________________________________________________________
st.container()

col1, col2 = st.columns(2)
with col1:
    st.markdown('##### Número de Restaurantes que fazem reservas por Cidade')
    fig = rest_with_book(df) 
    st.plotly_chart(fig, use_container_width = True)

with col2:
    st.markdown('##### Número de Restaurantes que aceitam pediso online por Cidade')
    fig = rest_with_online_order(df)
    st.plotly_chart(fig, use_container_width = True)


























