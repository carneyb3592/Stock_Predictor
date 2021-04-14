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

#start_time = int((dt.datetime.today()- dt.timedelta(days=1)).timestamp())
#end_time = int((dt.datetime.today() - dt.timedelta(days=1)).timestamp())
#posts = list(api.search_submissions(after = start_time,subreddit = 'wallstreetbets', filter = ['title'], limit = None))
#comments = list(api.search_comments(after = start_time,subreddit = 'wallstreetbets', filter = ['title'], limit = None))
#counter = 0
#for post in comments:
#    print("")
#    print(post.title)
#    print("")
#    counter += 1
#print(counter)
for submission in reddit.subreddit('wallstreetbets').search('flair:"Daily Discussion"',limit = 1,syntax='lucene'):
    print(submission.title)
    print(" ")
    submission.comments.replace_more(limit = None)
    for comment in submission.comments.list():
        counter += 1
        #print(comment.body)
# #tickers = pd.read_csv('stock_tickers.csv')
# #print(tickers)
print(counter)