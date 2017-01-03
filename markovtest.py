import unittest

from markovtweet import *


class MarkovTests(unittest.TestCase):

    def test_one_word(self):
        self.assertEqual(tokenize("Hello"), ['Hello'])

    def test_two_word(self):
        self.assertEqual(tokenize("Hello there"), ['Hello', 'there'])

    def test_punctuation(self):
        self.assertEqual(tokenize("Hello there!"), ['Hello', 'there', '!'])

    def test_hashtag(self):
        self.assertEqual(tokenize("#helloworld This is Jim"),
                         ["#helloworld", "This", "is", "Jim"])

    def test_emoticon(self):
        self.assertEqual(tokenize("Hi :D =-P ;p :o"),
                         ["Hi", ":D",  "=-P", ";p", ":o"])

    def test_atmention(self):
        self.assertEqual(tokenize("Hey @dude sup"), ["Hey", "@dude", "sup"])

    def test_htmltag(self):
        self.assertEqual(tokenize("<title>this is</title>"),
                         ["<title>", "this", "is", "</title>"])

    def test_URL(self):
        self.assertEqual(tokenize("Check this out: http://www.reddit.com"),
                         ["Check", "this", "out", ":", "http://www.reddit.com"])

    def test_contractions(self):
        self.assertEqual(tokenize("Don't stop the good-man!"),
                         ["Don't", "stop", "the", "good-man", "!"])

if __name__ == '__main__':
    unittest.main()
