# ———————————————————————————————————————————————————————————————————————————————————————————————— #
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import streamlit as st 
from sklearn.linear_model import LinearRegression

st.markdown("## Thats a stark contrast...")
st.markdown("### So now,")
st.markdown(" you walk across the street to talk to your neighbor that has that new shiny electric car to ask her a couple of questions. You knock on the door and no one answers, as you walk down their entryway their garage door opens and you catch her unplugging their car from the wall. You are obviously impressed and jealous of the ease of recharging her car. You belt out, 'wow, nice car! Must be rough on your electric bill though.' They respond, 'yeah thanks! It's really fun to own, surprisingly its not that expensive to keep around.' Now your really curious. 'How much does it actually cost to charge then? I'm considering getting one myself', you reply. She smiles and begin to explain the breakdown...")

image = Image.open('photos/electric_station.png')
st.image(image)

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("### She explains,")

st.markdown(" > First of all, the cost of charging an electric car is variable. Gas prices are posted and change day to day, and outside the average variance there is little variation. Not so much the case with the cost of electricity. The cost of electricity will change depending on when and where you decide to charge it.  **That being said the cheapest way to charge an electric car is to install a home charging station and charge through the middle of night when power cost is the lowest.**")

st.markdown(" > The next thing you need to understand is the metric used to calculate the cost of opperating an electric vehicle in regards to economy. When shopping for or considering a gasoline-powered car you will analyze the MPG it gets as the metric for overall cost of the car. You mention that you found the that metric and cost for your own can and understand the conversion and cost. The metric used for electric cars in the same way is actually kilowatt-hours per 100 miles which is posted on all new electric cars right on their specifications. So, **to figure out your cost of charging at home, multiply your vehicle's kWh/100 miles figure by the electricity rate — the cost per kWh — for the time of day you'll most often be charging (more about that in a minute). That figure will tell you the cost per 100 miles.**")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("##### For brevity lets hypothetically consider some kWh averages...")

electricity_cost = pd.read_excel('Data/electric_cost_overtime.xls')
electricity_cost.reset_index(inplace=True)

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

# Linear regression model for electric prices
x = electricity_cost['index'].values.reshape(-1, 1)
y = electricity_cost['Cost US Cents'].values
model = LinearRegression().fit(x, y)

# model.intercept_
# model.coef_
#model.intercept_ + model.coef_ * 365

st.markdown(" Considering the values from your charts, running a linear regression doesn't seems like a logical approach to predicting future costs of both gasoline and electricity. You find the following models:")

st.markdown("**Average electric cost change with time series regression model:**")
st.markdown("###### $ \hat{Y}_i \ \\text{(Estimated kWh Cost)}\ = " 
            + str(round(model.intercept_, 2))  + 
            "\\text{¢} + " 
            + str({round(model.coef_[0], 6)}) + 
            "\\text{¢}\ X_i \ \\text{(Months)}$")

for i in range(1,50):
    if model.intercept_ + model.coef_ * (12 * i) > (model.intercept_  * 2):
        st.markdown("###### On average the cost of electricity doubles every " + str(i) + " years")
        break
    
# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("### Crunching the numbers,")

st.markdown("So, for example, my electric SUV gets 32 kWh/100 miles and has a range of 348 miles. Lest say we charge it at the current rate of cost for kWh of 15¢.")

image = Image.open('photos/tesla_modelx.png')
st.image(image)

image = Image.open('photos/neighbor_car_specs.png')
st.image(image)

col1, col2, col3, col4= st.columns(4)
col1.metric("Vehicle Type", "SUV", delta_color="off")
col2.metric("Fuel Type", "Electricity", delta_color="off")
col3.metric("Fuel Economy", "32 kWh", delta_color="off")
col4.metric("Annual Cost for Power", "$707", delta_color="off")


image = Image.open('photos/lifetime_electric.png')
st.image(image)