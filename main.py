import tweepy
import json

with open('config.json') as api_keys:
    keys = json.load(api_keys)['twitter']

api_key = keys['API Key']
secret_key = keys['API Secret']
access_tok = keys['Access Token']
access_tok_sec = keys['Access Token Secret']

auth = tweepy.OAuthHandler(api_key,secret_key)
auth.set_access_token(access_tok, access_tok_sec)
api = tweepy.API(auth)

for status in tweepy.Cursor(api.user_timeline, id = 'kanyewest').items(4):
    print(status.text)

