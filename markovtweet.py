import tweepy
import json
import re
import time
import random


def create_api(config_filename):
    """
    Creates an authorized tweepy API object given a config file containing
    appropriate twitter application keys

    :param config_filename: string containing the config filename
    :return: the tweepy API object associated with the authorized twitter
        application
    """
    with open(config_filename) as api_keys:
        keys = json.load(api_keys)['twitter']

    api_key = keys['API Key']
    secret_key = keys['API Secret']
    access_tok = keys['Access Token']
    access_tok_sec = keys['Access Token Secret']

    auth = tweepy.OAuthHandler(api_key,secret_key)
    auth.set_access_token(access_tok, access_tok_sec)
    api = tweepy.API(auth)

    return api


def limit_handled(cursor):
    """
    Function to handle api call limits.  When limit is reached, the function
    will wait 15 minutes before iterating.  From Tweepy website

    :param cursor:
    :return:
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


def tokenize(tweet):
    """
    Uses regular expressions to tokenize tweets

    :param tweet: the text of a given tweet
    :return: the tokenization of that tweet as a list
    """
    emoticons_str = r"""
        (?:
            [:=;] #
            [oO\-]?
            [D\)\]\(\]/\\OpP]
        )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]

    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

    return tokens_re.findall(tweet)


class Markov_Chain:

    def __init__(self):
        self.mc = {}

    class Probability_Distribution:

        def __init__(self):
            self.dist = {}
            self.total = 0


        def pick(self):
            """
            Randomly returns a random token given the current distribution

            :return: a random token from the distribution
            """
            randnum = random.randrange(self.total)
            currDex = 0
            for token in self.dist:
                currCnt = self.dist[token]
                if randnum < currCnt + currDex:
                    return token
                currDex += currCnt



        def update(self, token):
            """
            Increment the probability of encountering a certain token

            :param token: a string containing the token
            """
            if token in self.dist:
                self.dist[token] += 1
            else:
                self.dist[token] = 1
            self.total += 1


    def update_markov_chain(self, tokens):
        """
        Updates the markov structure with a new tokenized tweet

        :param tokens: list of strings from tokenized tweet
        :return:
        """
        for i in range(1,len(tokens)):
            self.mc[tokens[i-1]].update(tokens[i])


    def train_on_tweets(self, api, ids, limit = -1):
        """
        Trains the given markov chain on the given twitter handles

        :param api: the authorized tweepy api object
        :param ids: list of ids you'd like to train on
        :param limit: limits the number of tweets, default no limit
        :return:
        """
        for user in ids:
            if (limit > 0):
                for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id = user).items(limit)):
                    self.update_markov_chain(tokenize(tweet))
            else:
                for tweet in limit_handled(tweepy.Cursor(api.user_timeline, id = user).items()):
                    self.update_markov_chain(tokenize(tweet))


    def save_markov_chain(self, filename):
        """
        Serializes a markov chain in a JSON file

        :param filename:
        """


    def load_markov_chain(self, filename):
        """

        :param filename:
        :return:
        """


    def generate_next_token(self, token):
        """

        :param token:
        :return:
        """
        return self.mc[token].pick()

    def generate_tweet(self, ):