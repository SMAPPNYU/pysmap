import os
import unittest
import networkx as nx

from datetime import datetime
from test.config import config
from pysmap import SmappCollection
from pysmap import networks

class TestNetworks(unittest.TestCase):

    def test_control(self):
        self.assertTrue(True)

    def test_make_retweet_network_graph(self):
        output_path = '{}/chart_tests/network-{}-retweet.graphml'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        digraph = networks.retweet_network(collection, ['id_str', 'retweeted_status.id_str', 'timestamp', 'text', 'lang'], ['id_str', 'screen_name', 'location', 'description'])
        nx.write_graphml(digraph, output_path)

    def test_empty_make_retweet_network_graph(self):
        output_path = '{}/chart_tests/network-{}-retweet-empty.graphml'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        digraph = networks.retweet_network(collection, [], [])
        nx.write_graphml(digraph, output_path)