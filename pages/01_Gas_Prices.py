# ———————————————————————————————————————————————————————————————————————————————————————————————— #
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import streamlit as st 

st.markdown("# Paying this much for gas is crazy...")
st.sidebar.markdown("# At the pump")

gas_prices = pd.read_excel('Data/10641_gasoline_prices_by_year_2-22-22.xlsx')

#st.dataframe(gas_prices.style.highlight_max(axis=0))

st.markdown("## Right now,")
st.markdown(" you are currently standing at a gas pump. Card swiped, nozzle in hand, and wincing as you select the grade of fuel for your gas. How frustrated and confused are you seeing the prices? You may think this is out of control, gas was 25¢ chaper like three days ago!")

image = Image.open('photos/gas_pump_slim.png')
st.image(image, caption='')
            
image = Image.open('photos/gas_prices_06_09.png')
st.image(image, caption='Gas prices as of June 9, 2022 https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm')

st.markdown("**Wow! Thank goodness** you don't own a large 1-ton diesel truck, that's absolutely **outrageous**! But, you still have to fuel up your ride. After a minute or two your tank is full and you have a large difference in your bank account. You storm away frustrated and sad you can't justify a late night pizza and movie night.") 
st.markdown("You consider, on the way home you think about how you can start saving money at the pump... want to start riding your bike everywhere? No thanks. You start thinking about your neigbors shiny new electric vehicle they keep raving about to you and all your neighbors. You've been thinking about an upgrade for a while now, maybe this is a good time to see whats out there whats available.")
st.markdown("")

st.markdown("## Later that day,")

st.markdown("You sit down on your laptop and search for gas prices in America, you want to see if things are really as bad as you think or if your local gas station is just a bad case of gutting locals. You find...")

image = Image.open('photos/gas_increase.png')
st.image(image, caption='')
        
# Graph for gas changes over time.    
c = alt.Chart(gas_prices).mark_line().encode(
     x='Year', y='Gasoline Price (2020 $/gallon)', tooltip=['Year', 'Gasoline Price (2020 $/gallon)'])
c = alt.Chart(gas_prices).encode(
    x = alt.X('Year', axis=None),
    y = alt.Y('Gasoline Price (2020 $/gallon)'),
    tooltip=['Year', 'Gasoline Price (2020 $/gallon)']
).properties(width=700, height=500)
c = c.mark_line(color = 'red') 
b = alt.Chart(gas_prices).encode(
    x = alt.X('Year', axis=None),
    y = alt.Y('Gasoline Price ($/gallon)'),
    tooltip=['Year', 'Gasoline Price ($/gallon)']
).properties(width=700, height=500)
b = b.mark_line(color = 'lightgrey')
d = b + c 
d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)

st.altair_chart(d, use_container_width=True)

st.markdown("And that's not all, you find some of the main economists in the US predicting this price to grow to **$7.00 a gallon by end of year!**")
st.markdown("")

