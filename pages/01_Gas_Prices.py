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
st.markdown(" you are currently standing at a gas pump. Card swiped, nozzle in hand, and wincing as you select the grade of fuel for your gas. How frustrated and confused are you seeing the prices? You may think this is out of control, gas was 25¢ chaper like three days ago!")

image = Image.open('photos/gas_pump_slim.png')
st.image(image, caption='Gas prices as of June 18, 2022 https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm')

col1, col2, col3, col4= st.columns(4)
col1.metric("Diesel", "$" + str(fuel_stats.current_diesel), str(int((fuel_stats.current_diesel / 3.287) * 100)) + '% since 2021', delta_color="off")
col2.metric("Regular", "$" + str(fuel_stats.current_regular), str(int((fuel_stats.current_regular / 3.008) * 100)) + '% since 2021', delta_color="off")
col3.metric("Mid-grade", "$" + str(fuel_stats.current_mid), str(int((fuel_stats.current_mid / 3.432) * 100)) + '% since 2021', delta_color="off")
col4.metric("Premium", "$" + str(fuel_stats.current_premium), str(int((fuel_stats.current_premium / 3.687) * 100)) + '% since 2021', delta_color="off")

st.markdown("**Wow! Thank goodness** you don't own a large 1-ton diesel truck, that's absolutely **outrageous**! But, you still have to fuel up your ride. After a minute or two your tank is full and you have a large difference in your bank account. You storm away frustrated and sad you can't justify a late night pizza and movie night.") 
st.markdown("You consider, on the way home you think about how you can start saving money at the pump... want to start riding your bike everywhere? No thanks. You start thinking about your neigbors shiny new electric vehicle they keep raving about to you and all your neighbors. You've been thinking about an upgrade for a while now, maybe this is a good time to see whats available out there.")
st.markdown("")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("## Later that day,")
st.markdown("You sit down on your laptop and search for gas prices in America, you want to see if things are really as bad as you think or if your local gas station is just a bad case of gutting locals. You find...")

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

st.markdown(" Considering the values from your charts, running a linear regression doesn't seems like a logical approach to predicting future costs of both gasoline and electricity. You find the following models:")

st.markdown("**Average electric cost change with time series regression model:**")
st.markdown("###### $ \hat{Y}_i \ \\text{(Estimated Gasoline Cost)}\ = \\text{}" 
            + str(round(model.intercept_, 2))  + 
            " + " 
            + str({round(model.coef_[0], 6)}) + 
            "\\text{}\ X_i \ \\text{(Years)}$")

for i in range(1,50):
    if model.intercept_ + model.coef_ * i > 0:
        st.markdown("###### According to the model the cost of gasoline is 1x the original cost every " + str(i) + " years")
        break

st.markdown("And that's not all, you find some of the influential economists in the US predicting this price to grow to **$7.00** a gallon by end of year! So, you keep doing some research and find some interesting statistics that will help you know the average cost of owning a traditional fuel propelled car.")
st.markdown("")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
file_ = open("gifs/stat_search.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',  unsafe_allow_html=True,)
st.markdown("")
st.markdown("")

st.markdown("As you keep doing some research you begin fiding some interesting stats that can help you uncover the actual cost of keeping your gasoline powered car on the road. The internet is full of interesting findings and summary statistics here are a few that help draw the bigger picture.")

image = Image.open('photos/gasoline_stats.png')
st.image(image)

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

st.markdown("Plotting the average fuel economy of all the different types of vehicles that are on the road today. Your car that you currently own is sitting happily as the red dot in the bottom portion of the chart. This average along with the other stats discovered will now allow you to run some basic mathematics on the data to compare and contrast your own long term fuel cost against an electric alternative.")

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

st.markdown("With a short analysis done, and a benchmark to beat, you decide to explore the contrasting electric vehicle alternative.")