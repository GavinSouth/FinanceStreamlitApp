# ———————————————————————————————————————————————————————————————————————————————————————————————— #
import base64
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import streamlit as st 
from sklearn.linear_model import LinearRegression

st.markdown("# Paying this much for gas is crazy...")

gas_prices = pd.read_excel('Data/10641_gasoline_prices_by_year_2-22-22.xlsx')
gas_prices.reset_index(inplace=True)
#st.data_frame(gas_prices.style.highlight_max(axis=0))

class fuel_stats: 
    avg_annual_miles = 14263
    avg_length_of_ownership = 8.4
    current_diesel = 5.718
    current_regular = 5.006
    current_mid = 5.455
    current_premium = 5.762

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("## Right now,")
st.markdown(" you're currently standing at a gas pump; card swiped, nozzle in hand, you wince as you select the grade of fuel for your car. How frustrated and confused are you seeing the cost of gas right now? You must think this is out of control as gas was 25¢ cheaper like three days ago! It's especially frustrating because you know you have no control over the situation.")

image = Image.open('photos/gas_pump_slim.png')
st.image(image, caption='Gas prices as of June 18, 2022 https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm')

col1, col2, col3, col4= st.columns(4)
col1.metric("Diesel", "$" + str(fuel_stats.current_diesel), str(int((fuel_stats.current_diesel / 3.287) * 100)) + '% since 2021', delta_color="off")
col2.metric("Regular", "$" + str(fuel_stats.current_regular), str(int((fuel_stats.current_regular / 3.008) * 100)) + '% since 2021', delta_color="off")
col3.metric("Mid-grade", "$" + str(fuel_stats.current_mid), str(int((fuel_stats.current_mid / 3.432) * 100)) + '% since 2021', delta_color="off")
col4.metric("Premium", "$" + str(fuel_stats.current_premium), str(int((fuel_stats.current_premium / 3.687) * 100)) + '% since 2021', delta_color="off")

st.markdown("These are the current diesel and gas prices right now. You may start to feel bad for anyone driving a one-ton diesel truck! But, you still have to deal with this burden of an out of control rise in cost, you don't have a choice as you need to commute to work and to your other responsibilities.") 
st.markdown("But, maybe there is something you can do about this unfortunate dilemma. You consider, on the way home from the station some different ways you could start saving money at the pump... You think: Maybe, I could start riding my bike everywhere! No thanks. Maybe, carpooling with the neighbor! But, that sounds like a logistical nightmare. But then, you start thinking about your neighbors shiny new electric vehicle they keep raving about. That must be much cheaper! Besides, you've been thinking about an upgrade for a while now, maybe this is a good time to see whats available out there and seriously consider getting one.")
st.markdown("")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("## Later that day,")
st.markdown("You sit down on your laptop and start researching gas prices in America, you want to see if things are really as bad as you think or if your local gas station is just a bad case of gutting locals. You find...")

image = Image.open('photos/gas_increase.png')
st.image(image, caption='')
        
# Graph for gas changes over time.    
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

# Linear regression model for gas prices
x = gas_prices['index'].values.reshape(-1, 1)
y = gas_prices['Gasoline Price ($/gallon)'].values
model = LinearRegression().fit(x, y)

# model.coef_
#model.intercept_ + model.coef_ 

st.markdown("The situation looks bleak. Gas prices are pretty standard around the country and after plotting the cost rise over time it becomes apparent that there is going to be no end in sight. You even make a little statistical model to see how much the cost of gas is changing over time and you find the following. ")

st.markdown("**Average electric cost change with a time series regression model:**")
st.markdown("###### $ \hat{Y}_i \ \\text{(Estimated Gasoline Cost)}\ = \\text{}" 
            + str(round(model.intercept_, 2))  + 
            " + " 
            + str({round(model.coef_[0], 6)}) + 
            "\\text{}\ X_i \ \\text{(Years)}$")

for i in range(1,50):
    if model.intercept_ + model.coef_ * i > 0:
        st.markdown("###### According to the model the cost of gasoline is 1x the original cost every " + str(i) + " years")
        break

st.markdown("And that's not all, you find after doing some more research that some of the most influential economists in the US are predicting the price to grow to **$7.00** a gallon by end of year! But, now you need benchmark to compare a traditional fuel propelled vehicle to an EV. To gain insight some simple summary statistics could be all you need.")
st.markdown("")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
file_ = open("gifs/stat_search.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',  unsafe_allow_html=True,)
st.markdown("")
st.markdown("")

st.markdown("The department of transportation reports the following figures:")

image = Image.open('photos/gasoline_stats.png')
st.image(image)

st.markdown("You also find the average fuel economy for the common types of transportation on the road right now:")

vehicle_type = pd.read_excel('Data/10310_fuel_economy_by_vehicle_type_3-26-20.xlsx')
#st.dataframe(vehicle_type.style.highlight_max(axis=0))

a = alt.Chart(vehicle_type).encode(
    x = alt.X('MPG Gasoline:Q', axis=alt.Axis(title='', tickCount=1)),
    y = alt.Y('Vehicle Type', sort =alt.EncodingSortField(field="x", op="min", order='descending')),
    tooltip=['Vehicle Type', 'MPG Gasoline']
).properties(width=700, height=500)
a = a.mark_circle(color = 'lightgrey', size=200) 
b = alt.Chart(vehicle_type.query("`Vehicle Type` == 'Car'")).encode(
    x = alt.X('MPG Gasoline:Q', axis=alt.Axis(title='', tickCount=1)),
    y = alt.Y('Vehicle Type', sort =alt.EncodingSortField(field="x", op="min", order='descending')),
    tooltip=['Vehicle Type', 'MPG Gasoline']
).properties(width=700, height=500)
b = b.mark_circle(color = 'red', size=400) 
c = alt.Chart(vehicle_type).encode(
    x = alt.X('MPG Diesel:Q', axis=alt.Axis(title='', tickCount=1)),
    y = alt.Y('Vehicle Type', sort=alt.EncodingSortField(field="x", op="min", order='descending')),
    tooltip=['Vehicle Type', 'MPG Diesel']
).properties(width=700, height=500)
c = c.mark_circle(color = 'lightgrey', size=200, opacity = .25) 
d = alt.Chart(vehicle_type.query("`Vehicle Type` == 'Car'")).encode(
    x = alt.X('MPG Diesel:Q', axis=alt.Axis(title='', tickCount=1)),
    y = alt.Y('Vehicle Type', sort=alt.EncodingSortField(field="x", op="min", order='descending')),
    tooltip=['Vehicle Type', 'MPG Diesel']
).properties(width=700, height=500)
d = d.mark_circle(color = 'red', size=300, opacity = .25) 

a = a+b+c+d
a = a.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
st.altair_chart(a, use_container_width=True)

st.markdown("Your personal car is sitting happily as the red dot in the bottom portion of the chart. This average along with the other stats discovered will now allow you to run some basic mathematics on the data to compare and contrast your own long term fuel cost against an electric alternative.")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("## Crunching the numbers,")

st.markdown("Taking the average annual miles, divided by the fuel economy, then multiplied by the current fuel rate you can figure a good idea of the cost to run a certain type of vehicle per month and per year.")

vehicle_type_chart = pd.DataFrame(
    vehicle_type.assign(**{"Monthly Regular Gas Cost":  "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Gasoline']) / 12) *fuel_stats.current_regular, 2).astype(str)},
                        **{"Monthly Mid-Grade Gas Cost":  "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Gasoline']) / 12) *fuel_stats.current_mid, 2).astype(str)},
                        **{"Monthly Premium Gas Cost":  "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Gasoline']) / 12) *fuel_stats.current_premium, 2).astype(str)},
                        **{"Monthly Diesel Gas Cost": "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Diesel']) / 12) *fuel_stats.current_diesel, 2).astype(str)},
                        **{"Yearly Regular Gas Cost":  "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Gasoline'])) *fuel_stats.current_regular, 2).astype(str)},
                        **{"Yearly Mid-Grade Gas Cost":  "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Gasoline'])) *fuel_stats.current_mid, 2).astype(str)},
                        **{"Yearly Premium Gas Cost":  "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Gasoline'])) *fuel_stats.current_premium, 2).astype(str)},
                        **{"Yearly Diesel Gas Cost": "$" + round(((fuel_stats.avg_annual_miles / vehicle_type['MPG Diesel'])) *fuel_stats.current_diesel, 2).astype(str)})
    .drop(['MPG Gasoline', 'MPG Diesel'], axis=1))
st.table(vehicle_type_chart)

image = Image.open('photos/personal_car_title.png')
st.image(image)

image = Image.open('photos/red_car.png')
st.image(image)

col1, col2, col3, col4= st.columns(4)
col1.metric("Vehicle Type", "Car", delta_color="off")
col2.metric("Fuel Type", "Regular", delta_color="off")
col3.metric("Fuel Economy", "24.2 mpg", delta_color="off")
col4.metric("Annual Cost for Fuel", "$2,950.44", delta_color="off")

image = Image.open('photos/personal_car_cost.png')
st.image(image)

st.markdown("With a short analysis done, and a benchmark to beat, you can now explore and compare an EV to your car to see the cost difference over time.")