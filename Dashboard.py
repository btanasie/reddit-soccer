import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from helper import *
admin = False
c1 = st.sidebar.checkbox('Admin Mode', False)
st.sidebar.image('./images/mcgill_logo.png')

st.title('Reddit Soccer Analysis')
st.sidebar.markdown('**By:** Anukriti, Siddharth, Richard, Bogdan')
st.sidebar.markdown('**McGill MMA** - Text Analytics')
st.sidebar.markdown('**GitHub:** https://github.com/bogdan-tanasie/reddit-soccer')

if c1:
      admin = True
      # st.sidebar.text(admin)
else:
    admin = False
    # st.sidebar.text(admin)

@st.cache(persist=True)
def load_data(attributes=['good','bad']):

      return(load_lifts(attributes))

data_load_state = st.text('Loading data...')
loaded_data= load_data()
lift,attributes=loaded_data['team_lift'],loaded_data['attribute_lift']
data_load_state.text("Done! (using st.cache)")

st.subheader('Raw data')
st.write(lift)
st.write(attributes)


matches=list(set(loaded_data['data']['matchid'].copy().astype(str)))
option = st.selectbox(
    'Which match?',
    matches)
print(option)

match_attributes=match_lift(loaded_data['data'].copy(),option,loaded_data['top_10_team'],['good','bad'])
st.write(match_attributes)

HtmlFile = open("./html/lda_n10.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, width=1200, height=800)