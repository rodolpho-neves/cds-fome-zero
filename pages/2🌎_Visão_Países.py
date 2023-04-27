import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


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
    page_title="Países",
    page_icon="🌎",
    layout="wide",
)

### ------------------------------------------------ ###
### Sidebar
### ------------------------------------------------ ###

sidebar_padrao(logo)
df, filtro_itens = filtros_pages(df)
rodape_padrao()

### ------------------------------------------------ ###
### Corpo principal
### ------------------------------------------------ ###


st.header('Visão Países')

with st.container():
    st.markdown('### Restaurantes cadastradas por país')
    #st.text('Gráfico de barra restaurantes x países')

    # Grafico de restaurantes por países
    df_aux = df.loc[:,['country_code', 'restaurant_name']].groupby('country_code').nunique()
    df_aux = df_aux.sort_values(by='restaurant_name',ascending=False).reset_index()
    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='country_code', 
                y='restaurant_name',
                labels={
                     "country_code": "Países",
                     "restaurant_name": "Restaurantes cadastrados"
                 })
    
    st.plotly_chart(fig, use_container_width=True)
    

with st.container():
    st.markdown('### Cidades cadastradas por país')
    #st.text('Gráfico de barra cidades x países')
    
    # Grafico de cidades por países
    df_aux = df.loc[:,['city', 'country_code']].groupby('country_code').nunique()
    df_aux = df_aux.sort_values(by='city',ascending=False).reset_index()
    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='country_code', 
                y='city',
                labels={
                     "country_code": "Países",
                     "city": "Cidades cadastradas"
                 })
    
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Nota média dos restaurantes por país')
        df_aux = (df[['country_code','aggregate_rating']]
                            .groupby('country_code')
                            .mean()
                            .sort_values(by='aggregate_rating',ascending=False)
                            .reset_index())
        fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                    x='country_code', 
                    y='aggregate_rating',
                    labels={
                            "country_code": "Países",
                            "aggregate_rating": "Média dos restaurantes"})

        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('#### Votos médio de restaurante por país!')
        #st.text('Gráfico de barra: Melhores médias por país')
        df_aux = df.loc[:,['restaurant_name','country_code', 'votes']]
        df_aux = df_aux.groupby('country_code').mean().sort_values(by=['votes'],ascending=False).reset_index()

        fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='country_code', 
                y='votes',
                #color='country_code',
                labels={
                #        "restaurant_name": "Restaurantes",
                        "votes": "Média de votos",
                        'country_code': 'Países'},
                #range_y=[0,5]
                )

        st.plotly_chart(fig, use_container_width=True)


with st.container():
    st.markdown("#### Tipos de culinária por país")
    df_aux = (df.loc[:,['country_code', 'cuisines']].groupby('country_code')
                                                .nunique()
                                                .sort_values(by='cuisines',ascending=False)
                                                .reset_index())
    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='country_code', 
                y='cuisines',
                #color='country_code',
                labels={
                #        "restaurant_name": "Restaurantes",
                        "cuisines": "Tipos de culinária",
                        'country_code': 'Países'},
                #range_y=[0,5]
                )

    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown("#### Preço do prato para dois (USD) por país")
    df_aux = (df[['country_code', 'average_cost_for_two(usd)']].groupby(['country_code'])
                                                .mean()
                                                .sort_values(by='average_cost_for_two(usd)',ascending=False)
                                                .reset_index()
                                                )
    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='country_code', 
                y='average_cost_for_two(usd)',
                #color='country_code',
                labels={
                #        "restaurant_name": "Restaurantes",
                        "average_cost_for_two(usd)": "Preço do prato para dois (USD)",
                        'country_code': 'Países'},
                #range_y=[0,5]
                )

    st.plotly_chart(fig, use_container_width=True)