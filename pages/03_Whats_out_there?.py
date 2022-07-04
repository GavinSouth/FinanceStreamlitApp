import numpy as np
import pandas as pd
import altair as alt
from PIL import Image
from sqlalchemy import null
import streamlit as st 

st.markdown("# Comparing Available Electric Cars on the Market")

st.markdown("The electric car market is starting be much more fleshed out. Most manufacturer conglomerates have at least one EV offering and many are on the verge of committing to an all electric range of vehicles. That being said below is a comparison of most of the current electric cars offered in 2022. Their cost and specs range vastly, but seeing the whole picture will help making a decision much easier.")

car_data = pd.read_excel('Data/electric_car_market.xlsx')
#st.dataframe(car_data.style.highlight_max(axis=0))

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.sidebar.markdown("## EV Models")

selected_model = st.sidebar.select_slider(
    'Most to Least Expensive',
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
selection = st.sidebar.radio(
     "Choose Y Variable",
     ('Horse Power', 'Range','Fuel Economy'))

Y = null
if selection == 'Horse Power':
    Y = 'max_hp'
if selection == 'Range':
    Y = 'range_miles'
if selection == 'Fuel Economy':
    Y = 'fuel_economy'

def plot_specs(_Y):
    c = alt.Chart(car_data).encode(
        x = alt.X('msrp', scale=alt.Scale(domain=[2e4, 12e4])),
        y = alt.Y(_Y),
        tooltip=['2022_ev_model', 'msrp', 'max_hp', 'range_miles']
    ).properties(width=700, height=500)
    c = c.mark_circle(color = 'lightgrey', size = 100) 
    b = alt.Chart(selected).encode(
        x = alt.X('msrp', scale=alt.Scale(domain=[2e4, 12e4])),
        y = alt.Y(_Y),
        tooltip=['2022_ev_model', 'msrp', 'max_hp', 'range_miles']
    ).properties(width=700, height=500)
    b = b.mark_circle(color = 'red', size = 200) 
    d = c + b
    d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
    st.altair_chart(d, use_container_width=True)
plot_specs(Y)

st.dataframe(car_data.style.highlight_max(axis=0))

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("# Fuel Comparable Model")

st.markdown("## " + selected.iloc[0]['Comparable_fuel_model'])

st.image(Image.open('photos/car_photos/' + selected_model + '.jpeg'))

col1, col2, col3, col4= st.columns(4)
col1.metric("MSRP", '$' + str(selected.iloc[0]['msrp_fuel']), delta_color="off")
col2.metric("Max HP", str(selected.iloc[0]['max_hp_fuel']) + ' hp', delta_color="off")
if  selected.iloc[0]['range_miles_fuel'] > 0:
    col3.metric("Range", str(round(selected.iloc[0]['range_miles_fuel'])) + ' miles', delta_color="off")
else:
    col3.metric("Range", 'TBD', delta_color="off")
col4.metric("Fuel Type", str(selected.iloc[0]['fuel_type']), delta_color="off")