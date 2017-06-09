import csv
import abc
import copy
import random
import sqlite3
import operator
import itertools
import smappdragon

from datetime import datetime
from bson import BSON, json_util
from stop_words import get_stop_words
from langdetect import detect, lang_detect_exception, DetectorFactory

class SmappCollection(object):
    def __init__(self, data_source_type, *args):
            if data_source_type == 'bson':
                self.collection = smappdragon.BsonCollection(args[0])
            elif data_source_type == 'json':
                self.collection = smappdragon.JsonCollection(args[0])
            elif data_source_type == 'csv':
                self.collection = smappdragon.CsvCollection(args[0])
            elif data_source_type == 'mongo':
                self.collection = smappdragon.MongoCollection(
                    args[0],
                    args[1],
                    args[2],
                    args[3],
                    args[4],
                    args[5]
                )
            else:
                raise IOError('Could not find your input, it\'s mispelled or doesn\'t exist.')

    def __iter__(self):
        for tweet in self.collection.get_iterator():
            yield tweet

    def set_custom_filter(self, custom_filter):
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(custom_filter)
        return cp

    def get_tweet_texts(self):
        for tweet in self.collection.get_iterator():
            yield tweet['text']

    def count_tweets(self):
        return sum(1 for tweet in self.collection.get_iterator())

    def count_tweet_terms(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        cp = copy.deepcopy(self)
        return sum(1 for tweet in cp.collection.set_custom_filter(tweet_contains_terms).get_iterator())

    def get_tweets_containing(self, *args):
        def tweet_contains_terms(tweet):
            return any([term in tweet['text'] for term in args])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(tweet_contains_terms)
        return cp

    def get_date_range(self, start, end):
        if type(start) is not datetime or type(end) is not datetime:
            raise ValueError('inputs to date_range must be python datetime.date objects')
        def tweet_is_in_date_range(tweet):
            return (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') >= start) and (datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y') < end)
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(tweet_is_in_date_range)
        return cp

    def find_date_range(self):
        date_min = datetime.max
        date_max = datetime.min
        for tweet in self.collection.get_iterator():
            date_to_process = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            if date_to_process <= date_min:
                date_min = date_to_process
            if date_to_process >= date_max:
                date_max = date_to_process
        return {"date_min":date_min,"date_max":date_max}

    def tweet_language_is(self, *args):
        def language_in_tweet(tweet):
            return  any(['lang' in tweet and language_code in tweet['lang'] for language_code in args])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(language_in_tweet)
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
        cp.collection.set_custom_filter(language_in_tweet)
        return cp

    def user_language_is(self, *args):
        def language_in_tweet(tweet):
            return any([language_code in tweet['user']['lang'] for language_code in args])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(language_in_tweet)
        return cp

    def exclude_retweets(self):
        def tweet_is_not_retweet(tweet):
            return 'retweeted_status' not in tweet
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(tweet_is_not_retweet)
        return cp

    def get_retweets(self):
        def tweet_is_retweet(tweet):
            return 'retweeted_status' in tweet
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(tweet_is_retweet)
        return cp

    def user_location_contains(self, *args):
        def user_has_location(tweet):
            return tweet['user']['location'] and any([place_term in tweet['user']['location'] for place_term in args])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(user_has_location)
        return cp

    def user_description_contains(self, *args):
        def user_description_contains_terms(tweet):
            return tweet['user']['description'] and any([d_term in tweet['user']['description'] for d_term in args])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(user_description_contains_terms)
        return cp

    def user_id_is(self, *args):
        def user_id_created_tweet(tweet):
            return tweet['user']['id'] and any([u_id == tweet['user']['id'] for u_id in args])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(user_id_created_tweet)
        return cp

    def get_geo_enabled(self):
        def geo_enabled_filter(tweet):
            return ("coordinates" in tweet 
                and tweet["coordinates"] is not None 
                and "coordinates" in tweet["coordinates"])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(geo_enabled_filter)
        return cp

    def get_non_geo_enabled(self):
        def non_geo_enabled_filter(tweet):
            return ('coordinates' not in tweet or
                tweet['coordinates'] is None or
                'coordinates' not in tweet['coordinates'])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(non_geo_enabled_filter)
        return cp
        
    def within_geobox(self, sw_lon, sw_lat, ne_lon, ne_lat):
        def tweet_is_in_geobox(tweet):
            if tweet['coordinates'] and tweet['coordinates']['coordinates']:
                coords = tweet['coordinates']['coordinates']
                return coords[0] > float(sw_lon) and coords[0] < float(ne_lon) and coords[1] > float(sw_lat) and coords[1] < float(ne_lat)
            return False
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(tweet_is_in_geobox)
        return cp

    def place_name_contains_country(self, *args):
        def place_name_contains_terms(tweet):
            return tweet['place'] and any([d_term in tweet['place']['country'] for d_term in args])
        cp = copy.deepcopy(self)
        cp.collection.set_custom_filter(place_name_contains_terms)
        return cp

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
        cp = copy.deepcopy(self)
        cp.collection.set_limit(limit)
        return cp

    def dump_to_bson(self, output_file):
        filehandle = open(output_file, 'ab+')
        for tweet in self.collection.get_iterator():
            filehandle.write(BSON.encode(tweet))
        filehandle.close()

    def dump_to_json(self, output_file):
        filehandle = open(output_file, 'a')
        for tweet in self.collection.get_iterator():
            filehandle.write(json_util.dumps(tweet)+'\n')
        filehandle.close()
        
    def dump_to_csv(self, output_file, input_fields, write_header=True, top_level=False):
        filehandle = open(output_file, 'a', encoding='utf-8')
        writer = csv.writer(filehandle)
        if write_header:
            writer.writerow(input_fields)
        tweet_parser = smappdragon.tools.tweet_parser.TweetParser()

        for tweet in self.collection.get_iterator():
            if top_level:
                ret = list(zip(input_fields, [tweet.get(field) for field in input_fields]))
            else:
                ret = tweet_parser.parse_columns_from_tweet(tweet,input_fields)
            ret_values = [col_val[1] for col_val in ret]
            writer.writerow(ret_values)
        filehandle.close()

    def dump_to_sqlite_db(self, output_file, input_fields, top_level=False):
        def replace_none(s):
            if s is None:
                return 'NULL'
            return s

        tweet_parser = smappdragon.tools.tweet_parser.TweetParser()
        column_str = ','.join([column for column in input_fields]).replace('.','__')
        question_marks = ','.join(['?' for column in input_fields])

        con = sqlite3.connect(output_file)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS data ({});".format(column_str))

        insert_list = []
        # batch insert if more than 10k tweets
        for count,tweet in enumerate(self.collection.get_iterator()):
            if top_level:
                ret = list(zip(input_fields, [tweet.get(field) for field in input_fields]))
            else:
                ret = tweet_parser.parse_columns_from_tweet(tweet, input_fields)
            row = [replace_none(col_val[1]) for col_val in ret]
            insert_list.append(tuple(row))
            if (count % 10000) == 0:
                cur.executemany("INSERT INTO data ({}) VALUES ({});".format(column_str, question_marks), insert_list)
                con.commit()
                insert_list = []
        if count < 10000:
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
        '''
        this method is especially troublesome
        i do not reccommend making any changes to it
        you may notice it uplicates code fro smappdragon
        there is no way around this as far as i can tell
        it really  might screw up a lot of stuff, stip tweets
        has been purposely omitted as it isnt supported in pysmap
        '''
        def new_get_iterator():
            tweet_parser = smappdragon.TweetParser()
            it = iter(self.collection.get_iterator())
            sample = list(itertools.islice(it, k))
            random.shuffle(sample)
            for i, item in enumerate(it, start=k+1):
                j = random.randrange(i)
                if j < k:
                    sample[j] = item
            for tweet in sample:
                if self.collection.limit != 0 and self.collection.limit <= count:
                    return
                elif tweet_parser.tweet_passes_filter(self.collection.filter, tweet) \
                and tweet_parser.tweet_passes_custom_filter_list(self.collection.custom_filters, tweet):
                    yield tweet
        cp = copy.deepcopy(self)
        cp.collection.get_iterator = new_get_iterator
        return cp

'''
author @yvan
for a lower level set of tools see: https://github.com/SMAPPNYU/smappdragon
'''