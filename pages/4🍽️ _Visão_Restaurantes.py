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
    page_title="Restaurantes",
    page_icon="🍽️",
    layout="centered",
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


st.header('Visão Restaurantes')


with st.container():
    st.markdown('### Preço médio (USD) por tipo culinário em cada país')
    #st.text('Gráfico de barra restaurantes x países')
    
    
    df_aux = (df.loc[:,['city','cuisines','average_cost_for_two(usd)']].groupby('cuisines')
              .agg({'city': 'first',
                    'average_cost_for_two(usd)': 'mean'})
              .sort_values(by=['average_cost_for_two(usd)'], ascending=False)
              .reset_index())
    df_paises = df.loc[:,['city','country_code']].groupby('city').first().reset_index()
    
    df_aux = (df_aux.join(df_paises.set_index('city'), on='city')
                .sort_values(by='average_cost_for_two(usd)',ascending=False))
    #st.dataframe(df_aux)
    df_aux.reset_index()
    #st.dataframe(df_aux)

    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='cuisines', 
                y='average_cost_for_two(usd)',
                color="country_code",
                category_orders={'cuisines': df_aux['cuisines'],
                                 'country_code': df_aux['country_code']},
                labels={
                    "city": "Cidade",
                    "country_code": "Países",
                    "cuisines" : "Tipo de culinária",
                    "average_cost_for_two(usd)": "Custo médio para duas pessoas (USD)"
                 })
    
    st.plotly_chart(fig, use_container_width=True)
    
    
with st.container():
    st.markdown(f'### Top {filtro_itens+1} restaurantes e suas culinárias')
    df_aux = (df[['restaurant_name','cuisines','city','country_code','aggregate_rating','average_cost_for_two(usd)','votes']]
                        .sort_values(by=['aggregate_rating','votes'],ascending=False)
                        .reset_index())
    df_aux = df_aux.loc[0:filtro_itens].set_index('restaurant_name')
    st.dataframe(df_aux.loc[:,['cuisines','city','country_code','aggregate_rating','average_cost_for_two(usd)','votes']], use_container_width=True)


with st.container():

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Maiores notas médias por tipo de culinária')
        df_aux = df.loc[:,['aggregate_rating','cuisines','city']]
        df_aux = (df_aux.groupby(['cuisines'])
                  .agg({'aggregate_rating': 'mean',
                        'city': 'first'})
                  .sort_values(by='aggregate_rating',ascending=False).reset_index())
    
        df_aux = (df_aux.join(df_paises.set_index('city'), on='city')
                .sort_values(by='aggregate_rating',ascending=False))
    
        fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='cuisines', 
                y='aggregate_rating',
                color='country_code',
                #barmode="relative",
                category_orders={'cuisines': df_aux['cuisines']},
                labels={
                        "aggregate_rating": "Notas médias",
                        "cuisines": "Tipo de culinária",
                        'country_code': 'Países'}
                )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('#### Menores notas médias por tipo de culinária')
        df_aux = df.loc[:,['aggregate_rating','cuisines','city']]
        df_aux = (df_aux.groupby(['cuisines'])
                  .agg({'aggregate_rating': 'mean',
                        'city': 'first'})
                  .sort_values(by='aggregate_rating',ascending=True).reset_index())
    
        df_aux = (df_aux.join(df_paises.set_index('city'), on='city')
                .sort_values(by='aggregate_rating',ascending=True))
    
        fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='cuisines', 
                y='aggregate_rating',
                color='country_code',
                #barmode="relative",
                category_orders={'cuisines': df_aux['cuisines']},
                labels={
                        "aggregate_rating": "Notas médias",
                        "cuisines": "Tipo de culinária",
                        'country_code': 'Países'}
                )

        st.plotly_chart(fig, use_container_width=True)


    
with st.container():
    st.markdown('### Tipos de culinária por cidade')
    df_aux = (df[['city','cuisines','country_code']]
                        .groupby('city')
                        .agg({'country_code': 'first',
                        'cuisines': 'nunique'})
                        .sort_values(by='cuisines',ascending=False)
                        .reset_index())
    
    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
            x='city', 
            y='cuisines',
            color='country_code',
            category_orders={'city': df_aux['city']},
            labels={
                    "cuisines": "Tipos de culinárias",
                    "city": "Cidade",
                    'country_code': 'Países'},
            )

    st.plotly_chart(fig, use_container_width=True)