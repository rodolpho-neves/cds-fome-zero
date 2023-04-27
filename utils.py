# Arquivo de utilidades para funcionamento do dashboard Fome Zero

import pandas as pd
import numpy as np
import inflection
import folium 
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import streamlit as st


# funcoes para conversao de valores do banco de dados

# transformar os codigos dos paises em nomes
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

# transformar os codigos de precos em categorias 
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


# transformar os codigos de cores em nomes das cores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]


# renomear as colunas para nomes em minusculo, sem
def rename_columns(dataframe):
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


# currency conversion
current_conversion_to_usd = {   'Philippines' : 0.076, 
                                'Brazil': 0.2, 
                                'Australia': 0.67, 
                                'United States of America':1,
                                'Canada': 0.74, 
                                'Singapure': 0.75, 
                                'United Arab Emirates':0.27, 
                                'India': 0.012,
                                'Indonesia': 0.000067, 
                                'New Zeland': 0.61, 
                                'England':1.24, 
                                'Qatar': 0.27, 
                                'South Africa': 0.055,
                                'Sri Lanka': 0.0031,
                                'Turkey': 0.052 }

def currency_conversion(x):
    return x['average_cost_for_two'] * current_conversion_to_usd[x['country_code']]

def clean_df(df_raw):
    df = rename_columns(df_raw)
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: str(x).split(",")[0])
    df['rating_color'] = df.loc[:,'rating_color'].apply(lambda x: color_name(x))
    df['country_code'] = df.loc[:,'country_code'].apply(lambda x: country_name(x))
    df['price_range'] = df.loc[:,'price_range'].apply(lambda x: create_price_type(x))
    df['average_cost_for_two(usd)'] = df.apply(lambda x: currency_conversion(x), axis=1)

    # modificacao por causa das definicoes do problema
    ## retirada dos valores duplicados de restaurantes
    df = df.drop_duplicates(subset=['restaurant_name','address'])
    ## retirada de um valor com preco medio outlier
    df = df.drop(385)
    
    # retirando os valores 'nan' de cuisines
    df = df.drop(df.loc[(df['cuisines'] == 'nan'),:].index)

    return df


# funcoes para facilitar a exploracao dos dados
def melhor_restaurante_da_culinaria(df, cozinha):
    """
    Encontrar o melhor restaurante de determinada culinaria
    """
    df_aux = df.loc[df.loc[:,'cuisines']==cozinha,['restaurant_name','aggregate_rating','votes']].sort_values(by=['aggregate_rating','votes'])
    return df_aux.iloc[-1]['restaurant_name']


def pior_restaurante_da_culinaria(df, cozinha):
    """
    Encontrar o pior restaurante de determinada culinaria.
    """
    df_aux = df.loc[df.loc[:,'cuisines']==cozinha,['restaurant_name','aggregate_rating','votes']].sort_values(by=['aggregate_rating','votes'])
    return df_aux.iloc[0]['restaurant_name']


def price_rate(x):
        if x == "cheap":
            return '$'
        elif x == "normal":
            return '$$'
        elif x == "expensive":
            return '$$$'
        else:
            return '$$$$'
    

# Mapa com os restaurantes
def map_order(df):
    df_aux = df
    map = folium.Map(location=[df_aux['latitude'].mean(), df_aux['longitude'].mean()],zoom_start=1,zoom_control=False) #, width=1400, height=500
    
    marker_cluster = MarkerCluster().add_to(map)
    
    for _, location_info in df_aux.loc[0:1000,:].iterrows():
        folium.Marker([location_info['latitude'], location_info['longitude']], 
                        popup=folium.Popup(f"{location_info['restaurant_name']}\n Nota: {location_info['aggregate_rating']}/5\n Preço: {price_rate(location_info['price_range'])}", 
                                           max_width=50),
                        icon=folium.Icon(color=location_info['rating_color'],prefix='fa',icon='fa-utensils'),
                        overlay=True).add_to(marker_cluster)
        

    folium_static(map, width=800, height=400)


def sidebar_padrao(logo):
    #logo = Image.open('./avaliacao.png')
    st.sidebar.image(logo,width=120)
    st.sidebar.markdown('# FomeZero!') 
    st.sidebar.markdown('###### Sua refeição em um clique!') 
    st.sidebar.markdown("""---""") 

def filtros_pages(df):
    itens_slider = st.sidebar.slider(
        'Quandos itens a mostra:',
        value = 10,
        min_value = 1,
        max_value = 20)
    itens_slider -= 1

    st.sidebar.markdown("""---""") 

    filtro_paises = st.sidebar.multiselect(
        'Países que serão exibidos:',
        df['country_code'].unique(),
        default=df['country_code'].unique())

    df = df.loc[df['country_code'].isin(filtro_paises), :]
    
    return df, itens_slider

def rodape_padrao():
    st.sidebar.markdown('###### Powered by Comunidade DS') 
    st.sidebar.markdown("""---""") 

"""
['restaurant_id', 'restaurant_name', 'country_code', 'city', 'address',
       'locality', 'locality_verbose', 'longitude', 'latitude', 'cuisines',
       'average_cost_for_two', 'currency', 'has_table_booking',
       'has_online_delivery', 'is_delivering_now', 'switch_to_order_menu',
       'price_range', 'aggregate_rating', 'rating_color', 'rating_text',
       'votes', 'average_cost_for_two(usd)']

"""    