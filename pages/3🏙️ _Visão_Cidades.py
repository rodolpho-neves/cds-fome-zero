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
    page_title="Cidades",
    page_icon="🏙️",
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


st.header('Visão Cidades')

with st.container():
    st.markdown('### Restaurantes cadastradas por cidade')
    #st.text('Gráfico de barra restaurantes x países')
    
    df_aux = df.loc[:,['restaurant_id','city']]
    df_aux = (df_aux.groupby(['city'])
                .agg({'restaurant_id': 'count'})
                #.sort_values(by=['restaurant_id'],ascending=False)
                .reset_index()
                )
    #st.dataframe(df_aux)
    df_paises = df.loc[:,['city','country_code']].groupby('city').first().reset_index()
    #st.dataframe(df_paises)
    df_aux = (df_aux.join(df_paises.set_index('city'), on='city')
                .sort_values(by='restaurant_id',ascending=False)).reset_index()
    #df.join(other.set_index('key'), on='key')
    
    #st.dataframe(df_aux)

    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='city', 
                y='restaurant_id',
                color="country_code",
                category_orders={'city': df_aux['city'],
                                 'country_code': df_aux['country_code']},
                labels={
                    "city": "Cidade",
                    "country_code": "Países",
                    "restaurant_id": "Restaurantes cadastrados"
                 })
    
    st.plotly_chart(fig, use_container_width=True)
    
    
with st.container():
    st.markdown('### Nota média dos restaurantes por país')
    df_aux = (df[['country_code','aggregate_rating']]
                        .groupby('country_code')
                        .mean()
                        .sort_values(by='aggregate_rating',ascending=False)
                        .reset_index())
    fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='country_code', 
                y='aggregate_rating',
                category_orders={'country_code': df_aux['country_code']},
                labels={
                     "country_code": "Países",
                     "aggregate_rating": "Média dos restaurantes"})
    
    st.plotly_chart(fig, use_container_width=True)


with st.container():

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Restaurantes com nota maior que 4')
        df_aux = df.loc[(df['aggregate_rating'] > 4),['restaurant_id','city']]
        df_aux = (df_aux.groupby('city')
                  .count()
                  .sort_values(by='restaurant_id',ascending=False).reset_index())
        df_aux = (df_aux.join(df_paises.set_index('city'), on='city')
                .sort_values(by='restaurant_id',ascending=False).reset_index())
    

        fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='city', 
                y='restaurant_id',
                color='country_code',
                #barmode="relative",
                category_orders={'city': df_aux['city'],
                                 'country_code': df_aux['country_code']},
                labels={
                        "restaurant_id": "Restaurantes",
                        "city": "Cidade",
                        'country_code': 'Países'},
                #range_y=[0,5]
                )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('#### Restaurantes com nota menor que 2.5')
        df_aux = df.loc[(df['aggregate_rating'] <= 2.5),['restaurant_id','city']]
        df_aux = (df_aux.groupby('city')
                  .count()
                  .sort_values(by='restaurant_id',ascending=False).reset_index())
        df_paises = df.loc[:,['city','country_code']].groupby('city').first().reset_index()
        df_aux = (df_aux.join(df_paises.set_index('city'), on='city')
                .sort_values(by='restaurant_id',ascending=False).reset_index())
    

        fig = px.bar(df_aux.loc[0:filtro_itens,:], 
                x='city', 
                y='restaurant_id',
                color='country_code',
                category_orders={'city': df_aux['city'],
                                 'country_code': df_aux['country_code']},
                labels={
                        "restaurant_id": "Restaurantes",
                        "city": "Cidade",
                        'country_code': 'Países'},
                #range_y=[0,5]
                )
        
        fig.update_layout(yaxis_categoryorder = 'total descending')


        st.plotly_chart(fig, use_container_width=True)


    
with st.container():
    st.markdown('### Tipos de culinária por cidade')
    df_aux = (df[['city','cuisines']]
                        .groupby('city')
                        .nunique()
                        .sort_values(by='cuisines',ascending=False)
                        .reset_index())
    df_aux = (df_aux.join(df_paises.set_index('city'), on='city')
                .sort_values(by='cuisines',ascending=False).reset_index())
    
    

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
    fig.update_layout(yaxis_categoryorder = 'total descending')

    st.plotly_chart(fig, use_container_width=True)