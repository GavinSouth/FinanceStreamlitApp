# from math import floor
# from statistics import mean
# import numpy as np
# import pandas as pd
# import altair as alt
# from PIL import Image
# from sqlalchemy import null
# import streamlit as st 

# car_data = pd.read_excel('data/electric_car_market.xlsx')
# charging_inf = pd.read_excel('data/10964_ev_charging_infrastructure_1-27-22.xlsx')
# #st.dataframe(charging_inf.style.highlight_max(axis=0))

# # ———————————————————————————————————————————————————————————————————————————————————————————————— #
# # TO DO NEXT:
# st.markdown("# What to Consider")

# st.markdown("Just as with all decisions and options, there are pros and cons to what you decide to do. Electric vehicles are absolutely a viable option for transportation and in all honesty will be the future. But, there are some drawbacks that all owners should be a little aware of.")

# # ———————————————————————————————————————————————————————————————————————————————————————————————— #
# st.markdown("### Cons")

# st.markdown("#### 1. Range anxiety ")
# st.markdown("> Glancing at the charts and comparisons on the last page, it's obvious that most of these EV's lose in the arena of range. Just looking at the averages of the vehicles in the data used in this project; electric cars have an average range of **" + str(floor(mean(car_data['range_miles']))) + "** miles on a single charge. Whereas the fuel powered vehicles in the data have an average range of **" + str(floor(mean(car_data['range_miles_fuel']))) + "**. The difference is glaring and many people that have an EV find that road tripping with their cars is often impractical and can cause stress and burden. This is a multi-factored problem though and a shorter range is just one piece of the puzzle.")

# st.markdown("#### 2. Charging Time")
# st.markdown("> According to sources, the average time it takes to refill a gas powered vehicle at the pump is 4.5 min. Not surprising at all. But, to charge an electric vehicle at the most powerful self service electric power stations it can take on average around an 30 min - 1 hr to completely charge said car. This is the next big chink in the reputation of EV's. Consider a 12 hour trip with a travel distance of 850 miles. If the EV you purchase has around the average range aforementioned you would likely need to stop three times to charge (as long as infrastructure permits) to make it. That could add another three hours to an already very long trip. If you travel long distances often, prepare for this inconvenience.")

# st.markdown("#### 3. Poor Infrastructure")
# st.markdown("> The support of gasoline vehicles in the form of refueling is grand. Decades of building and demand have made it so common place and familiar to have options all over the country. Unfortunately, EVs dont share the same support. There is a major deficit in the options for charging all over the states. And, there are some large strides in the area, and companies are trying to catch up, but it's still behind. There are currently " + str(max(charging_inf['Station Locations'])) + " in the US compared to 145000 fueling stations. A large difference.")

# a = alt.Chart(charging_inf).encode(
#     x = alt.X('Year:O', axis=alt.Axis(tickCount=10)),
#     y = alt.Y('Station Locations', axis=alt.Axis(tickCount=3)),
#     tooltip=['Year', 'Station Locations', 'EVSE Ports']
# ).properties(width=700, height=200)
# b = a.mark_line(color = 'lightgreen') 
# c = a.mark_circle(color = 'lightgreen') 
# a = b + c
# a = a.configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
# st.altair_chart(a, use_container_width=True)

# # ———————————————————————————————————————————————————————————————————————————————————————————————— #
# st.markdown("### Pros")

# st.markdown("#### 1. Economy and Cost")
# st.markdown("> As established before, electric cars are cheaper in the long run in relation to the operating and energy cost to run them. But, thats not where the savings and incentives end. If someone purchases one of the electric vehicles thats available now they will be given the option to use a tax credit up to \$7,500. Which is a huge offset to the principle cost of the vehicle. But, be aware there is a limit on the number of tax credits available on electric cars. Like Tesla, which has sold too many vehicles and now their new customers are not able to utilize that credit. Another cost savings thing is the cost of maintenance difference between the two types of options. In June 2021, a U.S. Department of Energy report estimated that the scheduled maintenance cost of a light-duty battery-electric vehicle is less than 7¢ per mile. By comparison, a conventional internal combustion engine costs approximately 10¢ per mile to maintain. This will scale and ultimately save owners so much money in the long run.")

# st.markdown("#### 2. Power, Gobs of Power")
# st.markdown("> Sure, horse power and top speed of EVs can be almost indistinguishable compared to fuel powered cars, but electric cars have the most legit ace up their sleeves. Torque. Massive amounts of it. Torque being the generated force of twist that translates to the tires is the force that will propel the vehicle from a stand still up to speed. EVs have so much of it due to the mechanical nature of said systems that the fastest, most powerful vehicles in the world are powered by electricity. Consider the Tesla Model S Plaid, that is the first production car to sprint to 60 miles an hour faster than 2 seconds. If you like performance, consider the EV options.")

# st.markdown("#### 3. Efficiency")
# st.markdown("> Saving the planet, saving fuel, saving money its what's important to so many people. Just to put things into perspective; the all new electric GMC Hummer is just as efficient as a Toyota Prius. If thats not evidence of a huge difference in clean energy, I don't know what it. ")

# st.markdown("")
# st.markdown("")
# st.markdown("# Ultimately,")
# st.markdown("#### You have the choice, you can have cheap and fun transportation thats good around town. Or, expensive but convenient transportation that will take you the distance. Thats the big distinction. Both are good in their own rights, but you have decided after your research that an electric car is the way to go. The cost savings and the future proofing that comes with electric cars is just unparalleled! It will well be worth the cost, especially over time. Now, is the tricky part, picking out the model you like the most.")

# st.markdown("")
# st.markdown("")
# st.markdown("#### Sources")
# st.markdown('<https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm>')
# st.markdown("<https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=3&year1=2021&year2=2023&vtype=Electric&srchtyp=newAfv&pageno=3&rowLimit=50&sortBy=Comb&tabView=0>")
# st.markdown("<https://fred.stlouisfed.org/series/APU000072610>")
# st.markdown("<https://www.edmunds.com/fuel-economy/the-true-cost-of-powering-an-electric-car.html>")
# st.markdown("<https://arstechnica.com/cars/2022/04/the-hummer-ev-is-an-electric-truck-for-people-who-think-evs-are-stupid/:~:text=The%20official%20EPA%20efficiency%20figures,41%20kWh%2F100%20km).>")
# st.markdown("<https://www.edmunds.com/car-news/tested-2022-audi-e-tron-gt-beats-epa-range-by-53-miles.html>")
# st.markdown("<https://www.visualcapitalist.com/visualizing-all-electric-car-models-available-in-the-us/>")
# st.markdown("<https://www.cochrantoyota.com/electric-car-maintenance-costs-vs-gas/>")