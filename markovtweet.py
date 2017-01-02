import tweepy
import json

def create_api(config_filename):
    """
    Creates an authorized tweepy API object given a config file containing appropriate twitter application keys

    @param config_filename: string containing the config filename
    @return: the tweepy API object associated with the authorized twitter application
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