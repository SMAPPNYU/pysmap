import os
import unittest

from datetime import datetime
from test.config import config
from pysmap import SmappCollection
from pysmap import plots

class TestPlots(unittest.TestCase):

    def test_control(self):
        self.assertTrue(True)

    def test_tweet_field_grouped_by_timeslice_hours(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            if '#JadeHelm' in tweet['text']:
                return True
            return False
        plots.bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, 'hours', datetime(2015,9,1), datetime(2015,11,30), output_path)

    def test_tweet_field_grouped_by_timeslice_days(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            return True
        plots.bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, 'days', datetime(2015,9,1), datetime(2015,11,30), output_path)

    def test_tweet_field_grouped_by_timeslice_weeks(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            return True
        plots.bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, 'weeks', datetime(2015,9,1), datetime(2015,11,30), output_path)

    def test_tweet_field_grouped_by_timeslice_months(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            return True
        plots.bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, 'months', datetime(2015,9,1), datetime(2015,11,30), output_path)

    def test_tweet_field_grouped_by_timeslice_years(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            return True
        plots.bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, 'years', datetime(2015,9,1), datetime(2015,11,30), output_path)

    def test_tweet_field_grouped_by_timeslice_custom_filter(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            if '#JadeHelm' in tweet['text']:
                return True
            return False
        plots.bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, 'days', datetime(2015,9,1), datetime(2015,11,30), output_path)

    def test_tweet_field_grouped_by_timeslice_single_level_field(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            return True
        plots.bar_graph_tweet_field_grouped_by_period(collection, 'id_str', ['661283295670493185'], custom_filter, 'months', datetime(2015,9,1), datetime(2015,11,30), output_path)

    def test_tweet_field_grouped_by_timeslice_compound_field(self):
        output_path = '{}/chart_tests/Bar-{}-bar.html'.format(os.path.dirname(os.path.realpath(__file__)), datetime.now())
        file_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), config['json']['valid'])
        collection = SmappCollection('json', file_path)
        def custom_filter(tweet):
            return True
        plots.bar_graph_tweet_field_grouped_by_period(collection, 'user.time_zone', ['Pacific Time (US & Canada)'], custom_filter, 'months', datetime(2015,9,1), datetime(2015,11,30), output_path)
