import abc
import operator
import smappdragon

from datetime import datetime
from langdetect import detect, lang_detect_exception, DetectorFactory
from stop_words import get_stop_words

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
            return (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') >= start) and (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') < end)
        self.collection.set_custom_filter(tweet_is_in_date_range)
        return self

    def tweet_language_is(self, *args):
        def language_in_tweet(tweet):
            return  any([language_code in tweet['lang'] for language_code in args])
        self.collection.set_custom_filter(language_in_tweet)
        return self

    def detect_tweet_language(self, *args):
        DetectorFactory.seed = 0
        def language_in_tweet(tweet):
            detected_lang = None
            try: 
                detected_lang = detect(tweet['text'])             
            except lang_detect_exception.LangDetectException:
                pass
            return  any([detected_lang in args])
        self.collection.set_custom_filter(language_in_tweet)
        return self

    def user_language_is(self, *args):
        def language_in_tweet(tweet):
            return any([language_code in tweet['user']['lang'] for language_code in args])
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
            return ('coordinates' not in tweet or
                tweet['coordinates'] is None or
                'coordinates' not in tweet['coordinates'])
        self.collection.set_custom_filter(non_geo_enabled_filter)
        return self

    def get_top_entities(self, requested_entities):
        returndict = {}
        returnstructure = {}
        tweet_parser = smappdragon.TweetParser()
        #init dempty dict for all entity types
        for entity_type in requested_entities:
            returndict[entity_type] = {}

        for tweet in self.collection.get_iterator():
            for entity_type in requested_entities:
                for entity in tweet_parser.get_entity(entity_type, tweet):
                    if entity_type == 'user_mentions':
                        entity_value = tweet_parser.get_entity_field('id_str', entity)
                    elif entity_type == 'hashtags' or entity_type == 'symbols':
                        entity_value = tweet_parser.get_entity_field('text', entity)
                    else:
                        entity_value = tweet_parser.get_entity_field('url', entity)

                    if entity_value in returndict[entity_type]:
                        returndict[entity_type][entity_value] += 1
                    else:
                        returndict[entity_type][entity_value] = 1

        for entity_type in returndict:
            returnstructure[entity_type] = {}
            if len(returndict[entity_type]) > 0:
                sorted_list = sorted(returndict[entity_type].items(), key=operator.itemgetter(1), reverse=True)
                # if the user put in 0 return all entites
                # otherwise slice the array and return the
                # number of top things they asked for
                # if the list is too short throw in None
                if requested_entities[entity_type] == 0:
                    returnstructure[entity_type] = {name: count for name, count in sorted_list}
                elif len(sorted_list) < requested_entities[entity_type]:
                    returnstructure[entity_type] = {name: count for name, count in sorted_list}
                    for i in range(0, requested_entities[entity_type]-len(sorted_list)):
                        returnstructure[entity_type][i] = None
                else:
                    returnstructure[entity_type] = { \
                        name: count for name, count in sorted_list[0:requested_entities[entity_type]] \
                    }
        return returnstructure

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
        return self.get_top_entities({'hashtags':num_top})

    def get_top_urls(self, num_top):
        return self.get_top_entities({'urls':num_top})

    def get_top_mentions(self, num_top):
        return self.get_top_entities({'user_mentions':num_top})

    def get_top_media(self, num_top):
        return self.get_top_entities({'media':num_top})

    def get_top_symbols(self, num_top):
        return self.get_top_entities({'symbols':num_top})

    def get_top_terms(self, num_top, stop_words=None):
        term_counts = {}
        if not stop_words:
            stop_words = get_stop_words('en')
        for tweet in self.collection.get_iterator():
            split_tweet = tweet['text'].split()
            for tweet_token in split_tweet:
                if tweet_token not in stop_words:
                    term_counts[tweet_token] = 0 if tweet_token not in term_counts else term_counts[tweet_token]+1
        sorted_counts = sorted(term_counts.items(), key=operator.itemgetter(1), reverse=True)[:num_top]
        return_counts = {}
        for k, v in sorted_counts:
            return_counts[k] = v
        return return_counts

'''
author @yvan
for a lower level set of tools see: https://github.com/SMAPPNYU/smappdragon
'''