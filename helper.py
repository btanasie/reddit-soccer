# Count values, lift, and MDS
import pandas as pd
import wordcloud as wc
from nltk.corpus import stopwords

def mentions(words,text):
  for word in words:
    if word not in text:
        return False
  return True
  
def allmentions(words,texts):
  mentionedcount = 0
  comentions=[]
  for text in texts:
    comention=mentions(words,text)
    if(comention):
      mentionedcount+=1
      comentions.append(True)
    else:
      comentions.append(False)
  return(mentionedcount,comentions)

def lift(countx,county,countxy,N):
  return(countxy/N)/((countx/N)*(county/N))
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import string

def TokenizeProcess(df,column):
    word_lemmatizer = WordNetLemmatizer()

    df_tk = pd.DataFrame(columns=[column])#columns=['ptitle', 'pscore', 'pid', 'pbody', 'pcreated', 'comment', 'cauthor', 'ccreated'])

    for comment in df.values.tolist():
        # Tokenize
        tokens = word_tokenize(str(comment))

        # Strip punctuation
        punctuation_list = str.maketrans('', '', string.punctuation)
        tokens_strp = [w.translate(punctuation_list) for w in tokens]

        # Remove other non-alphabetic tokens
        words = [word for word in tokens_strp if word.isalpha()]

        # Stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        # Lemmatize
        # Note: We might need to do this for the brands we want to detect as well
        words_lm = [word_lemmatizer.lemmatize(w) for w in words]
        df_tk = df_tk.append({column:words} ,ignore_index=True) 
    return df_tk

def GetTopN(df, words, n, word_type,columnnos,tokenize=False):
  if(tokenize==True):
    words = TokenizeProcess(df,df.columns[columnnos])
  words_count = dict.fromkeys(words, 0)  
  
  for row in df.values.tolist():
    comment = []
    for col in columnnos:
        comment.extend(row[col])
    for word in words_count:
      if word in comment:
        words_count[word] += 1
  
  words_df = pd.DataFrame.from_dict(words_count, orient='index')
  print('\nTop {} {} are:'.format(n, word_type))
  top_n_words = words_df.sort_values(by=[0], ascending=False).head(n)
  print(top_n_words)
  return top_n_words.index.tolist()


def mentions(words,text):
  for word in words:
    if word not in text:
        return False
  return True

def allmentions(words,texts):
  mentionedcount = 0
  comentions=[]
  for text in texts:
    comention=mentions(words,text)
    if(comention):
      mentionedcount+=1
      comentions.append(True)
    else:
      comentions.append(False)
  return(mentionedcount,comentions)

def lift(countx,county,countxy,N):
  return(countxy/N)/((countx/N)*(county/N))


#Define a function to calculate Lift
def liftcal(df_tk,word_1,word_2,ofinterest):
    w1count = sum(df_tk.apply(lambda x: word_1 in x[ofinterest], axis=1))
    w2count = sum(df_tk.apply(lambda x: word_2 in x[ofinterest], axis=1))
    bothcount = sum(df_tk.apply(lambda x: word_1 in x[ofinterest] and word_2 in x[ofinterest], axis=1))
    try:
      res= float(bothcount/len(df_tk))/((float(w1count)/len(df_tk))*(float(w2count)/len(df_tk)))
      return res
    except:
      return 0 

def liftcal_fromcounts(team_association,df_tk,word_1,word_2):
    w1count=team_association[word_1][word_1]
    w2count=team_association[word_2][word_2]
    bothcount= team_association[word_1][word_2]
    try:
      res= float(bothcount/len(df_tk))/((float(w1count)/len(df_tk))*(float(w2count)/len(df_tk)))
      return res
    except:
      return 0 

def CountMentions(df_tokenized, association_matrix,columnno):
  for row in df_tokenized.values.tolist():
    comment = row[columnno]
    for brand_col in association_matrix.columns:
      for brand_row in association_matrix.index:
        if brand_row in comment and brand_col in comment:
          association_matrix[brand_col][brand_row] += 1
  return association_matrix

def load_lifts(attributes=['good','bad']):
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
    match_plus_dates=df_tk_pre['involved_teams'].astype(str)+" "+df_tk_pre['pcreated_date'].astype(str)
    df_tk_pre['matchid'] = match_plus_dates
    
    
    keywords = pd.read_csv('./data/teams.csv')
    teams = list(map(str.lower, list(set(keywords.iloc[:, 0]))))
    
    top10_team_names = GetTopN(df_tk_pre, teams, 15, 'brands',[5,len(df_tk_pre.columns)-1],tokenize=False)
    top5_team_names = GetTopN(df_tk_pre, teams, 5, 'brands',[5,len(df_tk_pre.columns)-1],tokenize=False)

    top5_attributes = GetTopN(df_tk_pre, attributes, 5, 'attributes',[5])
    top10_attributes = GetTopN(df_tk_pre, attributes, 10, 'attributes',[5])

    teams_association = pd.DataFrame(0, columns=top10_team_names, index=top10_team_names)
    teams_association = CountMentions(df_tk_pre, teams_association,5)
  
    #Initialize empty dictionary for lift values
    brand_lifts = dict()
    import itertools
    top_team_combos = list(itertools.combinations(top10_team_names,2))


    #iterate over brand combinations, calculate lift, save to dictionary
    for i in range(0,len(top_team_combos)): 
        a,b = top_team_combos[i]
        brands = (a,b)
        lift = liftcal_fromcounts(teams_association,df_tk_pre,a,b)
        brand_lifts[brands] = lift
        
    df_lifts = pd.DataFrame(columns=top10_team_names,index=top10_team_names)
    for brand in top10_team_names: 
        df_lifts[brand][brand] = '-'
    for brands in brand_lifts:
        a,b = brands
        df_lifts[a][b] = (brand_lifts[brands])
        df_lifts[b][a] = '-'
        
    top_brand_lifts = pd.DataFrame(columns=top10_team_names,index=top10_team_names)

    #To calculate lift(dissimilarity)
    for brands in brand_lifts:
        a,b = brands
        try:
            top_brand_lifts[a][b] = (1/brand_lifts[brands])
            top_brand_lifts[b][a] = (1/brand_lifts[brands])
        except:
            top_brand_lifts[a][b] = 0
            top_brand_lifts[b][a] = 0
    for brand in top10_team_names: 
        top_brand_lifts[brand][brand] = 0

        
    team_atrib_associations=CountMentions(df_tk_pre,pd.DataFrame(columns=top10_team_names+top10_attributes, index=top10_team_names+top10_attributes).fillna(0),columnno=5)
    brand_attrib_combos = [ (i, j)
        for i in top10_team_names
        for j in top10_attributes ]

    attribute_lift = pd.DataFrame(columns=top10_team_names, index=top10_attributes)

    for brand in top10_team_names:
        for attribute in top10_attributes:
           attribute_lift[brand][attribute] = liftcal_fromcounts(team_atrib_associations,df_tk_pre,brand, attribute)
    

    return({'team_lift':top_brand_lifts,'team_counts':teams_association,'attribute_lift':attribute_lift,'team_atrib_counts':team_atrib_associations,'data':df_tk_pre,'top_10_team':top10_team_names,'top_10_attrib':top10_attributes})

def match_lift(df_tk_pre,match,top10_team_names,top10_attributes):
    #matches=list(set(df_tk_pre['involved_teams'].astype(str)))
#for match in matches:

    matches=list(set(df_tk_pre['matchid'].astype(str)))

    filtered=df_tk_pre[df_tk_pre['matchid'].astype(str)==match].reset_index(drop=True)
    team_atrib_associations=CountMentions(filtered,pd.DataFrame(columns=top10_team_names+top10_attributes, index=top10_team_names+top10_attributes).fillna(0),columnno=5)
    brand_attrib_combos = [ (i, j)
        for i in top10_team_names
        for j in top10_attributes ]
    #print(brand_attrib_combos)

    attribute_lift = pd.DataFrame(columns=top10_team_names, index=top10_attributes)

    for brand in top10_team_names:
        #print(brand)
        for attribute in top10_attributes:
           attribute_lift[brand][attribute] = liftcal_fromcounts(team_atrib_associations,filtered,brand, attribute)
    return(attribute_lift)


def group_by_involved_teams(df):
    all_words = {}
    all_words_str = {}
    df['involved_teams_str'] = df['involved_teams'].apply('_'.join)
    for teams, comment in df.groupby('involved_teams_str')['comment']:
        all_words[teams] = comment
        all_words_str[teams] = ','.join(list(map(','.join, comment)))
    return all_words, all_words_str

def get_word_cloud(value):
    wordcloud = wc.WordCloud(background_color="white", max_words=100000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(str(value))
    return wordcloud.to_image()
