import numpy as np
import pandas as pd
import altair as alt
from PIL import Image
import streamlit as st 

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("## Comparing Available Electric Cars on the Market")

car_data = pd.read_excel('Data/electric_car_market.xlsx')
#st.dataframe(car_data.style.highlight_max(axis=0))

selected_model = st.sidebar.select_slider(
    'Most  Least Expensive',
    options=car_data['2022_ev_model'],
    help = 'This is not a complete list of all availabe vehicles, but instead represents the current EV market by showing all ranges of prices and ranges.')
selected = car_data[car_data['2022_ev_model'] == selected_model]

st.markdown("## " + selected_model)

st.image(Image.open('photos/car_photos/' + selected_model + '.jpeg'))

col1, col2, col3, col4= st.columns(4)
col1.metric("MSRP", '$' + str(selected.iloc[0]['msrp']), delta_color="off")
col2.metric("Max HP", str(selected.iloc[0]['max_hp']) + ' hp', delta_color="off")
if  selected.iloc[0]['range_miles'] > 0:
    col3.metric("Range", str(round(selected.iloc[0]['range_miles'])) + ' miles', delta_color="off")
else:
    col3.metric("Range", 'TBD', delta_color="off")
col4.metric("Type", str.upper(selected.iloc[0]['ev']), delta_color="off")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
c = alt.Chart(car_data).encode(
    x = alt.X('msrp', scale=alt.Scale(domain=[2e4, 12e4])),
    y = alt.Y('max_hp'),
    tooltip=['2022_ev_model', 'msrp', 'max_hp', 'range_miles']
).properties(width=700, height=500)
c = c.mark_circle(color = 'lightgrey', size = 100) 
b = alt.Chart(selected).encode(
    x = alt.X('msrp', scale=alt.Scale(domain=[2e4, 12e4])),
    y = alt.Y('max_hp'),
    tooltip=['2022_ev_model', 'msrp', 'max_hp', 'range_miles']
).properties(width=700, height=500)
b = b.mark_circle(color = 'red', size = 200) 
d = c + b
d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)

st.altair_chart(d, use_container_width=True)