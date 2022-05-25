# We will be using the tweepy library, which is a library that allows access to the twitter API

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# This will import the data from the twittercredentials file which stores the keys and tokens

import twittercredentials 

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt 

# ----- TWITTER CLIENT ----- #

class TwitterClient(): 

    # This method initialises the twitter client and API to be used throughout the program

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client
    
    # This method is used to create the search which lets the user search for a keyword through the twitter API
    
    def get_tweets(self, query, count = 10):
                
        fetched_tweets = self.twitter_client.search(q = query, count = count)
        return fetched_tweets

# ----- TWITTER AUTHENTICATOR ----- #

class TwitterAuthenticator():

    # This method authenticates the consumer tokens and access tokens so the program can have access to the twitter API

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
        auth.set_access_token(twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)
        return auth 

# ----- TWEET ANALYSIS ----- #

# This class will categorise and analyse the collected tweets

class TweetAnalyser():

    # This method is used for removing hyperlinks and stop words and make it into a readable form

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # This is the most important method as its the one which does the sentiment analysis

    def analyse_sentiment(self, tweets):

        # Analysis stores the tweets so it can be checked for sentiment analysis

        analysis = self.clean_tweet(tweets)
        
        # The positive and negative words are stored into seperate text files and they are then stored into lists using the following
        # commands and through file handling

        # Note!! file directories should be changed accordingly

        positive_words = open("/Users/oem/Desktop/university/Project/positivewords.txt").read().splitlines()
        negative_words = open("/Users/oem/Desktop/university/Project/negativewords.txt").read().splitlines()
        
        # The for loops are used to iterate through the lists and the tweets and checks if the words which are in the list are also
        # in the tweet, if a word from positive_words is in the tweet, then positive is returned. If its an item in negative_words,
        # then negative returned

        for i in positive_words:
            if i in analysis:
                return "Positive"
       
        for j in negative_words:
            if j in analysis:
                return "Negative"
            
    # This method extracts the text from the tweets and displays it in a readable form and stores it in a dataframe

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        # The analyse_sentiment method is called in this one and stores the value in the dataframe
        df['sentiment'] = np.array([tweet_analyser.analyse_sentiment(tweet) for tweet in df['tweets']])

        return df

# ----- MAIN PROGRAM ----- #

if __name__ == "__main__":

    # These variables are used to be able to get the total amount of positive and negative words so it can be displayed in a graph
            
    global positivecount
    global negativecount
    positivecount = 0
    negativecount = 0

    # The classes are called and stored in variables to be used in the main program

    twitter_client = TwitterClient()
    tweet_analyser = TweetAnalyser()

    api = twitter_client.get_twitter_client_api()

    # This is where the user inputs the keyword they want to search for

    search = input("Enter keyword for sentiment analysis: ")
    
    # This is a verification to make sure the user enters a valid integer as the input, if not it will loop until the user 
    # enters a correct input

    while True: 
        amount = input("How many tweets do you want to see? (Max 100): ")
        try:
            amount = int(amount)
            break 
        except ValueError: 
            print ("Invalid input! Please enter a number")

    # The class is called and gets the values that are input by the user 

    tweets = twitter_client.get_tweets(query = search, count = amount)

    # The analyser class is called and stored in the variable df

    df = tweet_analyser.tweets_to_data_frame(tweets)

    # This is the counter loop, it iterates through the tweets and if the sentiment is positive, it adds 1 to the positivecount variable,
    # and likewise for negative sentiments

    for i in range(0, len(tweets)):
        if df['sentiment'][i] == "Positive":
            positivecount += 1
        else:
            negativecount +=1
        
    # These print out the tweets along with the positive and negative count

    print(df.head(amount))
    print(f"Positive count = {positivecount}")
    print(f"Negative count = {negativecount}")

    # These lines are used to display a bar graph, it counts the values of positive and negative sentiment and displays it in
    # a bar graph

    ax = df['sentiment'].value_counts().plot(kind='bar',
                                    figsize=(14,8),
                                    color=['red','green'],
                                    title="Count of sentiment values for keyword")
    ax.set_xlabel("sentiment value")
    ax.set_ylabel("Count")

    plt.show()