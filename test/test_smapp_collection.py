import os
import unittest

from test.config import config
from pysmap import SmappCollection

class TestBaseCollection(unittest.TestCase):

    def test_control(self):
        self.assertTrue(True)

    def test_smapp_bson_collection_iterates(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	self.assertTrue(len(list(collection)) > 0)

    def test_smapp_json_collection_iterates(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
    	collection = SmappCollection('json', file_path)
    	self.assertTrue(len(list(collection)) > 0)

    def test_smapp_csv_collection_iterates(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['csv']['valid'])
    	collection = SmappCollection('csv', file_path)
    	self.assertTrue(len(list(collection)) > 0)

    # limit before mongo because mongo should be limited or it takes too long
    def test_limit_number_of_tweets(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	self.assertTrue(len(list(collection.limit_number_of_tweets(100))) > 0)

    def test_smapp_mongo_collection_iterates(self):
    	collection = SmappCollection('mongo', 
    		config['mongo']['host'], 
    		config['mongo']['port'], 
    		config['mongo']['user'], 
    		config['mongo']['password'],
    		config['mongo']['database'],
    		config['mongo']['collection'])
    	self.assertTrue(len(list(collection.limit_number_of_tweets(100))) > 0)

    def test_get_tweet_texts(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	texts = [text for text in collection.limit_number_of_tweets(1).get_tweet_texts()]
    	self.assertEqual(str, type(texts[0]))

    def test_count_tweet_terms(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = collection.count_tweet_terms('jade')
    	self.assertEqual(167, count)

    def test_get_tweets_containing(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = len([tweet for tweet in collection.get_tweets_containing('jade')])
    	self.assertEqual(167, count)

    def test_get_date_range(self):
    	pass

    def test_tweet_language_is(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = len([tweet for tweet in collection.tweet_language_is('en')])
    	self.assertEqual(825, count)

    def test_user_language_is(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = len([tweet for tweet in collection.user_language_is('en')])
    	self.assertEqual(801, count)

    def test_exclude_retweets(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = len([tweet for tweet in collection.exclude_retweets()])
    	self.assertEqual(505, count)

    def test_tweets_with_user_location(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = len([tweet for tweet in collection.tweets_with_user_location('TX')])
    	self.assertEqual(10, count)

    def test_get_geo_enabled(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = len([tweet for tweet in collection.get_geo_enabled()])
    	self.assertEqual(1, count)

    def test_get_non_geo_enabled(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	count = len([tweet for tweet in collection.get_non_geo_enabled()])
    	self.assertEqual(1186, count)

    def test_get_top_hashtags(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	base_hashtags = {'hashtags': {'2a': 26, 'pjnet': 26, 'jadehelm': 111, 'falseflag': 32, 'JadeHelm': 118}}
    	hashtags = collection.get_top_hashtags(5)
    	self.assertTrue(set(hashtags.keys()) == set(base_hashtags.keys()))

    def test_get_top_urls(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	urls = collection.get_top_urls(5)
    	base_urls = {'urls': {'https://t.co/ATzXpRciyr': 18, 'https://t.co/dpz7vZ1JWy': 39, 'https://t.co/l9OEuvRlt8': 24, 'https://t.co/nkc4hnukLX': 21, 'https://t.co/rsNUItS48U': 60}}
    	self.assertTrue(set(urls.keys()) == set(base_urls.keys()))

    def test_get_top_mentions(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	top_mentions = collection.get_top_mentions(5)
    	base_top_mentions = {'user_mentions': {'233498836': 58, '27234909': 56, '10228272': 75, '1619936671': 41, '733417892': 121}}
    	self.assertTrue(set(top_mentions.keys()) == set(base_top_mentions.keys()))

    def test_get_top_media(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	top_media = collection.get_top_media(5)
    	base_top_media = {'media': {'https://t.co/pAfigDPcNc': 27, 'https://t.co/MaOGn6wH40': 17, 'https://t.co/TH8TmGuYww': 24, 'https://t.co/YpqDPqA2UO': 14, 'https://t.co/ORaTXOM2oX': 55}}
    	self.assertTrue(set(top_media.keys()) == set(base_top_media.keys()))

    def test_get_top_symbols(self):
    	file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['bson']['valid'])
    	collection = SmappCollection('bson', file_path)
    	top_symbols = collection.get_top_symbols(5)
    	base_top_symbols = {'symbols': {0: None, 'hould': 1, 2: None, 3: None, 1: None}}
    	self.assertTrue(set(top_symbols.keys()) == set(base_top_symbols.keys()))

if __name__ == '__main__':
    unittest.main()
