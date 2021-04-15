import praw
import pandas as pd
import re
import datetime as dt
reddit = praw.Reddit(client_id="khD2wxnPocaxjA",
                     client_secret="ipAIgBiv7KUux0hqjYZZixoEm03N-g",  
                     user_agent="ben_scrape")
file = pd.read_csv('stock_tickers.csv')
tickers = file.iloc[:,0:2]
#tickers["Name"] = tickers["Name"].series.str.split(' ')[0]
#print(tickers)
counter = 0
tickerDict = {}
regex = re.compile('[^a-zA-Z ]')
for submission in reddit.subreddit('wallstreetbets').search('flair:"Daily Discussion"',limit = 1,syntax='lucene'):
   submission.comments.replace_more(limit = None)
   for comment in submission.comments.list():
       
       splitComment = regex.sub('',str(comment.body))
       splitComment = splitComment.split(' ')
       for word in splitComment:
            if word in tickerDict:
                tickerDict[word] += 1
            else:
                tickerDict[word] = 1
tickerCounter_df = pd.DataFrame.from_dict(list(tickerDict.items())).rename(columns = {0:"Symbol",1:"Frequency"})
final_ticker_df = pd.merge(tickers,tickerCounter_df, on ="Symbol")
final_ticker_df = final_ticker_df.sort_values(by = "Frequency", ascending = False, ignore_index = True)
print(final_ticker_df)
       #print(comment.body)
#print(tickers)
#print(counter)