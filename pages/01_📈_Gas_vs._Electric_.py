
# ———————————————————————————————————————————————————————————————————————————————————————————————— #
import pandas as pd
import numpy as np
import streamlit as st 

st.markdown("## Comparing Gasoline/Diesel to Electric Vehicles")
st.sidebar.markdown("# Gas vs. Electric")

car_data = pd.read_excel('Data/electric_car_market.xlsx')

st.dataframe(car_data.style.highlight_max(axis=0))