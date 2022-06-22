# ———————————————————————————————————————————————————————————————————————————————————————————————— #
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import streamlit as st 

st.markdown("## There is definately a huge contrast in cost...")
st.markdown("Now you walk across the street to talk to your neighbor that has that new shiny electric car to ask her a couple of questions. You knock on the door and no one answers, as you walk down their entryway their garage door opens and you catch her unplugging their car from the wall. You are obviously impressed and jealous of the ease of recharging the car. You belt out, 'wow, nice car! Must be rough on the electric bill though.' They respond, 'yeah thanks! It's really fun to own, surprisingly its not that expensive to keep around.' Now your really curious. 'How much does it actually cost to charge then? I'm considering getting one myself', you reply. They smile and begin to explain the breakdown...")

image = Image.open('photos/electric_station.png')
st.image(image)

electricity_cost = pd.read_excel('Data/electric_cost_overtime.xls')
#st.dataframe(electricity_cost.style.highlight_max(axis=0))

image = Image.open('photos/current_kwh.png')
st.image(image)

# Graph for gas changes over time.    
a = alt.Chart(electricity_cost).encode(
    x = alt.X('Date', axis=alt.Axis(tickCount=10)),
    y = alt.Y('Cost US Cents', axis=alt.Axis(tickCount=10)),
    tooltip=['Date', 'Cost US Cents']
).properties(width=700, height=400)
a = a.mark_line(color = 'lightgreen') 
a = a.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
st.altair_chart(a, use_container_width=True)

