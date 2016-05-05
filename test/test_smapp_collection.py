import os
import unittest

from test.config import config
from smappy import SmappCollection

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

if __name__ == '__main__':
    unittest.main()
