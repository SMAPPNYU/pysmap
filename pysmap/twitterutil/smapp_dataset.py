import abc
import random
import operator
import itertools
import smappdragon

from datetime import datetime
from langdetect import detect, lang_detect_exception, DetectorFactory
from stop_words import get_stop_words

class SmappDataset(object):
    def __init__(self, *args, **kwargs):
            self.collections = []
            for input_list in args:
                if 'collection_regex' in kwargs:
                    input_list[1] = kwargs['collection_regex']

                if input_list[0] == 'bson':
                    self.collections.append(smappdragon.BsonCollection(input_list[1]))
                elif input_list[0] == 'json':
                    self.collections.append(smappdragon.JsonCollection(input_list[1]))
                elif input_list[0] == 'csv':
                    self.collections.append(smappdragon.CsvCollection(input_list[1]))
                elif input_list[0] == 'mongo':
                    if 'collection_regex' in kwargs:
                        input_list[5] = kwargs['collection_regex']
                    if 'database_regex' in kwargs:
                        input_list[4] = kwargs['database_regex']
                    self.collections.append(smappdragon.MongoCollection(
                        input_list[0],
                        input_list[1],
                        input_list[2],
                        input_list[3],
                        input_list[4],
                        input_list[5]
                    ))
                else:
                    raise IOError('Could not find your input: {}, it\'s mispelled or doesn\'t exist.'.format(input_list))

    #simple helper method for getting the iterators out
    #of all collections in a SmappDataset
    def get_collection_iterators(self):
        return itertools.chain(*[collection.get_iterator() for collection in self.collections])

    def apply_filter_to_collections(self, filter_to_set):
        self.collections = [collection.set_custom_filter(filter_to_set) for collection in self.collections]

    def __iter__(self):
        for tweet in get_collection_iterators():
            yield tweet

    def get_tweet_texts(self):
        for tweet in get_collection_iterators():
            yield tweet['text']

    def count_tweets(self):
        return sum(1 for tweet in get_collection_iterators())

    def count_tweet_terms(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        self.apply_filter_to_collections(tweet_contains_terms)
        return sum(1 for tweet in get_collection_iterators())

    def get_tweets_containing(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        self.apply_filter_to_collections(tweet_contains_terms)
        return self

    def get_date_range(self, start, end):
        if type(start) is not datetime or type(end) is not datetime:
            raise ValueError('inputs to date_range must be python datetime.date objects')
        def tweet_is_in_date_range(tweet):
            return (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') >= start) and (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') < end)
        self.apply_filter_to_collections(tweet_is_in_date_range)
        return self

    def tweet_language_is(self, *args):
        def language_in_tweet(tweet):
            return  any([language_code in tweet['lang'] for language_code in args])
        self.apply_filter_to_collections(language_in_tweet)
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
        self.apply_filter_to_collections(language_in_tweet)
        return self

    def user_language_is(self, *args):
        def language_in_tweet(tweet):
            return any([language_code in tweet['user']['lang'] for language_code in args])
        self.apply_filter_to_collections(language_in_tweet)
        return self

    def exclude_retweets(self):
        def tweet_is_not_retweet(tweet):
            return 'retweeted_status' in tweet
        self.apply_filter_to_collections(tweet_is_not_retweet)
        return self

    def tweets_with_user_location(self, place_term):
        def user_has_location(tweet):
            return tweet['user']['location'] and place_term in tweet['user']['location']
        self.apply_filter_to_collections(user_has_location)
        return self

    def get_geo_enabled(self):
        def geo_enabled_filter(tweet):
            return ("coordinates" in tweet 
                and tweet["coordinates"] is not None 
                and "coordinates" in tweet["coordinates"])
        self.apply_filter_to_collections(geo_enabled_filter)
        return self

    def get_non_geo_enabled(self):
        def non_geo_enabled_filter(tweet):
            return ('coordinates' not in tweet or
                tweet['coordinates'] is None or
                'coordinates' not in tweet['coordinates'])
        self.apply_filter_to_collections(non_geo_enabled_filter)
        return self

    def get_top_entities(self, requested_entities):
        returndict = {}
        returnstructure = {}
        tweet_parser = smappdragon.TweetParser()
        #init dempty dict for all entity types
        for entity_type in requested_entities:
            returndict[entity_type] = {}

        for tweet in get_collection_iterators():
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
        self.collections = [collection.set_limit(limit) for collection in self.collections]
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

    def sample(self, k):
        it = iter(self.collection.get_iterator())
        sample = list(itertools.islice(it, k))
        random.shuffle(sample)
        for i, item in enumerate(it, start=k+1):
            j = random.randrange(i)
            if j < k:
                sample[j] = item
        for sample_value in sample:
            yield sample_value
'''
author @yvan
for a lower level set of tools see: https://github.com/SMAPPNYU/smappdragon
'''