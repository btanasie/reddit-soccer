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
    from datetime import datetime
    #pre_df = pd.read_csv('./data/pre_soccer_replaced.csv')
    #post_df = pd.read_csv('./data/post_soccer_replaced.csv')

    import pickle
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    from nltk.corpus import stopwords
    df_tk_pre = pickle.load( open( "./data/pre_df_tk.p", "rb" ) )
    df_tk_pre['ptitle'] = [text.lower() for text in df_tk_pre['ptitle']]
    df_tk_pre['involved_teams'] = [x.split(" vs ") for x in df_tk_pre['involved_teams']]
    keywords = pd.read_csv('./data/teams.csv')
    teams = list(map(str.lower, list(set(keywords.iloc[:, 0]))))
    
    top10_team_names = GetTopN(df_tk_pre, teams, 15, 'brands',[5,len(df_tk_pre.columns)-1],tokenize=False)
    top5_team_names = GetTopN(df_tk_pre, teams, 5, 'brands',[5,len(df_tk_pre.columns)-1],tokenize=False)
    top5_attributes = GetTopN(df_tk_pre, attributes, 5, 'attributes',[5])
    top10_attributes = GetTopN(df_tk_pre, attributes, 10, 'attributes',[5])

    teams_association = pd.DataFrame(0, columns=top10_team_names, index=top10_team_names)
    teams_association = CountMentions(df_tk_pre, teams_association,5)
  

    return(teams_association)

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

st.subheader('Raw data')
st.write(data)


HtmlFile = open("./html/lda_n10.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, width=1200, height=800)