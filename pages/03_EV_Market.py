import numpy as np
import pandas as pd
import altair as alt
from PIL import Image
from sqlalchemy import null
import streamlit as st 

st.markdown("# Comparing Available Electric Cars")

st.markdown("The electric car market in 2022 is much more fleshed out than previous years. Most manufacturer conglomerates have at least one EV offering and many are on the verge of committing to an all electric range of vehicles. That being said below is a comparison of most of the current electric cars offered in 2022. Their cost and specs range vastly, but seeing the whole picture will help making a decision much easier.")

car_data = pd.read_excel('Data/electric_car_market.xlsx')
#st.dataframe(car_data.style.highlight_max(axis=0))

class fuel_stats: 
    avg_annual_miles = 14263
    avg_length_of_ownership = 8.4
    current_electric = 0.154
    current_diesel = 5.718
    current_regular = 5.006
    current_mid = 5.455
    current_premium = 5.762

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

st.markdown("The selected car from the slider is showing red on this chart to show a quick difference in specs to the other EVs on the market. To change the Y-axis variable use the radio button on the sidebar.")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
selection = st.sidebar.radio(
     "Choose Y Variable",
     ('Horse Power', 'Range','Fuel Economy'))

Y = null
if selection == 'Horse Power':
    Y = 'max_hp'
    Y2 = 'max_hp_fuel'
if selection == 'Range':
    Y = 'range_miles'
    Y2 = 'range_miles_fuel'
if selection == 'Fuel Economy':
    Y = 'fuel_economy'
    Y2 = 'fuel_economy_fuel'

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

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("# Fuel Comparable Model")
st.markdown("To compare apples to apples as best as possible it seems like a useful comparison to look at vehicles that **cost the same as an electric model**. Seeing this comparison may make an even stronger case for the possible fuel savings over time. But, as you may see, this isn't the entire story. Some of the electric cars may have a lot less power and range compared to their gasoline cost equivilents. These trade-offs are variables to consider if you plan on going with an EV.")

st.markdown("## " + selected.iloc[0]['Comparable_fuel_model'])
st.image(Image.open('photos/car_photos/' + selected.iloc[0]['Comparable_fuel_model'] + '.jpeg'))

col1, col2, col3, col4= st.columns(4)
col1.metric("MSRP",
            '$' + str(selected.iloc[0]['msrp_fuel']),
            'Equally Priced',
            delta_color="off")
col2.metric("Max HP", 
            str(selected.iloc[0]['max_hp_fuel']) + ' hp', 
            str(selected.iloc[0]['max_hp_fuel'] - selected.iloc[0]['max_hp']) + ' hp', 
            delta_color="normal")
if selected.iloc[0]['range_miles_fuel'] > 0 and selected.iloc[0]['range_miles'] > 0:
    col3.metric("Range", 
                str(round(selected.iloc[0]['range_miles_fuel'])) + ' miles',
                str(round(selected.iloc[0]['range_miles_fuel']) - round(selected.iloc[0]['range_miles'])) + ' miles', 
                delta_color="normal")
else:
    col3.metric("Range", 'TBD', delta_color="off")
col4.metric("Fuel Type", str(selected.iloc[0]['fuel_type']), delta_color="off")

st.markdown("You notice that some of the differences between the specs on the EV model and the fuel model reflect in color coding. This is an interesting distinction that will help you see the difference at a glimpse.")
st.markdown("")

def plot_specs(_Y2):
    c = alt.Chart(car_data).encode(
        x = alt.X('msrp_fuel', scale=alt.Scale(domain=[2e4, 12e4])),
        y = alt.Y(_Y2),
        tooltip=['Comparable_fuel_model', 'msrp_fuel', 'max_hp_fuel', 'range_miles_fuel']
    ).properties(width=700, height=500)
    c = c.mark_circle(color = 'lightgrey', size = 100) 
    b = alt.Chart(selected).encode(
        x = alt.X('msrp_fuel', scale=alt.Scale(domain=[2e4, 12e4])),
        y = alt.Y(_Y2),
        tooltip=['Comparable_fuel_model', 'msrp_fuel', 'max_hp_fuel', 'range_miles_fuel']
    ).properties(width=700, height=500)
    b = b.mark_circle(color = 'red', size = 200) 
    d = c + b
    d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
    st.altair_chart(d, use_container_width=True)
plot_specs(Y2)

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("# Anticipated cost comparison:")
st.markdown("#### Electric Powered: " + selected_model)
col1, col2, col3 = st.columns(3)
col1.metric('EV MSRP', 
           '$' + (selected.iloc[0]['msrp']).astype(str),
           delta_color="off")
col2.metric("Lifetime Electricity Cost",
            "$" +
            round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric, 2).astype(str),
            delta_color="off")
col3.metric("Total Cost of Ownership", 
            "$" + 
            round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric + (selected.iloc[0]['msrp']), 2).astype(str),
            delta_color="off")

st.markdown("#### Gas Powered: " + selected.iloc[0]['Comparable_fuel_model'])
col1, col2, col3 = st.columns(3)
col1.metric('Fuel MSRP', 
           '$' + (selected.iloc[0]['msrp_fuel']).astype(str),
           delta_color="off")
col2.metric("Lifetime Fuel Cost",
            "$" +
            round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership, 2).astype(str),
            delta_color="off")
col3.metric("Total Cost of Ownership", 
            "$" + round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership +(selected.iloc[0]['msrp_fuel']), 2).astype(str),
            '$' + round(round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership + (selected.iloc[0]['msrp_fuel']), 2) - round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric + (selected.iloc[0]['msrp']), 2), 2).astype(str),
            delta_color='off')

st.markdown("Comparing both of these vehicles side by side and looking at an estimated overall cost, the estimated savings of the **" + 
            selected_model + 
            '** over the **' + 
            selected.iloc[0]['Comparable_fuel_model'] + 
            '** is:')

st.markdown("### $" + round(round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership + (selected.iloc[0]['msrp_fuel']), 2) - round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric + (selected.iloc[0]['msrp']), 2), 2).astype(str))

st.markdown("")
st.markdown("Out of all the electric vehicles on the market right now, there are still some that are more efficent than others. The **" + selected_model + "** falls here compared to the rest of the EVs. Note: The higher the kWh/100 mile rating the less efficient it is. That being said if your goal is to save the most money possible and use less resources, consider some of the ones on the right side of the chart. ")
st.markdown("")

c = alt.Chart(car_data).mark_point(filled=True, size=100, color = 'lightgrey').encode(
    x = alt.X('kWh', scale=alt.Scale(reverse=True)),
    tooltip=['2022_ev_model', 'kWh', 'msrp', 'range_miles']
    ).properties(width=700, height=100)
b = alt.Chart(selected).mark_point(filled=True, size=200, color = 'red').encode(
    x = alt.X('kWh', scale=alt.Scale(reverse=True)),
    tooltip=['2022_ev_model', 'kWh', 'msrp', 'range_miles']
    ).properties(width=700, height=100)
d = c + b
d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
st.altair_chart(d, use_container_width=True)

st.markdown("**Note:** Some manufacturers have better tech than others in this space. Tesla, for example, has been improving and polishing it's evs for years and as such many of there models are more efficient, powerful, and reasonably priced. Another car company that has made some impressive strides is General Motors with their Ultium battery system. It's so modular and solid that other companies, like Honda Mtrs. is joining GM to build their electric vehicles on their platform. Be aware of these differences as you prepare to grab a new ev, they can make a large difference in the long run.")