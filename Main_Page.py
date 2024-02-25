# %%
import numpy as np
import altair as alt
import pandas as pd
from PIL import Image
from sqlalchemy import null
import streamlit as st

from datetime import datetime
import polars as pl
import plotly.graph_objects as go

st.markdown("# Budgeting and Finance App Title")

st.markdown("Blah, some context maybe some good stuff to look at and review")

class fd: 
    year = datetime.now().year
    month = datetime.now().month
    
    # taxes 
    state = "Arizona" # maybe offer a drop down off all the states in a list and they can pick one. 
    state_tax = 0.03 # maybe we can do a dictionary for all the states or states abbreviated in the data. 
    FICA_tax = 0.065 
    
    single_deduction_amount = 14600.0 #          2024 amount
    max_personal_401k_contribution = 23000.0 #   2024 max
    max_traditional_IRA_contributions = 7000.0 # 2024 max
    personal_401k_contribution = 0.0
    traditional_IRA_contributions = 0.0 # research this if it clashes with the 401k max
    # HSA = 0
    # college_plans = 0
    # retirement limits
    
    gross = 0.0
    taxable_income = 0.0
    net = 0.0
    
# ———————————————————————————————————————————————————————————————————————————————————————————————— #
# %%
def fed_tax_burden(income):
    if income <= 11600:
        tax = [income * 0.1, "10%"]
    elif income <= 47150:
        tax = [(income - 11600) * 0.12 + 1160.0, "12%"]
    elif income <= 100525:
        tax = [(income - 47150) * 0.22 + 5426.0, "22%"]
    elif income <= 191950:
        tax = [(income - 100525) * 0.24 + 17168.5, "24%"]
    elif income <= 243725:
        tax = [(income - 191950) * 0.32 + 39110.5, "32%"]
    elif income <= 609350:
        tax = [(income - 243725) * 0.35 + 55678.5, "35%"]
    else:
        tax = [(income - 609350) * 0.37 + 183647.25, "37%"]
    return tax

print(fed_tax_burden(70000))
# ———————————————————————————————————————————————————————————————————————————————————————————————— #
# %%
st.markdown("## Budget Breakdown")
st.markdown("### Income")
col1, col2, col3 = st.columns(3) 

pay = col1.number_input("Paycheck Total ", min_value=0.0, step=500.0, help = '')
pay_periods = col2.number_input("Pay Periods Per Year", min_value=0.0, step=12.0, help = '')
extra_in = col3.number_input("Additional Monthly Income", min_value=0.0, step=100.0, help = '')
income = sum([(pay * pay_periods) / 12, extra_in])


st.markdown("### Expenses")
col1, col2, col3 = st.columns(3) 

housing = col1.number_input('Housing', min_value=0.0, step=500.0, help = 'This is your monthly rent or mortgage payment.')
power = col2.number_input('Power', min_value=0.0, step=25.0, help = '')
utilities = col3.number_input('Utilities', min_value=0.0, step=25.0, help = '')
food = col1.number_input('Food', min_value=0.0, step=50.0, help = '') 
internet = col2.number_input('Internet', min_value=0.0, step=25.0, help = '')
phone = col3.number_input('Phone', min_value=0.0, step=25.0, help = '')
vehicle = col1.number_input('Vehicle', min_value=0.0, step=100.0, help = '')
gas = col2.number_input('Gas', min_value=0.0, step=25.0, help = '')
insurance = col3.number_input('Insurance', min_value=0.0, step=100.0, help = '')
medical = col1.number_input('Medical', min_value=0.0, step=25.0, help = '')
fun = col2.number_input('Fun', min_value=0.0, step=25.0, help = '')
donations = col3.number_input('Donations', min_value=0.0, step=50.0, help = '')
expenses = sum([housing, power, gas, utilities, internet, phone, vehicle, insurance, food, medical, fun, donations])


col1.markdown("### Totals")
col1, col2, col3 = st.columns(3) 

col1.markdown("###### Monthly Income: $" + str(round(income, 2)))
col2.markdown("###### Monthly Expenses: $" + str(round(expenses, 2)))
col3.markdown("###### Monthly Remaining: +$" + str(round(income - expenses, 2)))
col1.markdown("###### Yearly Income: $" + str(round(income * 12, 2)))
col2.markdown("###### Yearly Expenses: $" + str(round(expenses * 12, 2)))
col3.markdown("###### Yearly Remaining: +$" + str(round((income * 12) - (expenses * 12), 2)))




label_list = ["Income", "Remaining", "Expenses", "Housing", "Power", "Gas", "Utilities", "Internet", "Phone", "Vehicle", "Insurance", "Food", "Medical", "Fun","Donations"]
source = [0, 0] + [2 for i in range(len(label_list) - 2)]
target = list(range(1,len(label_list)))
count = [income - expenses, expenses, # two splits for income
         housing, power, gas, utilities, internet, phone, vehicle, insurance, food, medical, fun, donations # mutlisplit for expenses
         ]

fig = go.Figure(data=[go.Sankey(
    node = {"label": label_list},
    link = {"source": source, "target": target, "value": count})])

st.plotly_chart(fig)


# ———————————————————————————————————————————————————————————————————————————————————————————————— #
st.markdown("## Taxes")

col1, col2, col3 = st.columns(3)
fd.gross = col1.number_input(str(fd.year) + ' Gross Income', min_value=0.0, step = 10000.0, help="")
fd.personal_401k_contribution = col2.number_input('Pre-Tax 401k Contributions', min_value=0.0, max_value = fd.max_personal_401k_contribution,step = 1000.0, help="")
if fd.gross <= 7e4:
    fd.traditional_IRA_contributions = col3.number_input("Traditional IRA Contributions: $", min_value=0.0, step = 1000.0, max_value= fd.max_traditional_IRA_contributions)

fd.taxable_income = fd.gross - fd.personal_401k_contribution - fd.single_deduction_amount - fd.traditional_IRA_contributions
# fd.net = fd.gross - fed_tax_burden(fd.taxable_income)[0] - fd.personal_401k_contribution - (fd.state_tax * fd.taxable_income) - (fd.FICA_tax * fd.gross)

col1.markdown("##### Federal")
col1.markdown("###### Tax Bracket: " + fed_tax_burden(fd.gross - fd.single_deduction_amount)[1])
col1.markdown("###### Tax Amount: $" + str(fed_tax_burden(fd.gross - fd.single_deduction_amount)[0]))
col1.markdown("###### Tax % Income: " + str(round((fed_tax_burden(fd.gross - fd.single_deduction_amount)[0] / fd.gross) * 100, 2)) + "%")

col2.markdown("##### With 401k")
col2.markdown("###### Tax Bracket: " + fed_tax_burden(fd.taxable_income  + fd.traditional_IRA_contributions)[1])
col2.markdown("###### Tax Amount: $" + str(fed_tax_burden(fd.taxable_income + fd.traditional_IRA_contributions)[0]))
col2.markdown("###### Tax % Income: " + str(round((fed_tax_burden(fd.taxable_income + fd.traditional_IRA_contributions)[0] / fd.gross) * 100, 2)) + "%")

if fd.gross <= 7e4:
    col3.markdown("##### With Pre-Tax IRA")
    col3.markdown("###### Tax Bracket: " + fed_tax_burden(fd.taxable_income)[1])
    col3.markdown("###### Tax Amount: $" + str(fed_tax_burden(fd.taxable_income)[0]))
    col3.markdown("###### Tax % Income: " + str(round((fed_tax_burden(fd.taxable_income)[0] / fd.gross) * 100, 2)) + "%")

col1.markdown("##### State")
col1.markdown("###### Tax Bracket: " + fed_tax_burden(fd.gross - fd.single_deduction_amount)[1])
col1.markdown("###### Tax Amount: $" + str(fed_tax_burden(fd.gross - fd.single_deduction_amount)[0]))
col1.markdown("###### Tax % Income: " + str(round((fed_tax_burden(fd.gross - fd.single_deduction_amount)[0] / fd.gross) * 100, 2)) + "%")

    
    
    
    
st.markdown(fd.taxable_income)
st.markdown(fed_tax_burden(fd.taxable_income))

st.markdown(fd.state_tax * fd.taxable_income)
st.markdown((fd.state_tax * fd.taxable_income) / 26)
st.markdown(fd.state_tax * fd.FICA_tax * fd.gross)
st.markdown(fed_tax_burden(fd.taxable_income)[0] / 26)
st.markdown(fed_tax_burden(fd.taxable_income)[0] / 12)
st.markdown(fd.net)
st.markdown(fd.net)


# st.sidebar.markdown("## EV Models")

# selected_model = st.sidebar.select_slider(
#     'Most to Least Expensive',
#     options=car_data['2022_ev_model'],
#     help = 'This is not a complete list of all availabe vehicles, but instead represents the current EV market by showing all ranges of prices and ranges.')
# selected = car_data[car_data['2022_ev_model'] == selected_model]

# st.markdown("## " + selected_model)
# st.image(Image.open('photos/car_photos/' + selected_model + '.jpeg'))

# col1, col2, col3, col4= st.columns(4)
# col1.metric("MSRP", '$' + str(selected.iloc[0]['msrp']), delta_color="off")
# col2.metric("Max HP", str(selected.iloc[0]['max_hp']) + ' hp', delta_color="off")
# if  selected.iloc[0]['range_miles'] > 0:
#     col3.metric("Range", str(round(selected.iloc[0]['range_miles'])) + ' miles', delta_color="off")
# else:
#     col3.metric("Range", 'TBD', delta_color="off")
# col4.metric("Type", str.upper(selected.iloc[0]['ev']), delta_color="off")

# st.markdown("The selected car from the slider is showing red on this chart to show a quick difference in specs to the other EVs on the market. To change the Y-axis variable use the radio button on the sidebar.")

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
# selection = st.sidebar.radio(
#      "Choose Y Variable",
#      ('Horse Power', 'Range','Fuel Economy'))

# Y = null
# if selection == 'Horse Power':
#     Y = 'max_hp'
#     Y2 = 'max_hp_fuel'
# if selection == 'Range':
#     Y = 'range_miles'
#     Y2 = 'range_miles_fuel'
# if selection == 'Fuel Economy':
#     Y = 'fuel_economy'
#     Y2 = 'fuel_economy_fuel'

# def plot_specs(_Y):
#     c = alt.Chart(car_data).encode(
#         x = alt.X('msrp', scale=alt.Scale(domain=[2e4, 12e4])),
#         y = alt.Y(_Y),
#         tooltip=['2022_ev_model', 'msrp', 'max_hp', 'range_miles']
#     ).properties(width=700, height=500)
#     c = c.mark_circle(color = 'lightgrey', size = 100) 
#     b = alt.Chart(selected).encode(
#         x = alt.X('msrp', scale=alt.Scale(domain=[2e4, 12e4])),
#         y = alt.Y(_Y),
#         tooltip=['2022_ev_model', 'msrp', 'max_hp', 'range_miles']
#     ).properties(width=700, height=500)
#     b = b.mark_circle(color = 'red', size = 200) 
#     d = c + b
#     d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
#     st.altair_chart(d, use_container_width=True)
# plot_specs(Y)

# ———————————————————————————————————————————————————————————————————————————————————————————————— #
# st.markdown("# Fuel Comparable Model")
# st.markdown("To compare apples to apples as best as possible it seems like a useful comparison to look at vehicles that **cost the same as an electric model**. Seeing this comparison may make an even stronger case for the possible fuel savings over time. But, as you may see, this isn't the entire story. Some of the electric cars may have a lot less power and range compared to their gasoline cost equivalents. These trade-offs are variables to consider if you plan on going with an EV.")

# st.markdown("## " + selected.iloc[0]['Comparable_fuel_model'])
# st.image(Image.open('photos/car_photos/' + selected.iloc[0]['Comparable_fuel_model'] + '.jpeg'))

# col1, col2, col3, col4= st.columns(4)
# col1.metric("MSRP",
#             '$' + str(selected.iloc[0]['msrp_fuel']),
#             'Equally Priced',
#             delta_color="off")
# col2.metric("Max HP", 
#             str(selected.iloc[0]['max_hp_fuel']) + ' hp', 
#             str(selected.iloc[0]['max_hp_fuel'] - selected.iloc[0]['max_hp']) + ' hp', 
#             delta_color="normal")
# if selected.iloc[0]['range_miles_fuel'] > 0 and selected.iloc[0]['range_miles'] > 0:
#     col3.metric("Range", 
#                 str(round(selected.iloc[0]['range_miles_fuel'])) + ' miles',
#                 str(round(selected.iloc[0]['range_miles_fuel']) - round(selected.iloc[0]['range_miles'])) + ' miles', 
#                 delta_color="normal")
# else:
#     col3.metric("Range", 'TBD', delta_color="off")
# col4.metric("Fuel Type", str(selected.iloc[0]['fuel_type']), delta_color="off")

# st.markdown("You notice that some of the differences between the specs on the EV model and the fuel model reflect in color coding. This is an interesting distinction that will help you see the difference at a glimpse.")
# st.markdown("")

# def plot_specs(_Y2):
#     c = alt.Chart(car_data).encode(
#         x = alt.X('msrp_fuel', scale=alt.Scale(domain=[2e4, 12e4])),
#         y = alt.Y(_Y2),
#         tooltip=['Comparable_fuel_model', 'msrp_fuel', 'max_hp_fuel', 'range_miles_fuel']
#     ).properties(width=700, height=500)
#     c = c.mark_circle(color = 'lightgrey', size = 100) 
#     b = alt.Chart(selected).encode(
#         x = alt.X('msrp_fuel', scale=alt.Scale(domain=[2e4, 12e4])),
#         y = alt.Y(_Y2),
#         tooltip=['Comparable_fuel_model', 'msrp_fuel', 'max_hp_fuel', 'range_miles_fuel']
#     ).properties(width=700, height=500)
#     b = b.mark_circle(color = 'red', size = 200) 
#     d = c + b
#     d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
#     st.altair_chart(d, use_container_width=True)
# plot_specs(Y2)

# # ———————————————————————————————————————————————————————————————————————————————————————————————— #
# st.markdown("# Anticipated cost comparison:")
# st.markdown("#### Electric Powered: " + selected_model)
# col1, col2, col3 = st.columns(3)
# col1.metric('EV MSRP', 
#            '$' + (selected.iloc[0]['msrp']).astype(str),
#            delta_color="off")
# col2.metric("Lifetime Electricity Cost",
#             "$" +
#             round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric, 2).astype(str),
#             delta_color="off")
# col3.metric("Total Cost of Ownership", 
#             "$" + 
#             round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric + (selected.iloc[0]['msrp']), 2).astype(str),
#             delta_color="off")

# st.markdown("#### Gas Powered: " + selected.iloc[0]['Comparable_fuel_model'])
# col1, col2, col3 = st.columns(3)
# col1.metric('Fuel MSRP', 
#            '$' + (selected.iloc[0]['msrp_fuel']).astype(str),
#            delta_color="off")
# col2.metric("Lifetime Fuel Cost",
#             "$" +
#             round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership, 2).astype(str),
#             delta_color="off")
# col3.metric("Total Cost of Ownership", 
#             "$" + round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership +(selected.iloc[0]['msrp_fuel']), 2).astype(str),
#             '$' + round(round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership + (selected.iloc[0]['msrp_fuel']), 2) - round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric + (selected.iloc[0]['msrp']), 2), 2).astype(str),
#             delta_color='off')

# st.markdown("Comparing both of these vehicles side by side and looking at an estimated overall cost, the estimated savings of the **" + 
#             selected_model + 
#             '** over the **' + 
#             selected.iloc[0]['Comparable_fuel_model'] + 
#             '** is:')

# st.markdown("### $" + round(round((((fuel_stats.avg_annual_miles / selected.iloc[0]['fuel_economy_fuel'])) * fuel_stats.current_premium) * fuel_stats.avg_length_of_ownership + (selected.iloc[0]['msrp_fuel']), 2) - round((((fuel_stats.avg_annual_miles *  fuel_stats.avg_length_of_ownership) / 100) * selected.iloc[0]['kWh']) * fuel_stats.current_electric + (selected.iloc[0]['msrp']), 2), 2).astype(str))

# st.markdown("")
# st.markdown("Out of all the electric vehicles on the market right now, there are still some that are more efficient than others. The **" + selected_model + "** falls here compared to the rest of the EVs. Note: The higher the kWh/100 mile rating the less efficient it is. That being said if your goal is to save the most money possible and use less resources, consider some of the ones on the right side of the chart. ")
# st.markdown("")

# c = alt.Chart(car_data).mark_point(filled=True, size=100, color = 'lightgrey').encode(
#     x = alt.X('kWh', scale=alt.Scale(reverse=True)),
#     tooltip=['2022_ev_model', 'kWh', 'msrp', 'range_miles']
#     ).properties(width=700, height=100)
# b = alt.Chart(selected).mark_point(filled=True, size=200, color = 'red').encode(
#     x = alt.X('kWh', scale=alt.Scale(reverse=True)),
#     tooltip=['2022_ev_model', 'kWh', 'msrp', 'range_miles']
#     ).properties(width=700, height=100)
# d = c + b
# d = d.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
# st.altair_chart(d, use_container_width=True)

# st.markdown("**Note:** Some manufacturers have better tech than others in this space. Tesla, for example, has been improving and polishing it's evs for years and as such many of there models are more efficient, powerful, and reasonably priced. Another car company that has made some impressive strides is General Motors with their Ultium battery system. It's so modular and solid that other companies, like Honda Mtrs. is joining GM to build their electric vehicles on their platform. Be aware of these differences as you prepare to grab a new ev, they can make a large difference in the long run.")
# %%
