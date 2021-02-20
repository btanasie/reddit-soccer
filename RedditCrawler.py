import praw
import pandas as pd

reddit = praw.Reddit(client_id='d8FC4nZtpiV5tw', client_secret='Zqa3Hy5ePYBNbMGxX_zSyr_tiF3Z-A', user_agent='soccer_scraper')

def GetPosts(soccer_subreddit, timeline, limit, columns):
    # Get
    posts = []
    index = 0
    print(timeline)
    for post in soccer_subreddit:
        print(index)
        # Get comments
        submission = reddit.submission(id=post.id)


        if timeline == 'pre':
            submission.comments.replace_more(limit=limit)
            for comment in submission.comments.list():
                posts.append([post.title, post.score, post.id, post.selftext, post.created, comment.body.replace('\n', ' ').replace('\r', ' '), comment.author, comment.created])
        else:
            posts.append([post.title, post.score, post.id, post.selftext,post.created])

        index += 1
    print('\n')
    if timeline == 'pre':
        return pd.DataFrame(posts, columns=columns)
    else:
        return pd.DataFrame(posts, columns=columns)


pre_soccer_subreddit = reddit.subreddit('soccer').search('flair:Pre Match Thread')
pre_posts = GetPosts(pre_soccer_subreddit, timeline='pre', limit=None, columns=['ptitle', 'pscore', 'pid', 'pbody', 'pcreated', 'comment', 'cauthor', 'ccreated'])

post_soccer_subreddit = reddit.subreddit('soccer').search('flair:Post Match Thread')
post_posts = GetPosts(post_soccer_subreddit, timeline='post', limit=25, columns=['ptitle', 'pscore', 'pid', 'pbody','pcreated'])

pre_posts.to_csv("./data/pre_soccer_extraction.csv", index=False)
post_posts.to_csv("./data/post_soccer_extraction.csv", index=False)