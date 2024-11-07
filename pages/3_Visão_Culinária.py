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

def avg_rate(avg = 'High'): 
    # Retorna o nome do restaurante com maior ou menor media de avaliação. 
    #Args:
     #   cuisine (str): Tipo de culinária ('Italian', 'BBQ'..).
     #   avg (str, optional): 'High' para a maior média, 'Low' para a menor. Defaults to 'High'.
    
    type_cuisines = ['Italian', 'American', 'Arabian', 'Japanese', 'Home-made']
    results = []
    
    for i in type_cuisines:
        if avg == 'High':
            lines = df['cuisines'] == i
            restaurant_name = df.loc[lines, ['restaurant_name','cuisines', 'aggregate_rating', 'votes']].sort_values(by = ['aggregate_rating', 'votes'], ascending = False).reset_index(drop=True) 
        else:
            lines = (df['cuisines'] == i) & (df['votes'] != 0) & (df['aggregate_rating'] != 0)
            restaurant_name = df.loc[lines, ['restaurant_name','cuisines', 'aggregate_rating', 'votes']].sort_values(by = ['aggregate_rating', 'votes']).reset_index(drop=True)
        results.append(restaurant_name)
    df_final = pd.concat(results, ignore_index=True)
    df_final = df_final.groupby('cuisines').first().reset_index()
    return df_final

def high_and_low_rate(df):
    fig = px.scatter(c, y='aggregate_rating', color='cuisines',text='aggregate_rating', size ='votes', size_max = 45)
    fig.update_traces(textposition='middle right', textfont_size=19)
    fig.update_layout(xaxis_title = 'Número de Cozinhas', yaxis_title = 'Nota Média', margin=dict(l=70, r=70, b=50, t=50),  legend=dict(font=dict(size=20)),  legend_title_text='Culinária')
    return fig

def high_price(df):
    high_avg = df.loc[:,['cuisines', 'converted_to_dollar', 'country_name', 'average_cost_for_two','currency']].groupby('cuisines').max().sort_values('converted_to_dollar', ascending = False).reset_index()
    high_avg_10 = high_avg.head(30)
    fig = px.bar(high_avg_10, x = 'cuisines', y = 'converted_to_dollar', text = 'converted_to_dollar', color = 'country_name')
    fig.update_traces(textposition = 'outside', textfont=dict(size=19))
    fig.update_xaxes(tickangle=90)
    fig.update_layout( margin=dict(l=0, r=0, b=0, t=0), width=5000, height=500, xaxis_title='Culinária', yaxis_title='Valor médio do prato pra 2', legend_title_text='País')
    return fig

def votes_high_rate(df):
    high_avg_rate = (df.loc[:,['cuisines', 'aggregate_rating', 'votes']].groupby('cuisines').agg({'aggregate_rating': 'max', 'votes':'sum'})
                                                                        .sort_values(by= ['aggregate_rating','votes'], ascending = False).reset_index())
    high_avg_rate_15 = high_avg_rate.head(15)
    fig = px.bar(high_avg_rate_15, x = 'cuisines', y = 'votes', text = high_avg_rate_15['votes'].apply(lambda x: millify(x)))
    fig.update_xaxes(tickangle=90)
    fig.update_traces(textposition = 'outside', marker_color = 'rgb(226, 100, 59)', textfont=dict(size=15) )
    fig.update_layout(xaxis_title = 'Culinárias', yaxis_title = 'Avaliações', width = 400, height = 500)
    return fig

def cuisines_rest(df):  
    lines = (df['has_online_delivery'] == 'Yes') & (df['is_delivering_now'] == 'Yes')
    contagem_por_culinaria = df.loc[lines, ['cuisines', 'restaurant_name']].groupby('cuisines')['restaurant_name'].nunique()
    df_aux_1 = pd.DataFrame(contagem_por_culinaria)
    df_aux_2 = df_aux_1.sort_values('restaurant_name', ascending= False).reset_index()
    fig = px.bar(df_aux_2.head(15), x = 'cuisines', y = 'restaurant_name', text = 'restaurant_name')
    fig.update_traces(textposition = 'outside', marker_color='rgb(10, 35, 81)', textfont=dict(size=15))
    fig.update_layout(xaxis_title = 'Culinárias', yaxis_title = 'Número de Restaurantes', width = 700, height = 500)
    fig.update_xaxes(tickangle=90)

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

titles('Visão Culinária')
st.markdown('''___''')
#___________________________________________________________________________________________________________________________________________________________

st.container()
st.markdown('### Nota Mais Alta e Mais Baixa por tipo de Culinária')
a = avg_rate(avg = 'Low')
b = avg_rate(avg = 'High')
c = pd.concat([a, b])

fig = high_and_low_rate(c)
st.plotly_chart(fig)
#___________________________________________________________________________________________________________________________________________________________

st.container()
st.markdown('### Os Pratos pra 2 mais caros por País e por Culinária')
fig = high_price(df)
st.plotly_chart(fig)
#___________________________________________________________________________________________________________________________________________________________

st.container()

col1, col2 = st.columns(2)

with col1:
    st.markdown('### Número Total de avaliações feitas para restaurantes com nota Média de 4.9')
    fig = votes_high_rate(df)
    st.plotly_chart(fig, use_container_width = True)

with col2:
    st.markdown('### Culinárias com mais restaurantes que fazem entregas e aceitam pedidos online')
    fig = cuisines_rest(df)
    st.plotly_chart(fig)
























