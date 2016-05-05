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

if __name__ == '__main__':
    unittest.main()
