import praw
import pandas as pd

reddit = praw.Reddit(client_id='d8FC4nZtpiV5tw', client_secret='Zqa3Hy5ePYBNbMGxX_zSyr_tiF3Z-A', user_agent='soccer_scraper')

def GetPosts(soccer_subreddit):
  # Get
  posts = []
  for post in soccer_subreddit:
      # Get comments
      comments = []
      submission = reddit.submission(id=post.id)
      submission.comments.replace_more(limit=None)
      for comment in submission.comments.list():
        #comments.append(comment.body.replace('\n', ' ').replace('\r', ' '))
        # print(comment.created)
        # print(comment.author)
        posts.append([post.title, post.score, post.id, post.selftext, post.created, comment.body.replace('\n', ' ').replace('\r', ' '), comment.author, comment.created])

  return pd.DataFrame(posts, columns=['ptitle', 'pscore', 'pid', 'pbody', 'pcreated', 'comment', 'cauthor', 'ccreated'])

pre_soccer_subreddit = reddit.subreddit('soccer').search('flair:Pre Match Thread')
pre_posts = GetPosts(pre_soccer_subreddit)

pre_soccer_subreddit = reddit.subreddit('soccer').search('flair:Post Match Thread')
post_posts = GetPosts(pre_soccer_subreddit)

pre_posts.to_csv("./data/pre_soccer_extraction.csv",index=False)
post_posts.to_csv("./data/post_soccer_extraction.csv",index=False)