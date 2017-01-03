from markovtweet import *

api = create_api('config.json')

for status in tweepy.Cursor(api.user_timeline, id = 'kanyewest').items(5):
    print(tokenize(status.text))
