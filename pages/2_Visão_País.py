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
def city_by_country(df):
    city_per_country = (df.loc[:,['country_name', 'city']].groupby('country_name').nunique().sort_values('city').reset_index())
    city_per_country_10 = city_per_country.tail(10)
    fig = px.bar(city_per_country_10, x = 'city', y = 'country_name', text = 'city')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Cidades', yaxis_title='País')
    fig.update_traces(marker_color='rgb(226, 100, 59)')
    return fig

def rest_per_country(df):
    restaurant_per_country = (df.loc[:,['country_name', 'restaurant_name']].groupby('country_name').nunique().sort_values('restaurant_name').reset_index())
    restaurant_per_country_10 = restaurant_per_country.tail(10)
    fig = px.bar(restaurant_per_country_10, x = 'restaurant_name', y = 'country_name', text = 'restaurant_name')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Restaurantes', yaxis_title='País')
    return fig

def rest_per_country_4(df):   
    restaurant_per_country = (df.loc[df['price_range'] == 4 ,['country_name', 'restaurant_id']].groupby('country_name').count().sort_values('restaurant_id', ascending = True).reset_index())
    restaurant_per_country_10 = restaurant_per_country.tail(10)
    fig = px.bar(restaurant_per_country_10, x = 'restaurant_id', y = 'country_name', text = 'restaurant_id')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Restaurantes(Nota Média >= 4.0)', yaxis_title='País')
    fig.update_traces(marker_color='rgb(10, 35, 81)')
    return fig

def cuisines_per_country(df):    
    cusines_per_country = df.loc[:,['country_name', 'cuisines']].groupby('country_name').nunique().sort_values('cuisines', ascending = True).reset_index()
    cusines_per_country_10 = cusines_per_country.tail(10)
    fig = px.bar(cusines_per_country_10, x = 'cuisines', y = 'country_name', text = 'cuisines')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Culinárias Distintas', yaxis_title='País')
    fig.update_traces(marker_color='rgb(226, 100, 59)')
    return fig

def votes_per_country(df):    
    votes_per_country = df.loc[:,['country_name', 'votes']].groupby('country_name').sum().sort_values('votes').reset_index()
    votes_per_country_10= votes_per_country.tail(3)
    fig = px.pie(votes_per_country_10, values = 'votes', color = 'country_name', names = 'country_name', 
                 color_discrete_map={'E. Arabes': 'rgb(226, 100, 59)' , 'USA': 'rgb(131, 201, 255)', 'India': 'rgb(10, 35, 81)'})
    fig.update_traces(textposition='outside', textinfo='value+percent', textfont=dict(size=19))
    fig.update_layout(legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1,font=dict(size=17)), width=500, height=400, margin=dict(l=50, r=15, b=0, t=60))
    return fig

def reest_order_per_country(df):
    delivery_per_country = (df.loc[df['has_online_delivery'] == 'Yes', ['country_name', 'has_online_delivery']].groupby('country_name').count()
                                                                                                               .sort_values('has_online_delivery', ascending = False).reset_index())
    delivery_per_country_10 = delivery_per_country.head(3)
    fig = px.pie(delivery_per_country_10, values = 'has_online_delivery', color = 'country_name', names = 'country_name', 
                 color_discrete_map={'Qatar': 'rgb(226, 100, 59)' , 'E. Arabes': 'rgb(131, 201, 255)', 'India': 'rgb(10, 35, 81)'})
    fig.update_traces(textposition='outside', textinfo='value+ percent', textfont=dict(size=19))
    fig.update_layout(legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1,font=dict(size=17)), width=500, height=400, margin=dict(l=50, r=15, b=0, t=60))
    return fig

def rest_booking_per_country(df):
    tbokking = df.loc[df['has_table_booking'] == 'Yes',['country_name', 'has_table_booking']].groupby('country_name').count().sort_values('has_table_booking').reset_index()
    fig = px.bar(tbokking, x = 'has_table_booking', y = 'country_name', text = 'has_table_booking')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número de Restaurantes que Aceitam Reserva', yaxis_title='País')
    fig.update_traces(marker_color='rgb(226, 100, 59)')
    return fig

def avg_votes_per_country(df):    
    qtt_votes_by_country = df.loc[:,['country_name', 'votes']].groupby('country_name').mean().sort_values('votes').reset_index().round(1)
    qtt_votes_by_country_10 = qtt_votes_by_country.tail(10)
    fig = px.bar(qtt_votes_by_country_10, x= 'votes', y = 'country_name', text = 'votes', height = 450)
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Número Médio de Avaliações', yaxis_title='País')
    return fig

def high_review_per_country(df):    
    high_rate =df.loc[:,['country_name', 'aggregate_rating']].groupby('country_name').mean().sort_values('aggregate_rating').reset_index()
    high_rate_10 = high_rate.tail(10)
    high_rate_10['aggregate_rating'] = high_rate_10['aggregate_rating'].round(2)
    fig = px.bar(high_rate_10, x = 'aggregate_rating', y = 'country_name', text = 'aggregate_rating' )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Maior Nota Registrada', yaxis_title='País')
    fig.update_traces(marker_color='rgb(10, 35, 81)')
    return fig

def avg_price_per_country(df):
    price_avg = (df.loc[df['average_cost_for_two'] != 0, ['currency','country_name', 'average_cost_for_two', 'converted_to_dollar']].groupby(['country_name', 'currency']).mean().round(2).reset_index())
    fig = (px.scatter(price_avg, y='converted_to_dollar', color='country_name',text='$ ' + price_avg['converted_to_dollar']
                    .astype(str),size = price_avg['converted_to_dollar'],hover_data=['country_name', 'converted_to_dollar'], size_max = 45) )
    fig.update_traces(textposition='middle right', textfont_size=18)
    fig.update_layout(xaxis_title = 'Número de Países', yaxis_title = 'Preço', margin=dict(l=70, r=70, b=50, t=50),  legend=dict(font=dict(size=20)))
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

titles('Visão País')
st.markdown('''___''')
#___________________________________________________________________________________________________________________________________________________________

st.container()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('##### Número de Cidades por País')
    fig = city_by_country(df)
    st.plotly_chart(fig, use_container_width = True)

with col2:
    st.markdown('##### Número de Restaurantes por País')
    fig = rest_per_country(df)
    st.plotly_chart(fig, use_container_width = True)

with col3:
    st.markdown('##### Restaurantes por País (Média > 4.0)')
    fig = rest_per_country_4(df)
    st.plotly_chart(fig, use_container_width = True)
#___________________________________________________________________________________________________________________________________________________________

st.container()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('##### Número de Culinárias Distintas por Páis')
    fig = cuisines_per_country(df)
    st.plotly_chart(fig, use_container_width = True)

with col2:
    st.markdown('##### Número de Avaliações feitas por País')
    fig = votes_per_country(df)
    st.plotly_chart(fig, use_container_width = True)

with col3:
    st.markdown('##### Restaurantes que fazem entrega por País')   
    fig = reest_order_per_country(df)
    st.plotly_chart(fig, use_container_width = True)
#___________________________________________________________________________________________________________________________________________________________

st.container()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('##### Restaurantes com Reserva por País')    
    fig = rest_booking_per_country(df)
    st.plotly_chart(fig, use_container_width = True)

with col2:
    st.markdown('##### Número Médio de Avaliações por País')    
    fig = avg_votes_per_country(df)
    st.plotly_chart(fig, use_container_width = True)

with col3:
    st.markdown('##### Maior Nota registrada por País')    
    fig = high_review_per_country(df)
    st.plotly_chart(fig, use_container_width = True)
#___________________________________________________________________________________________________________________________________________________________

st.container()

st.markdown('##### Média de Preço de um prato para 2 por País')    
fig = avg_price_per_country(df)
st.plotly_chart(fig, use_container_width = True)






