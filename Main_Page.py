
# ———————————————————————————————————————————————————————————————————————————————————————————————— #
import pandas as pd
import numpy as np
import streamlit as st 

st.markdown("## Analysing the Current Electric Car Market")
st.sidebar.markdown("# Background")

car_data = pd.read_excel('Data/electric_car_market.xlsx')

st.dataframe(car_data.style.highlight_max(axis=0))