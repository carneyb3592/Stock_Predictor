import praw
from psaw import PushshiftAPI
import pandas as pd
import re
import datetime as dt
reddit = praw.Reddit(client_id="khD2wxnPocaxjA",
                     client_secret="ipAIgBiv7KUux0hqjYZZixoEm03N-g",  
                     user_agent="ben_scrape")
api = PushshiftAPI(reddit)
counter = 0

start_time = int((dt.datetime.today() - dt.timedelta(days=1)).timestamp())
end_time = int(dt.datetime.today().timestamp())
#posts = list(api.search_submissions(after = start_time,before = end_time,subreddit = 'wallstreetbets', filter = ['title'], limit = None))
comments = list(api.search_comments(after = start_time,before = end_time,subreddit = 'wallstreetbets', filter = ['title'], limit = None))
counter = 0
for post in comments:
    print("")
    print(post.body)
    print("")
    counter += 1
print(counter)
# for submission in reddit.subreddit('wallstreetbets').search("today",limit = None):
#     print(submission.title)
#     print(" ")
#     counter += 1
#     #submission.comments.replace_more(limit = 1)
#     #for comment in submission.comments.list():
#     #    print(comment.body)
# #tickers = pd.read_csv('stock_tickers.csv')
# #print(tickers)
# print(counter)