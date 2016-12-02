import os
import re
import abc
import glob
import random
import pymongo
import operator
import itertools
import smappdragon

from datetime import datetime
from pysmap.twitterutil.smapp_collection import SmappCollection
from langdetect import detect, lang_detect_exception, DetectorFactory
from stop_words import get_stop_words

class SmappDataset(object):
    def __init__(self, *args, **kwargs):
            input_servers_ports = {}
            self.collections = []
            for input_list_or_datasource in args:
                if type(input_list_or_datasource) is SmappCollection:
                    self.collections.append(input_list_or_datasource.collection)
                elif type(input_list_or_datasource) is type(self):
                    self.collections.extend(input_list_or_datasource.collections)
                else:
                    if input_list_or_datasource[0] == 'bson':
                        if 'file_pattern' == input_list_or_datasource[1]:
                            for path in glob.glob(os.path.expanduser(input_list_or_datasource[2])):
                                self.collections.append(smappdragon.BsonCollection(path))
                        else:
                            self.collections.append(smappdragon.BsonCollection(input_list_or_datasource[1]))
                    elif input_list_or_datasource[0] == 'json':
                        if 'file_pattern' == input_list_or_datasource[1]:
                            for path in glob.glob(os.path.expanduser(input_list_or_datasource[2])):
                                self.collections.append(smappdragon.JsonCollection(path))
                        else:
                            self.collections.append(smappdragon.JsonCollection(input_list_or_datasource[1]))
                    elif input_list_or_datasource[0] == 'csv':
                        if 'file_pattern' == input_list_or_datasource[1]:
                            for path in glob.glob(os.path.expanduser(input_list_or_datasource[2])):
                                self.collections.append(smappdragon.CsvCollection(path))
                        else:
                            self.collections.append(smappdragon.CsvCollection(input_list_or_datasource[1]))
                    elif input_list_or_datasource[0] == 'mongo':
                        # we make one connection for each unique server/port pair the user provided
                        host_port_key = input_list_or_datasource[1]+str(input_list_or_datasource[2])
                        if host_port_key not in input_servers_ports:
                            new_connection = pymongo.MongoClient(input_list_or_datasource[1], int(input_list_or_datasource[2]))
                            input_servers_ports[host_port_key] = new_connection
                        if 'database_regex' in kwargs or 'collection_regex' in kwargs:
                            mongo = pymongo.MongoClient(input_list_or_datasource[1], int(input_list_or_datasource[2]))
                            if 'database_regex' in kwargs:
                                db_regex = re.compile(kwargs['database_regex'])
                                matched_dbs = [match.group(1) for db_name in mongo.database_names() for match in [db_regex.search(db_name)] if match]
                            else:
                                matched_dbs = [input_list_or_datasource[5]]

                            for matched_db in matched_dbs:
                                if 'collection_regex' in kwargs:
                                    collection_regex = re.compile(kwargs['collection_regex'])
                                    matched_collections = [match.group(1) for collection_name in mongo[matched_db].collection_names() for match in [collection_regex.search(collection_name)] if match]
                                else:
                                    if len(input_list_or_datasource) > 6:
                                        matched_collections = [input_list_or_datasource[6]]
                                    else:
                                        matched_collections = [input_list_or_datasource[5]]
                                for matched_collection in matched_collections:
                                    self.collections.append(smappdragon.MongoCollection(
                                        input_list_or_datasource[3],
                                        input_list_or_datasource[4],
                                        matched_db,
                                        matched_collection,
                                        passed_mongo=input_servers_ports[input_list_or_datasource[1]+str(input_list_or_datasource[2])]
                                    ))
                        else:
                            self.collections.append(smappdragon.MongoCollection(
                                input_list_or_datasource[3],
                                input_list_or_datasource[4],
                                input_list_or_datasource[5],
                                input_list_or_datasource[6],
                                passed_mongo=input_servers_ports[input_list_or_datasource[1]+str(input_list_or_datasource[2])]
                            ))
                    else:
                        raise IOError('Could not find your input: {}, it\'s mispelled or doesn\'t exist.'.format(input_list_or_datasource))

    #simple helper method for getting the iterators out
    #of all collections in a SmappDataset
    def get_collection_iterators(self):
        return itertools.chain(*[collection.get_iterator() for collection in self.collections])

    # helper applies filters to all collections in dataset
    def apply_filter_to_collections(self, filter_to_set):
        self.collections = [collection.set_custom_filter(filter_to_set) for collection in self.collections]

    def __iter__(self):
        for tweet in self.get_collection_iterators():
            yield tweet

    def get_tweet_texts(self):
        for tweet in self.get_collection_iterators():
            yield tweet['text']

    def count_tweets(self):
        return sum(1 for tweet in self.get_collection_iterators())

    def count_tweet_terms(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        self.apply_filter_to_collections(tweet_contains_terms)
        return sum(1 for tweet in self.get_collection_iterators())

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

    def find_date_range(self):
        date_min = datetime.max
        date_max = datetime.min
        for tweet in self.collection.get_collection_iterators():
            date_to_process = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            if date_to_process <= date_min:
                date_min = date_to_process
            if date_to_process >= date_max:
                date_max = date_to_process
        return {"date_min":date_min,"date_max":date_max}

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
            return 'retweeted_status' not in tweet
        self.apply_filter_to_collections(tweet_is_not_retweet)
        return self

    def get_retweets(self):
        def tweet_is_retweet(tweet):
            return 'retweeted_status' in tweet
        self.apply_filter_to_collections(tweet_is_retweet)
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

        for tweet in self.get_collection_iterators():
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

    def dump_to_bson(self, output_file, parallel=False):
        for i, collection in enumerate(self.collections):
            if parallel:
                filename, file_extension = output_file.split(os.extsep, 1)
                collection.dump_to_bson('{}_{}.{}'.format(filename, i, file_extension))
            else:
                collection.dump_to_bson(output_file)

    def dump_to_json(self, output_file, parallel=False):
        for i, collection in enumerate(self.collections):
            if parallel:
                filename, file_extension = output_file.split(os.extsep, 1)
                collection.dump_to_json('{}_{}.{}'.format(filename, i, file_extension))
            else:
                collection.dump_to_json(output_file)

    def dump_to_csv(self, output_file, keep_fields, parallel=False):
        for i, collection in enumerate(self.collections):
            if parallel:
                filename, file_extension = output_file.split(os.extsep, 1)
                collection.dump_to_csv('{}_{}.{}'.format(filename, i, file_extension), keep_fields)
            else:
                collection.dump_to_csv(output_file, keep_fields, write_header=(i == 0))

    def dump_to_sqlite_db(self, output_file, keep_fields, parallel=False):
        for i, collection in enumerate(self.collections):
            if parallel:
                filename, file_extension = output_file.split(os.extsep, 1)
                collection.dump_to_sqlite_db('{}_{}.{}'.format(filename, i, file_extension), keep_fields)
            else:
                collection.dump_to_sqlite_db(output_file, keep_fields)

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
        for tweet in self.get_collection_iterators():
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
        it = iter(self.get_collection_iterators())
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