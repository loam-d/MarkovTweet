from markovtweet import *

api = create_api('config.json')

trump_mc = Markov_Chain()

for status in tweepy.Cursor(api.user_timeline, id = 'realDonaldTrump').items(5):
    print(tokenize(status.text))

trump_mc.train_on_tweets(api,['realDonaldTrump','kanyewest'],500)

print trump_mc.generate_tweet('The')