import abc
import smappdragon

from datetime import datetime

class SmappCollection(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, data_source_type, *args):
            # non mongo collection
            if data_source_type == 'bson':
                self.collection = smappdragon.BsonCollection(args[0])
            elif data_source_type == 'json':
                self.collection = smappdragon.JsonCollection(args[0])
            elif data_source_type == 'csv':
                self.collection = smappdragon.CsvCollection(args[0])
            # mongo collection
            elif data_source_type == 'mongo':
                self.collection = smappdragon.MongoCollection(
                    args[0],
                    args[1],
                    args[2],
                    args[3],
                    args[4],
                    args[5]
                )
            # some kinda error
            else:
                raise IOError('Could not find your input, it\'s mispelled or doesn\'t exist.')

    def __iter__(self):
        for tweet in self.collection.get_iterator():
            yield tweet

    def get_tweet_texts(self):
        for tweet in self.collection.get_iterator():
            yield tweet['text']

    def count_tweet_terms(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        return sum(1 for tweet in self.collection.set_custom_filter(tweet_contains_terms).get_iterator())

    def get_tweets_containing(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        self.collection.set_custom_filter(tweet_contains_terms)
        return self

    def get_date_range(self, start, end):
        if type(start) is not datetime or type(end) is not datetime:
            raise ValueError('inputs to date_range must be python datetime.date objects')
        def tweet_is_in_date_range(tweet):
            return datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') >= start and datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') < end
        self.collection.set_custom_filter(tweet_is_in_date_range)
        return self

    def tweet_language_is(self, language_code):
        def language_in_tweet(tweet):
            return language_code in tweet['lang']
        self.collection.set_custom_filter(language_in_tweet)
        return self

    def user_language_is(self, language_code):
        def language_in_tweet(tweet):
            return language_code in tweet['user']['lang']
        self.collection.set_custom_filter(language_in_tweet)
        return self

    def exclude_retweets(self):
        def tweet_is_not_retweet(tweet):
            return 'retweeted_status' in tweet
        self.collection.set_custom_filter(tweet_is_not_retweet)
        return self

    def tweets_with_user_location(self, place_term):
        def user_has_location(tweet):
            return tweet['user']['location'] and place_term in tweet['user']['location']
        self.collection.set_custom_filter(user_has_location)
        return self

    def get_geo_enabled(self):
        def geo_enabled_filter(tweet):
            return ("coordinates" in tweet 
                and tweet["coordinates"] is not None 
                and "coordinates" in tweet["coordinates"])
        self.collection.set_custom_filter(geo_enabled_filter)
        return self

    def get_non_geo_enabled(self):
        def non_geo_enabled_filter(tweet):
            return 'coordinates' not in tweet or \
                tweet['coordinates'] is None or \
                'coordinates' not in tweet['coordinates']
        self.collection.set_custom_filter(non_geo_enabled_filter)
        return self

    def limit_number_of_tweets(self, limit):
        self.collection.set_limit(limit)
        return self

    def dump_to_bson(self, output_file):
        self.collection.dump_to_bson(output_file)

    def dump_to_json(self, output_file):
        self.collection.dump_to_json(output_file)

    def dump_to_csv(self, output_file, keep_fields):
        self.collection.dump_to_csv(output_file, keep_fields)

    def get_top_hashtags(self, num_top):
        return self.collection.top_entities({'hashtags':num_top})

    def get_top_urls(self, num_top):
        return self.collection.top_entities({'urls':num_top})

    def get_top_mentions(self, num_top):
        return self.collection.top_entities({'user_mentions':num_top})

    def get_top_media(self, num_top):
        return self.collection.top_entities({'media':num_top})

    def get_top_symbols(self, num_top):
        return self.collection.top_entities({'symbols':num_top})
'''
author @yvan
for a lower level set of tools see: https://github.com/SMAPPNYU/smappdragon
'''