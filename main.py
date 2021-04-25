import praw
import pandas as pd
import re
import datetime as dt
from datetime import date
pd.options.mode.chained_assignment = None
reddit = praw.Reddit(client_id="khD2wxnPocaxjA",
                     client_secret="ipAIgBiv7KUux0hqjYZZixoEm03N-g",  
                     user_agent="ben_scrape")
file = pd.read_csv('stock_tickers.csv')
tickers = file.iloc[:,0:2]

#Sets up name to be compared in text
tickers["Comparable Name"] = tickers["Name"].str.split(' ').str[0].str.lower()
counter = 0
tickerDict = {}

#Filter for only letters
regex = re.compile('[^a-zA-Z ]')

#List of common words that people chat with that are also company name's first words
banned_words = ['on','go','next','fat','love','main','nice','the','up','new','big','first','two','old','rh','red','whole','under','home','dollar','ready','world','bank',
                'virgin','national','gee','hope','second','rocket','safe','general','a','k','m','dd']

#Checks if it is the weekend
if date.today().weekday() >= 5:
    pass
else:
    #Searches Daily Discussions for stock tickers
    # Ex. If today was thursday, then it would take the "Daily Discussion thread for thursday" and "What are your moves tomorrow, thursday"
    for submission in reddit.subreddit('wallstreetbets').search('flair:"Daily Discussion"',sort = 'new',limit = 2,syntax='lucene'):

        submission.comments.replace_more(limit = None)
        
        for comment in submission.comments.list():
            splitComment = regex.sub('',str(comment.body))
            splitComment = splitComment.split(' ')
            
            for word in splitComment:
                    if word.lower() in banned_words:
                        pass
                    elif word in tickerDict or word.lower() in tickerDict:
                        if word not in tickerDict:
                            tickerDict[word] = 0
                        tickerDict[word] += 1
                    else:
                        tickerDict[word.lower()] = 1
                        tickerDict[word] = 1
    #Searches all hot posts for stock tickers
    for submission in reddit.subreddit('wallstreetbets').hot(limit = None):
        splitTitle = regex.sub('',str(submission.title))
        splitTitle = splitTitle.split(' ')

        for word in splitTitle:
        
            if word.lower() in banned_words:
                    pass
            elif word in tickerDict or word.lower() in tickerDict:
                if word not in tickerDict:
                    tickerDict[word] = 0
                tickerDict[word] += 1
            else:
                tickerDict[word.lower()] = 1
                tickerDict[word] = 1

    #Creates Dataframe for the tickers found
    tickerCounter_df = pd.DataFrame.from_dict(list(tickerDict.items())).rename(columns = {0:"Symbol",1:"Frequency"})
    final_ticker_df = pd.merge(tickers,tickerCounter_df, on ="Symbol")

    #Adds the times the name of company was mentioned, not just the ticker
    tickerCounter_df2 = pd.DataFrame.from_dict(list(tickerDict.items())).rename(columns = {0:"Comparable Name",1:"Frequency2"})
    final_ticker_df = pd.merge(final_ticker_df,tickerCounter_df2, on = "Comparable Name")

    #Data wrangling to finalize DF
    final_ticker_df['Frequency'] = final_ticker_df['Frequency'] + final_ticker_df['Frequency2']
    final_ticker_df = final_ticker_df.drop(['Frequency2'],axis = 1)
    final_ticker_df = final_ticker_df.drop(['Comparable Name'],axis = 1)
    final_ticker_df = final_ticker_df.sort_values(by = "Frequency", ascending = False, ignore_index = True)

    #Save data with date stamp
    filename = '\\' + str(date.today()) + '_stocks.csv'
    final_ticker_df.to_csv(r'C:\Users\djntr\StockPredictor\Stock_Predictor' + filename ,index=False)
    print(final_ticker_df.head(20))


