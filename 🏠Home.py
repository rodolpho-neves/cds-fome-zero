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


# 📚⚙️⚛️💅🌏🛢🍪🤐🦀🧪🐞⚠️🚨🚀🔨💡🗑👷‍♂️🔒🏞🎞🔈📂📦

st.set_page_config(
    page_title="Home",
    page_icon="🚨",
    layout="centered"
)

### ------------------------------------------------ ###
### Sidebar
### ------------------------------------------------ ###

st.sidebar.image(logo,width=120)
st.sidebar.markdown('# FomeZero!') 
st.sidebar.markdown('###### Sua refeição em um clique!') 
st.sidebar.markdown("""---""") 

st.sidebar.markdown('###### Powered by Comunidade DS') 
st.sidebar.markdown("""---""") 

### ------------------------------------------------ ###
### Corpo principal
### ------------------------------------------------ ###


st.markdown("# FomeZero Growth Dashboard")
st.markdown(
    """
    This dashboard was developed for keep tracking the overall growth metrics for a restaurant grading app.
    ### How to use this dashboard?
    - Overall view:
        - Check all the global numbers of the FomeZero App.
    - Country view:
        - Track the numbers by country and compare among them.
    - Restaurant view: 
        - View metrics of restaurants and some comparisons.
    - Cuisines view:
        - View comparisons of cuisines, prices and ratings.
    
    ### Ask for help:
    - Data Science Team on Discord
        - @rodolpho.neves
    """
    )