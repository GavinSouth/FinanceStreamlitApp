
# ———————————————————————————————————————————————————————————————————————————————————————————————— #
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
import streamlit as st 

st.markdown("# Exciting, you've decided to buy an electric car!")

image = Image.open('photos/showroom.jpg')
st.image(image, caption='')

st.sidebar.markdown("# The Decision")

st.markdown("## After a ton of research,")
st.markdown(" you feel ready and confident in buying a new electric car. This decision, although not a simple one makes the most sense in the long run. After all, the numbers don't like, and you want all the pros that come along with it. Throughout this analysis we will explore the ins and outs of the electric car market and how it compares to the rest of the available vehicles out there. But, it will be done with the addition of a little data science flair. We will look at:")

st.markdown("#### • The absolute wild inflation of fuel prices and how much it's likely to increase.")
st.markdown("#### • The contrast of gas to the cost of electricity over time and how much it would save someone.")
st.markdown("#### • Similarly prices electric cars and gas powered cars to show contrast.")
st.markdown("#### • A well composed pros and cons list with some final considerations.")

st.markdown("")
image = Image.open('photos/geom.jpeg')
st.image(image, caption='')