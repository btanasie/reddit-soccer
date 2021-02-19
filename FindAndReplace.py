import pandas as pd

pre_df = pd.read_csv('./data/pre_soccer_extraction.csv')
post_df = pd.read_csv('./data/post_soccer_extraction.csv')
teams = pd.read_csv('./data/teams.csv')

post_df['comment'] = post_df['comment'].str.lower()
pre_df['comment'] = post_df['comment'].str.lower()
teams['Other Name'] = teams['Other Name'].str.lower()


def Replace(df, replace_list, key):
  #for i in range(0,len(df)):
  for (main_value, to_replace) in replace_list.values:
    df[key].replace({to_replace: main_value}, regex=True,inplace=True)
    #df[key][i] = df[key][i].replace(to_replace.lower(), main_value.lower())

  return df


post_df = Replace(post_df, teams, 'comment')
pre_df = Replace(pre_df, teams, 'comment')

pre_df.to_csv('./data/pre_soccer_replaced.csv',index=False)
post_df.to_csv('./data/post_soccer_replaced.csv',index=False)