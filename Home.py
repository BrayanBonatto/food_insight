#---------------------------------------------------------------------------------------------
#                                  IMPORT DAS BIBLIOTECAS
#---------------------------------------------------------------------------------------------
import streamlit as st
from PIL import Image

#---------------------------------------------------------------------------------------------
#                                       FUNÇÕES ESTILIZADAS
#---------------------------------------------------------------------------------------------

def titles(name):   
    # Título centralizado e estilizado
    st.markdown(
        f"""<h1 style="text-align: center; color: #E2643B; font-size: 50px;">{name}</h1>""",
        unsafe_allow_html=True
    )

def subtitles(name):  
    # Subtítulo centralizado e estilizado
    st.markdown(
        f"""<h2 style="text-align: center; color: #E2643B; font-size: 40px;">{name}</h2>""",
        unsafe_allow_html=True
    )

def sidebar():
    # Monta a barra lateral com logo e tema
    with st.sidebar:
        st.title('🍲 Food Tech Insights')
        image = Image.open('logo.jpg')
        st.image(image, width=200)
        st.markdown("---")        
        st.write("🔍 Explore as melhores insights para o setor de restaurantes e gastronomia.")

#---------------------------------------------------------------------------------------------
#                             INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO
#---------------------------------------------------------------------------------------------

st.set_page_config(page_title='Home', layout="wide")

# Exibindo a barra lateral
sidebar()

# Conteúdo Principal
titles('Página Inicial')
st.divider()

subtitles('A seguir, um breve resumo das visões disponíveis neste Dashboard.')

st.write('')

# Container de Resumo com Seções e Ícones
with st.container():
    st.markdown(
        """
        ### 📊 - Visão Dados Gerais
        *Analisar dados de restaurantes permite identificar oportunidades de mercado, entender as preferências dos clientes e tomar decisões estratégicas para o seu negócio, como definir o cardápio, os preços e a localização.*

        ### 🌎 - Visão País
        *Compare restaurantes do mundo todo: encontre os países com a melhor comida, os melhores preços e os serviços mais completos, baseados em avaliações de clientes.*

        ### 🍽️ - Visão Culinária
        *Explore o mundo gastronômico e descubra os melhores restaurantes, com base em dados de milhões de avaliações, e tome decisões mais inteligentes para o seu negócio.*

        ### 🏆 - Visão Restaurantes
        *Mergulhe em um universo de dados sobre restaurantes e descubra os melhores estabelecimentos, os pratos mais populares e as tendências do mercado. Tome decisões mais assertivas para o seu negócio, com base em milhões de avaliações e análises detalhadas.*
        """, unsafe_allow_html=True
    )

# Footer customizado para dar um toque final
st.markdown("<hr style='border:2px solid #E2643B'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>💡 Insights baseados em dados para o futuro do seu negócio gastronômico!</div>", unsafe_allow_html=True)














