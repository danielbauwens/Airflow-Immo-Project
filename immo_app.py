import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Immo Eliza: Home",
    page_icon="📊",
    layout='wide'
)
data = pd.read_csv('./data/processed_data.csv',index_col='index')
st.dataframe(data)