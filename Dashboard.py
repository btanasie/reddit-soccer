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

@st.cache(persist=True, allow_output_mutation=True)
def load_data(attributes=['good','bad']):
    #predictions = pd.read_csv('./data/garbage_predictions.csv')
    import pickle
    predictions = pickle.load( open( "./data/predicted.p", "rb" ) )
    # predictions['involved_teams_str'] = predictions['involved_teams'].apply('_'.join)
    #predictions['matchid'] = predictions['involved_teams'].astype(str)+" "+predictions['pcreated_date'].astype(str)
    return (load_lifts(attributes), predictions)


def load_groupby(loaded_data):
    all_words, all_words_str = group_by_involved_teams(loaded_data['data'])
    return all_words, all_words_str

import re

st.header('Data')
input_attributes = st.text_input("Please enter attributes (ie. good,bad)")
if(len(input_attributes)==0):
    toassess=['good','bad']
else:
    toassess=input_attributes.split(",")

    

data_load_state = st.text('Loading data...')
loaded_data, predictions = load_data(toassess)
all_words, all_words_str = load_groupby(loaded_data)
lift,attributes=loaded_data['team_lift'],loaded_data['attribute_lift']
data_load_state.text("Done! (using st.cache)")

c1 = st.checkbox("Show/Hide Raw Data", True)
if c1:
    st.write(lift)
    st.write(attributes)

st.header('Matchup Analysis')
matches = list(set(loaded_data['data']['matchid'].copy().astype(str)))
option = st.selectbox(
    'Which match?',
    matches)

st.text('Matchup Lift')
match_attributes = match_lift(loaded_data['data'].copy(), option, loaded_data['top_10_team'],toassess)
st.write(match_attributes)
         
st.text('Matchup Sentiment')
sentiment=predictions[predictions['matchid']==option]['sentiment'].reset_index(drop=True)
st.write(sentiment)

prediction=predictions[predictions['matchid']==option]['winner_predict'].reset_index(drop=True)[0]
st.text('Our winner prediction: {}'.format(prediction))


st.subheader('Wordcloud based on involved teams')
teams = option.replace('[', '').replace(']', '').split(',')
involved_teams = [teams[0], teams[1].split()[0]]
team_value_str = all_words_str[str(involved_teams[0] + '_' + involved_teams[1]).replace("'", "")]
st.image(get_word_cloud(team_value_str))

st.header('Topic Modeling Per Matchup')
HtmlFile = open("./html/lda_n5" + str(involved_teams[0] + '_' + involved_teams[1]).replace("'", "") + ".html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, width=1200, height=800)

st.header('Topic Modeling All Teams')
option = st.selectbox('Which pre-processing?',
    ('tfidf','bag of words'))

if(option=="bag of words"):
    HtmlFile = open("./html/lda_n10.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, width=1200, height=800)
else:
    HtmlFile = open("./html/ldatf-idf_n10.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, width=1200, height=800)