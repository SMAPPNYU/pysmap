import abc
import datetime
import smappdragon

class SmappCollection(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, data_source_type, **kwargs):
            # non mongo collection
            if key == 'filepath':
                if data_source_type == 'bson':
                    self.collection = smappdragon.BsonCollection(filepath)
                elif data_source_type == 'json':
                    self.collection = smappdragon.JsonCollection(filepath)
                elif data_source_type == 'csv':
                    self.collection = smappdragon.CsvCollection(filepath)
            # mongo collection
            elif data_source_type == 'mongo':
                self.collection = smappdragon.MongoCollection(
                    kwargs['host'],
                    kwargs['port'],
                    kwargs['user'],
                    kwargs['password'],
                    kwargs['database'],
                    kwargs['collection']
                )
            # some kinda error
            else:
                raise IOError('Could not find your input, it\'s mispelled or doesn\'t exist.')

    def get_tweets_containing(self, term):
        def tweet_contains_term(tweet):
            return term in tweet['text']
        self.collection.set_custom_filter(tweet_contains_term)
        return self

    def count_terms(self, term):
        def tweet_contains_term(tweet):
            return term in tweet['text']
        return sum(1 for tweet in self.collection.set_custom_filter(tweet_contains_term).get_iterator())

    def get_tweet_texts(self, term):
        self.collection.strip_tweets(['text'])
        return self

    def date_range(self, start, end):
        if type(start) is not datetime.date or type(end) is not datetime.date:
            raise ValueError('inputs to date_range must be python datetime.date objects')
        self.collection.set_filter({'timestamp': {'$gte': start, '$lt', end}})
        return self

