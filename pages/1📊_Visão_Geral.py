import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium 


from utils import *

# importing and cleaning data
df_raw = pd.read_csv('./dataset/zomato.csv')
df = clean_df(df_raw)

logo = Image.open('./avaliacao.png')
#print("All fine!")

### ================================================ ###
### Dashboard Streamlit 
### ================================================ ###

st.set_page_config(
    page_title="Geral",
    page_icon="📊",
    layout="wide",
)

### ------------------------------------------------ ###
### Sidebar
### ------------------------------------------------ ###

sidebar_padrao(logo)
#df, filtro_itens = filtros_pages(df)
rodape_padrao()

### ------------------------------------------------ ###
### Corpo principal
### ------------------------------------------------ ###


st.markdown('### Visão Geral')
st.markdown('#### Números de cadastros')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        #st.markdown('##### ')
        #st.text('Número de países')
        col1.metric('Países',df['country_code'].nunique())
    
    with col2:
        #st.markdown('##### ')
        #st.text('Número de cidades')
        col2.metric('Cidades',df['city'].nunique())
    
    with col3:
        #st.markdown('##### ')
        #st.text('Número de restaurantes')
        col3.metric('Restaurantes',df['restaurant_name'].nunique())
    
    with col4:
        #st.markdown('##### ')
        #st.text('Número de culinárias')
        col4.metric('Culinárias',df['cuisines'].nunique())

    with col5:
        #st.markdown('##### ')
        #st.text('Número de culinárias')
        col5.metric('Votos totais',df['votes'].sum())

 
with st.container(): 
    st.markdown('#### Mapa com restaurantes cadastrados')
    map_order(df) 
