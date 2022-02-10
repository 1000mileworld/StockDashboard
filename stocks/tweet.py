from tweepy import OAuthHandler, API
from decouple import config

CONSUMER_KEY = config('API')
CONSUMER_SECRET = config('API_SECRET')
BEARER_TOKEN = config('BEARER_TOKEN')
ACCESS_TOKEN = config('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
    def get_twitter_client_api(self):
        return self.twitter_client

api = TwitterClient().get_twitter_client_api()

def getTweetID(searchText, numTweets):
    tweets = api.search_tweets(q=searchText, count=numTweets)
    ids = []
    for tweet in tweets:
       #urls.append('https://twitter.com/twitter/statuses/'+tweet.id_str)
       ids.append(tweet.id_str) 
    return ids