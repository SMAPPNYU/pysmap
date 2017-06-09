import os
import re
import csv
import abc
import copy
import glob
import random
import sqlite3
import pymongo
import operator
import itertools
import smappdragon

from datetime import datetime
from bson import BSON, json_util
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

    # simple helper method for getting the iterators out
    # of all collections in a SmappDataset, sample overrides
    # this method
    def get_collection_iterators(self):
        return itertools.chain(*[collection.get_iterator() for collection in self.collections])

    # helper applies filters to all collections in dataset
    def apply_filter_to_collections(self, filter_to_set):
        self.collections = [collection.set_custom_filter(filter_to_set) for collection in self.collections]

    def __iter__(self):
        for tweet in self.get_collection_iterators():
            yield tweet

    def set_custom_filter(self, custom_filter):
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(custom_filter)
        return cp

    def get_tweet_texts(self):
        for tweet in self.get_collection_iterators():
            yield tweet['text']

    def count_tweets(self):
        return sum(1 for tweet in self.get_collection_iterators())

    def count_tweet_terms(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(tweet_contains_terms)
        return sum(1 for tweet in cp.get_collection_iterators())

    def get_tweets_containing(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(tweet_contains_terms)
        return cp

    def get_date_range(self, start, end):
        if type(start) is not datetime or type(end) is not datetime:
            raise ValueError('inputs to date_range must be python datetime.date objects')
        def tweet_is_in_date_range(tweet):
            return (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') >= start) and (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') < end)
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(tweet_is_in_date_range)
        return cp

    def find_date_range(self):
        date_min = datetime.max
        date_max = datetime.min
        for tweet in self.get_collection_iterators():
            date_to_process = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            if date_to_process <= date_min:
                date_min = date_to_process
            if date_to_process >= date_max:
                date_max = date_to_process
        return {"date_min":date_min,"date_max":date_max}

    def tweet_language_is(self, *args):
        def language_in_tweet(tweet):
            return  any([language_code in tweet['lang'] for language_code in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(language_in_tweet)
        return cp

    def detect_tweet_language(self, *args):
        DetectorFactory.seed = 0
        def language_in_tweet(tweet):
            detected_lang = None
            try: 
                detected_lang = detect(tweet['text'])             
            except lang_detect_exception.LangDetectException:
                pass
            return  any([detected_lang in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(language_in_tweet)
        return cp

    def user_language_is(self, *args):
        def language_in_tweet(tweet):
            return any([language_code in tweet['user']['lang'] for language_code in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(language_in_tweet)
        return cp

    def exclude_retweets(self):
        def tweet_is_not_retweet(tweet):
            return 'retweeted_status' not in tweet
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(tweet_is_not_retweet)
        return cp

    def get_retweets(self):
        def tweet_is_retweet(tweet):
            return 'retweeted_status' in tweet
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(tweet_is_retweet)
        return cp

    def user_location_contains(self, *args):
        def user_has_location(tweet):
            return tweet['user']['location'] and any([place_term in tweet['user']['location'] for place_term in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(user_has_location)
        return cp

    def user_description_contains(self, *args):
        def user_description_contains_terms(tweet):
            return tweet['user']['description'] and any([d_term in tweet['user']['description'] for d_term in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(user_description_contains_terms)
        return cp

    def user_id_is(self, *args):
        def user_id_created_tweet(tweet):
            return tweet['user']['id'] and any([u_id == tweet['user']['id'] for u_id in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(user_id_created_tweet)
        return cp

    def get_geo_enabled(self):
        def geo_enabled_filter(tweet):
            return ("coordinates" in tweet 
                and tweet["coordinates"] is not None 
                and "coordinates" in tweet["coordinates"])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(geo_enabled_filter)
        return cp

    def get_non_geo_enabled(self):
        def non_geo_enabled_filter(tweet):
            return ('coordinates' not in tweet or
                tweet['coordinates'] is None or
                'coordinates' not in tweet['coordinates'])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(non_geo_enabled_filter)
        return cp

    def within_geobox(self, sw_lon, sw_lat, ne_lon, ne_lat):
        def tweet_is_in_geobox(tweet):
            if tweet['coordinates'] and tweet['coordinates']['coordinates']:
                coords = tweet['coordinates']['coordinates']
                return coords[0] > float(sw_lon) and coords[0] < float(ne_lon) and coords[1] > float(sw_lat) and coords[1] < float(ne_lat)
            return False
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(tweet_is_in_geobox)
        return cp

    def place_name_contains_country(self, *args):
        def place_name_contains_terms(tweet):
            return tweet['place'] and any([d_term in tweet['place']['country'] for d_term in args])
        cp = copy.deepcopy(self)
        cp.apply_filter_to_collections(place_name_contains_terms)
        return cp


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
        cp = copy.deepcopy(self)
        cp.collections = [collection.set_limit(limit) for collection in cp.collections]
        return cp

    def dump_to_bson(self, output_file, num_files=1):
        filehandles = [None]*num_files
        filename, file_extension = output_file.split(os.extsep, 1)

        # open all filehandles
        if num_files == 1:
            filehandles[0] = open(output_file, 'ab+')
        else:
            # open all filehandles
            filename, file_extension = output_file.split(os.extsep, 1)
            for i in range(num_files):
                filehandles[i] = open('{}_{}.{}'.format(filename, i, file_extension), 'ab+')

        # write the tweets as evenly 
        # as possible in each file
        tracker = 0 
        for tweet in self.get_collection_iterators():
            filehandles[tracker].write(BSON.encode(tweet))
            if tracker == num_files-1:
                tracker = 0
            else:
                tracker += 1

        # close all filehandles
        for fh in filehandles:
            fh.close()

    def dump_to_json(self, output_file, num_files=1):
        filehandles = [None]*num_files

        if num_files == 1:
            filehandles[0] = open(output_file, 'a')
        else:
            # open all filehandles
            filename, file_extension = output_file.split(os.extsep, 1)
            for i in range(num_files):
                filehandles[i] = open('{}_{}.{}'.format(filename, i, file_extension), 'a')

        # write the tweets as evenly 
        # as possible in each file
        tracker = 0 
        for tweet in self.get_collection_iterators():
            filehandles[tracker].write(json_util.dumps(tweet)+'\n')
            if tracker == num_files-1:
                tracker = 0
            else:
                tracker += 1

        # close all filehandles
        for fh in filehandles:
            fh.close()

    def dump_to_csv(self, output_file, input_fields, write_header=True, top_level=False, num_files=1):
        filehandles = [None]*num_files
        writers = [None]*num_files

        if num_files == 1:
            filehandles[0] = open(output_file, 'a', encoding='utf-8')
            writers[0] = csv.writer(filehandles[0])
            if write_header:
                writers[0].writerow(input_fields)
        else:
            # open all filehandles
            filename, file_extension = output_file.split(os.extsep, 1)
            for i in range(num_files):
                filehandles[i] = open('{}_{}.{}'.format(filename, i, file_extension), 'a')
                writers[i] = csv.writer(filehandles[i])
                if write_header:
                    writers[i].writerow(input_fields)

        tweet_parser = smappdragon.tools.tweet_parser.TweetParser()

                # write the tweets as evenly 
        # as possible in each file
        tracker = 0 
        for tweet in self.get_collection_iterators():
            if top_level:
                ret = list(zip(input_fields, [tweet.get(field) for field in input_fields]))
            else:
                ret = tweet_parser.parse_columns_from_tweet(tweet,input_fields)
            ret_values = [col_val[1] for col_val in ret]
            writers[tracker].writerow(ret_values)

            if tracker == num_files-1:
                tracker = 0
            else:
                tracker += 1

       # close all filehandles
        for fh in filehandles:
            fh.close()

    def dump_to_sqlite_db(self, output_file, input_fields, top_level=False, num_files=1):
        def replace_none(s):
            if s is None:
                return 'NULL'
            return s
        cons = [None]*num_files
        cursors = [None]*num_files

        tweet_parser = smappdragon.tools.tweet_parser.TweetParser()
        column_str = ','.join([column for column in input_fields]).replace('.','__')
        question_marks = ','.join(['?' for column in input_fields])

        con = sqlite3.connect(output_file)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS data ({});".format(column_str))

        insert_list = []
        # batch insert if more than 10k tweets
        for tweet in self.get_collection_iterators():
            if top_level:
                ret = list(zip(input_fields, [tweet.get(field) for field in input_fields]))
            else:
                ret = tweet_parser.parse_columns_from_tweet(tweet, input_fields)
            row = [replace_none(col_val[1]) for col_val in ret]
            insert_list.append(tuple(row))
            if (len(insert_list) % 10000) == 0:
                cur.executemany("INSERT INTO data ({}) VALUES ({});".format(column_str, question_marks), insert_list)
                con.commit()
                insert_list = []
        if len(insert_list) < 10000:
            cur.executemany("INSERT INTO data ({}) VALUES ({});".format(column_str, question_marks), insert_list)
            con.commit()
        con.close()

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
        def new_get_iterators():
            it = iter(self.get_collection_iterators())
            sample = list(itertools.islice(it, k))
            random.shuffle(sample)
            for i, item in enumerate(it, start=k+1):
                j = random.randrange(i)
                if j < k:
                    sample[j] = item
            for sample_value in sample:
                yield sample_value

        cp = copy.deepcopy(self)
        cp.get_collection_iterators = new_get_iterators
        return cp

'''
author @yvan
for a lower level set of tools see: https://github.com/SMAPPNYU/smappdragon
'''