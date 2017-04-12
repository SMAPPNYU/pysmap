```
 _ __  _   _ ___ _ __ ___   __ _ _ __
| '_ \| | | / __| '_ ` _ \ / _` | '_ \
| |_) | |_| \__ \ | | | | | (_| | |_) |
| .__/ \__, |___/_| |_| |_|\__,_| .__/
|_|    |___/                    |_|
```

[![PyPI](https://img.shields.io/pypi/v/pysmap.svg)](https://pypi.python.org/pypi/pysmap) [![PyPI](https://img.shields.io/pypi/l/pysmap.svg)](https://github.com/SMAPPNYU/pysmap/blob/master/LICENSE)

:snake: pysmap is a high level toolkit for dealing with twitter data it also has a higher level interface for [smappdragon](https://github.com/SMAPPNYU/smappdragon). it has functionality from the old toolkit and functionality from our old util library smappPy.
- [twitterutil](#twitterutil)
    - [smapp_dataset](#smapp_dataset)
    - [smapp_collection](#smapp_collection)
        - [set_custom_filter](#set_custom_filter)
        - [get_tweets_containing](#get_tweets_containing)
        - [get_top_terms](#get_top_terms)
        - [get_tweet_texts](#get_tweet_texts)
        - [get_date_range](#get_date_range)
        - [get_geo_enabled](#get_geo_enabled)
        - [get_non_geo_enabled](#get_non_geo_enabled)
        - [get_top_entities](#get_top_entities)
        - [get_top_hashtags](#get_top_hashtags)
        - [get_top_urls](#get_top_urls)
        - [get_top_mentions](#get_top_mentions)
        - [get_top_media](#get_top_media)
        - [get_top_symbols](#get_top_symbols)
        - [find_date_range](#find_date_range)
        - [count_tweet_terms](#count_tweet_terms)
        - [count_tweets](#count_tweets)
        - [exclude_retweets](#exclude_retweets)
        - [get_retweets](#get_retweets)
        - [user_location_contains](#user_location_contains)
        - [user_description_contains](#user_description_contains)
        - [place_name_contains_country](#place_name_contains_country)
        - [within_geobox](#within_geobox)
        - [limit_number_of_tweets](#limit_number_of_tweets)
        - [tweet_language_is](#tweet_language_is)
        - [detect_tweet_language](#detect_tweet_language)
        - [user_language_is](#user_language_is)
        - [sample](#sample)
        - [dump_to_bson](#dump_to_bson)
        - [dump_to_json](#dump_to_json)
        - [dump_to_csv](#dump_to_csv)
        - [dump_to_sqlite_db](#dump_to_sqlite_db)
- [viz](#viz)
    - [plots](#plots)
        - [bar_graph_tweet_field_grouped_by_period](#bar_graph_tweet_field_grouped_by_period)
        - [bar_graph_languages](#bar_graph_languages)
        - [bar_graph_user_languages](#bar_graph_user_languages)
        - [bar_graph_tweets](#bar_graph_tweets)
        - [bar_graph_tweets_with_urls](#bar_graph_tweets_with_urls)
        - [bar_graph_tweets_with_media](#bar_graph_tweets_with_media)
        - [bar_graph_tweets_with_mentions](#bar_graph_tweets_with_mentions)
        - [bar_graph_tweets_with_hashtags](#bar_graph_tweets_with_hashtags)
        - [bar_graph_tweets_with_symbols](#bar_graph_tweets_with_symbols)
        - [bar_graph_tweets_with_retweets](#bar_graph_tweets_with_retweets)
        - [bar_graph_tweets_with_locations](#bar_graph_tweets_with_locations)
    - [networks](#networks)
        - [retweet_network](#retweet_network)

# installation

`pip install pysmap`

`pip install pysmap --upgrade`

# twitterutil

the package with an array of twitter tools.

# smapp_collection

this is the smapp_collection class, an abstraction of smappdragon collections.

abstract:
```python
from pysmap import SmappCollection

collection = SmappCollection(DATA_TYPE, OTHER_INPUTS)
```

practical:
```python
from pysmap import SmappCollection

collection = SmappCollection('bson', '/path/to/my/bson/file.bson')
# or
collection = SmappCollection('mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweets_1')
# or
collection = SmappCollection('json', '/path/to/my/file.json')
# or
collection = SmappCollection('csv', '/path/to/my/csv/file.csv')
```

*returns* a collection object that you can use to call methods below on

# smapp_dataset

this is the dataset class, it can be used anywhere one might use a [SmappCollection](#smapp_collection) object. it lets you combine collections and other datasets at will.

abstract:
```python

# standard

dataset = SmappDataset([TYPE_OF INPUT, FILE_PATH], [TYPE_OF_INPUT, MONGO_INPUTS])

# or with regex for matching mongo databases/collections
# this is only for mongo and not for files

dataset = SmappDataset(collection_regex=REGEX, database_regex=REGEX, [MONGO_INPUT, MONGO_INPUT, etc])

dataset = SmappDataset(collection_regex=REGEX, [MONGO_INPUT, MONGO_INPUT, etc])

# or with a unix style file pattern for matching file paths (this is not regex)
# this is only for files and not for mongo

dataset = SmappDataset([TYPE_OF_INPUT, 'file_pattern', FILE_PATTTERN], [TYPE_OF_INPUT, 'file_pattern', FILE_PATTTERN], etc)
```

practical:
```python
# combine collections of the same type
dataset = SmappDataset(['bson', '/path/to/my/bson/file1.bson'], ['bson', '/path/to/my/bson/file2.bson'], ['bson', '/path/to/my/bson/file3.bson'])

dataset = SmappDataset(['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweets_1'], ['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweets_2'])

# combine collections of different types

dataset = SmappDataset(['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweets_1'], ['bson', '/path/to/my/bson/file1.bson'], ['json', '/path/to/my/bson/json_file.json'])

# or combine collections and datasets

collection = SmappCollection('csv', '/path/to/my/csv/file.csv')

dataset_one = SmappDataset(['bson', '/path/to/my/bson/file1.bson'], ['bson', '/path/to/my/bson/file2.bson'], ['bson', '/path/to/my/bson/file3.bson'])

dataset_two =  SmappDataset(['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweets_1'], ['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweets_2'])

final_dataset = SmappDataset(['json', '/path/to/my/bson/json_file.json'], dataset_one, dataset_two, collection)

# or use regex to match for multiple collections/dbs

dataset = SmappDataset(['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler'], collection_regex='(^data$|^tweets$|^tweets_\d+$)')

dataset = SmappDataset(['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD'], collection_regex='(^tweets$|^tweets_\d+$)', database_regex='(^GERMANY_ELECTION_2015_Nagler_\d+$)')

# or use a file pattern to match many files
dataset_one = SmappDataset(['bson', 'file_pattern', '~/smappwork/data_*.bson'])

dataset_two = SmappDataset(['json', 'file_pattern', '~/smappwork/data_*.json'], ['csv', 'file_pattern', '/Users/yvan/data/counts_*.csv'])

dataset_three = SmappDataset(['json', '/non/pattern/path/to/my/bson/json_file.json'], dataset_one, dataset_two)
```

`regex` - regex stands for 'regular expression' its the way programmers pattern match on words, so regex inputs for SmappDataset allow you to pattern match data sources, you must use regex type input patterns or lists+collections+datasets as inputs you cannot use both

`collection_regex` - this is required, to grab all collections named tweets_X (backwards compatiblilty) use `(^tweets$|^tweets_\d+$)` for new/regular collections use `(^data$)` or `(^data$|^tweets$|^tweets_\d+$)` for compatilibly backwards and forwards, if you have a different naming convention you can use a regex to match for that.

`database_regex` - only required for mongo datasets, you can omit this variable if you are not using regex to try to match databases

`file_pattern` - use to select multiple file paths based off a unix style pattern. pysmap smapp_dataset uses [glob](https://docs.python.org/2/library/glob.html#module-glob) under the hood to match the filepaths. pysmap also includes tilde `~` expansion which is not included by glob. so for example:
```
/scratch/smapp/test_dumps_dec1/dump_*.json
#would match 
/scratch/smapp/test_dumps_dec1/dump_1.json
/scratch/smapp/test_dumps_dec1/dump_blah_blah.json 
#and
try_dump_dat_parallel_?.bson
#would match
try_dump_dat_parallel_0.bson
try_dump_dat_parallel_1.bson
#and
try_dump_dat_parallel_[0-9].* 
#would match
try_dump_dat_parallel_0.bson
try_dump_dat_parallel_0.csv 
try_dump_dat_parallel_0.db 
try_dump_dat_parallel_0.json 
try_dump_dat_parallel_1.bson 
try_dump_dat_parallel_1.csv 
try_dump_dat_parallel_1.db
try_dump_dat_parallel_1.json
```
read about [unix file patterns here](http://www.robelle.com/smugbook/wildcard.html).

regex explanation example in the statement:

```python
dataset = SmappDataset(collection_regex='(^tweets$|^tweets_\d+$)', database_regex='(^GERMANY_ELECTION_2015_Nagler_\d+$)', ['mongo', 'superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD'])
```

the collection regex `(^tweets$|^tweets_\d+$)` means match every collection that is called tweets or tweets_\d where `\d` is some number. so tweets, tweets_1, tweets_2, etc

the database regex `(^GERMANY_ELECTION_2015_Nagler_\d+$)` means match every database that has GERMANY_ELECTION_2015_Nagler_\d where `\d` is some number. so GERMANY_ELECTION_2015_Nagler_1, GERMANY_ELECTION_2015_Nagler_2, etc. the regex will not match 'GERMANY_ELECTION_2015_Nagler' in this case as it lacks the term '^GERMANY_ELECTION_2015_Nagler$'.

*input* several `SmappDataset` objects and/or `SmappCollection` objects

*output* a SmappDataset object that can be used the same way a [SmappCollection](#smapp_collection) can be 

#iterate through tweets

iterate through the tweets in the collection you've made.

abstract:
```python
for tweet in collection:
    print(tweet)
```

practical:
```python
for tweet in collection.get_tweets_containing('cat').tweet_language_is('fr'):
    print(tweet)
```

note:

if on nyu hpc, print will not work, totally out of my control. you gotta change locale. 

to fix it, you need to reset the default bash encoding BEFORE opening/running python. just type in bash:
```
LANG=en_US.utf8 
```

# set_custom_filter

sets a user defined function to act as a filter

abstract:
```python
collection.set_custom_filter(TERM)
```

practical:
```python
def my_cust_filter(tweet):
    if 'text' in tweet and 'cats' in tweet['text']:
        return True
    else:
        return False

collection.set_custom_filter(my_cust_filter)
```

*returns* a collection or dataset whese all tweets will be passed through the filter

note this is just a wrapper for smappdragons [set_custom_filter](https://github.com/SMAPPNYU/smappdragon#set_custom_filter) function.

# get_tweets_containing

gets tweets containing the specified term.

abstract:
```python
collection.get_tweets_containing(TERM)
```

practical:
```python
collection.get_tweets_containing('cats')
```

*returns* a collection which will filter out any tweets that do no have the specified term

# count_tweet_terms

counts the number of tweets that contain all these terms

abstract:
```python
collection.count_tweet_terms(TERM_1, TERM_2, ETC)
```

practical:
```python
count = collection.count_tweet_terms('cats', 'dogs')
print(count)
```

*returns* an integer value that counts all the tweets containing the terms

# count_tweets

counts the number of tweets in a collection

abstract:
```python
collection.count_tweets()
```

practical:
```python
count = collection.count_tweets()
print(count)
```

*returns* an integer value that counts all the tweets in a collection

# get_top_terms

counts thet top words in a collection, [english stop words](https://github.com/Alir3z4/stop-words/blob/25c6a0aea665871e887f155b883e950c3743ce50/english.txt) are automatically included, otherwise you can specify your own set of stopwords with python stop-wrods. the stopwords are words taht get ignored and dwill not return in the final counts

abstract:
```python
collection.count_tweet_terms(MUMBER_OF_TERMS, LIST_OF_STOP_WORDS)
```

practical:
```python
count = collection.get_top_terms(5)
#or
count = collection.get_top_terms(5, ['blah', 'it', 'cat'])
print(count)
```

*note* `LIST_OF_STOP_WORDS` is optional, it is set to englis hby default

*returns* a dictionary that has all the top_X terms 

# get_tweet_texts

returns a new collection where the only key will be tweets.

abstract:
```python
for text in collection.get_tweet_texts():
    print(text)
```

practical:
```python
for text in collection.get_tweet_texts():
    print(text)
```

*returns* an iterator that returns just the text of each tweet

# get_date_range

gets tweets in a date range specified by python datmetime objects

abstract:
```python
collection.get_date_range(START, END)
```

practical:
```python
from datetime import datetime
collection.get_date_range(datetime(2014,1,30), datetime(2014,4,30))
```

*returns* a collection that will only return tweets from the specified datetime range

# find_date_range

finds the date range (min/max date in a collection)

abstract:
```python
collection.find_date_range()
```

practical:
```python
from datetime import datetime
range = collection.find_date_range()
print(range)
# or compare to datetime objects
if range['date_min'] > datetime.now()
    print('greater')
elif range['date_max'] < datetime.now():
    print('less')
    print('whatever')
```

*output* 
```
{"date_min":datetime(2016,5,23),"date_max":datetime(2016,5,24)}
```

*returns* a dictionary with two datetime objects

# tweet_language_is

only returns tweets where the language is the specified one (differs from [detect_tweet_language](#detect_tweet_language)  just checks the field on the tweet object reported by twitter, does not detect)

abstract:
```python
collection.tweet_language_is(LANGUAGE_CODES)
```

practical:
```python
#get tweets in english and french
collection.tweet_language_is('en', 'fr')
```

*returns* a collection where all the tweets have their text language as the specified language

# detect_tweet_language

a filter that filters tweets based on language detetction. (differs from [tweet_language_is](#tweet_language_is) because it actually detects the language, tweet_language_is just checks the field on the tweet object reported by twitter)

abstract:
```python
collection.detect_tweet_language(LANGUAGE_CODES)
```

practical:
```python
#get tweets in english
collection.detect_tweet_language('en')
#get tweetsi n english and french
collection.detect_tweet_language('en', 'fr')
```

*returns* a collection where all the tweets have their text language as the specified language

note: uses [langdetect](https://pypi.python.org/pypi/langdetect?) under the hood. it is a pythoh port of google language detection tool.


# user_language_is

only returns tweets where the user's specified language is the specified one

abstract:
```python
collection.user_language_is(LANGUAGE_CODE)
```

practical:
```python
collection.user_language_is('en')
```

*returns* a collection where all the tweets will come from users whose specified language matches the input

# exclude_retweets

exclueds retweets from your collection

abstract:
```python
collection.exclude_retweets()
```

practical:
```python
collection.exclude_retweets()
```

*returns* a collection where there are no retweets


# get_retweets

gets all tweets that are retweets from the collection

abstract:
```python
collection.get_retweets()
```

practical:
```python
collection.get_retweets()
```

*returns* a collection where there are only retweets

# user_location_contains

returns tweets that have a user location that contain one of the listed terms

abstract:
```python
collection.user_location_contains(PLACE_TERM, ANOTHER_PLACE_TERM, ETC)
```

practical:
```python
collection.tweets_with_user_location('CA', 'FL', 'NY', 'palm springs')
```

*returns* a collection where the user location field of that tweet has any of the specified places

# user_description_contains

returns tweets where the user description (for the user tweeting) contained the requested terms

abstract:
```python
collection.user_description_contains(TERM, TERM, ETC)
```

practical:
```python
collection.user_description_contains('dad', 'conservative', 'texas', 'mother')
```

*returns* a collection where the user location field of that tweet has any of the specified places

# place_name_contains_country

returns tweets that have a user location

abstract:
```python
collection.place_name_contains_country(PLACE_TERM, ANOTHER_PLACE_TERM, ETC)
```

practical:
```python
collection.place_name_contains_country('United States', 'France', 'Spain')
```

*returns* a collection where the places field of that tweet has the specified place

note: for more information about places see https://dev.twitter.com/overview/api/places

# within_geobox

returns tweets that ari within a geobox

abstract:
```python
collection.within_geobox(sw_longitude, sw_latitude, ne_longitude, ne_latitude)
```

practical:
```python
collection.within_geobox(-75.280303,39.8670041,-74.9557629,40.1379919)
```

*returns* a collection where the tweets streaming through will be from the stated geobox

note: 
sw_longitude, sw_latitude - the southwest corner
ne_longitude, ne_latitude - the northeast corner
geobox specified by points (longitude, latitude)

# get_geo_enabled

returns only geotagged tweets

abstract:
```python
collection.get_geo_enabled()
```

practical:
```python
collection.get_geo_enabled()
```

*returns* a collection that only produces geo tagged tweets

# get_non_geo_enabled

returns only non geotagged tweets

abstract:
```python
collection.get_non_geo_enabled()
```

practical:
```python
collection.get_non_geo_enabled()
```

*returns* a collection that only produces non geo tagged tweets

# limit_number_of_tweets

limits the # of tweets a collection can output

abstract:
```python
collection.limit_number_of_tweets(LIMIT_NUMEBER)
```

practical:
```python
collection.limit_number_of_tweets(145)

for tweet in collection.limit_number_of_tweets(145):
    print(tweet)
```

*returns* a collection that is limited on terms of the number of tweets it can output

node: works differently than expected on datasets, it will apply this limit to each sub collection/file in the dataset, so if you have 5 files in a dataset it would apply a liit of 145 to each file in the dataset, and
you would end up with 145 x 5 = 725 tweets.

# sample

gets a sample of tweets from a collection using reservior sampling

abstract:
```python
collection.sample(NUMBER_OF_TWEETS_TO_SAMPLE)
```

practical:
```python
collection.sample(10)

for tweet in collection.sample(10):
    print(tweet)
```

*returns* a collection that only returns a sample of tweets as big as the number of tweets you specified

note: you can [read more about reservior sampling here](http://www.geeksforgeeks.org/reservoir-sampling/) and [here](https://en.wikipedia.org/wiki/Reservoir_sampling). reservior sampling allows us to sample a data set in one pass

# dump_to_bson

abstract:
```python
collection.dump_to_bson(output_file)
```

practical:
```python
collection.dump_to_bson('/Users/blah/your_data.bson')
# or with a dataset dumping to one file
dataset.dump_to_bson('/Users/blah/your_data.bson')
# or with a dataset dumping to one file for each input
dataset.dump_to_bson('/Users/blah/your_data.bson', parallel=True)
```

`parallel` - with the 'parallel' option set to true the dump method works a little differently for SmappDataset objects, it does not dump to one file but rather a file for each subsection in the dataset, so each SmappCollection, input, or SmappDataset inside the SmappDataset get its own file.

*input* a path to a bson file

*output* a bson file with the data from your SmappCollection

# dump_to_json

abstract:
```python
collection.dump_to_json(output_file)
```

practical:
```python
collection.dump_to_json('/Users/blah/your_data.json')
# or with a dataset dumping to one file
dataset.dump_to_json('/Users/blah/your_data.json')
# or with a dataset dumping to one file for each input
dataset.dump_to_json('/Users/blah/your_data.json', parallel=True)
```

`parallel` - with the 'parallel' option set to true the dump method works a little differently for SmappDataset objects, it does not dump to one file but rather a file for each subsection in the dataset, so each SmappCollection, input, or SmappDataset inside the SmappDataset get its own file.

*input* a path to a json file

*output* a json file with the data from your SmappCollection

# dump_to_csv

dumps a collection/dataset to a csv based on the fields you specify. can see the fields inside a tweet object [here](https://dev.twitter.com/overview/api/tweets).

abstract:
```python
collection.dump_to_csv('/PATH/TO/OUTPUT/FILE.csv', ['FIELD1', 'FIELD2', 'FIELD3.SUBFIELD', ETC])
```

practical:
```python
collection.dump_to_csv('~/smappstuff/file.csv', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
# or 
collection.limit_number_of_tweets(5).dump_to_csv('/Users/kevin/work/smappwork/file.csv', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
# or with a dataset dumping to one file
dataset.dump_to_csv('/Users/blah/your_data.csv', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
# or with a dataset dumping to one file for each input
dataset.dump_to_csv('/Users/blah/your_data.csv', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'], parallel=True)
```

*input* a path to a csv file and fields to keep

```python
collection = pysmap.SmappCollection('json','/scratch/smapp/us_election_hillary_2016/data/us_election_hillary_2016_data__10_18_2016__00_00_00__23_59_59.json')
# or dataset
dataset = pysmap.SmappDataset(
['json','/scratch/smapp/us_election_hillary_2016/data/us_election_hillary_2016_data__10_18_2016__00_00_00__23_59_59.json'],
['json','/scratch/smapp/us_election_hillary_2016/data/us_election_hillary_2016_data__10_19_2016__00_00_00__23_59_59.json'],
['json','/scratch/smapp/us_election_hillary_2016/data/us_election_hillary_2016_data__10_20_2016__00_00_00__23_59_59.json']
)

field_list = ['id_str',
'coordinates.coordinates.0',
'coordinates.coordinates.1',
'user.id_str',
'user.lang',
'lang',
'text',
'user.screen_name',
'user.location',
'user.description',
'created_at',
'user.friends_count',
'user.followers_count',
'retweet_count',
'entities.urls.0.expanded_url',
'entities.urls.1.expanded_url',
'entities.urls.2.expanded_url',
'entities.urls.3.expanded_url',
'entities.urls.4.expanded_url']

dataset.dump_to_csv('/scratch/smapp/compile_trump_hillary_csvs/us_election_hillary_2016_data.csv', field_list)
```

*output* a csv file with the data from your SmappCollection, but only the fields you chose to keep

```csv
id_str,coordinates.coordinates.0,coordinates.coordinates.1,user.id_str,user.lang,lang,text,user.screen_name,user.location,user.description,created_at,user.friends_count,user.followers_count,retweet_count,entities.urls.0.expanded_url,entities.urls.1.expanded_url,entities.urls.2.expanded_url,entities.urls.3.expanded_url,entities.urls.4.expanded_url

788556059375874048,50,50,2240756971,en,en,RT @dailypenn: The DP and @WellesleyNews are jointly endorsing Wellesley alum @HillaryClinton over Wharton ’68 @realDonaldTrump.… ,CorrectRecord,,Correct The Record is a strategic research and rapid response team designed to defend Hillary Clinton from baseless attacks.,Wed Oct 19 01:43:09 +0000 2016,224,23080,0,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/

788556059317186560,,,4655522325,fr,fr,Barack Obama conseille à Donald Trump « d’arrêter de pleurnicher » -  https://t.co/eEl1mOnIwp https://t.co/8EeOGya28r,metrodakar_net,Senegal,,Wed Oct 19 01:43:09 +0000 2016,110,657,0,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,,,,
```

`parallel` - with the 'parallel' option set to true the dump method works a little differently for SmappDataset objects, it does not dump to one file but rather a file for each subsection in the dataset, so each SmappCollection, input, or SmappDataset inside the SmappDataset get its own file.

note: to get things inside a list you need to refer to their list index. its better to overshoot (so if you want to get 5 entites urls where there are 5) you would use `['entities.urls.0.expanded_url','entities.urls.1.expanded_url','entities.urls.2.expanded_url','entities.urls.3.expanded_url','entities.urls.4.expanded_url']`, for tweet objects with less than 5 `urls` entities this will fill out urls up to 5 urls, if there are less than 5 the extra ones will be empty `,,` fields

note: empty lists `[]` will return nothing. you must specify fields.

note: fields that have no value will appear empty `,,`

# dump_to_sqlite_db

dumps all tweets (only the fields you specify) to an sqlite database file

abstract:
```python
collection.dump_to_sqlite_db('/PATH/TO/OUTPUT/FILE.db', ['FIELD1', 'FIELD2', 'FIELD3.SUBFIELD', ETC])
```

pratical:
```python
collection.dump_to_sqlite_db('~/smappstuff/file.db', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
# or 
collection.limit_number_of_tweets(5).dump_to_sqlite_db('/Users/kevin/work/smappwork/file.db', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
# or 
dataset = pysmap.SmappDataset(
['json','/scratch/smapp/us_election_hillary_2016/data/us_election_hillary_2016_data__10_18_2016__00_00_00__23_59_59.json'],
['json','/scratch/smapp/us_election_hillary_2016/data/us_election_hillary_2016_data__10_19_2016__00_00_00__23_59_59.json'],
['json','/scratch/smapp/us_election_hillary_2016/data/us_election_hillary_2016_data__10_20_2016__00_00_00__23_59_59.json']
)

field_list = ['id_str',
'coordinates.coordinates.0',
'coordinates.coordinates.1',
'user.id_str',
'user.lang',
'lang',
'text',
'user.screen_name',
'user.location',
'user.description',
'created_at',
'user.friends_count',
'user.followers_count',
'retweet_count',
'entities.urls.0.expanded_url',
'entities.urls.1.expanded_url',
'entities.urls.2.expanded_url',
'entities.urls.3.expanded_url',
'entities.urls.4.expanded_url']

dataset.dump_to_sqlite_db('/scratch/smapp/compile_trump_hillary_csvs/us_election_hillary_2016_data.db', field_list)
# or with a dataset dumping to one file for each input
dataset.dump_to_sqlite_db('/scratch/smapp/compile_trump_hillary_csvs/us_election_hillary_2016_data.db', field_list, parallel=True)
```

*input* a collection object and a list of fields/subfields
```
[
    'id_str',
    'coordinates.coordinates.0',
    'coordinates.coordinates.1',
    'user.id_str',
    'user.lang',
    'lang',
    'text',
    'user.screen_name',
    'user.location',
    'user.description',
    'created_at',
    'user.friends_count',
    'user.followers_count',
    'retweet_count',
    'entities.urls.0.expanded_url',
    'entities.urls.1.expanded_url',
    'entities.urls.2.expanded_url',
    'entities.urls.3.expanded_url',
    'entities.urls.4.expanded_url'
]
```

*output* an sqlite db that looks like so:
```
sqlite> .schema
CREATE TABLE data (id_str,user__id_str,text,entities__urls__0__expanded_url,entities__urls__1__expanded_url,entities__media__0__expanded_url,entities__media__1__expanded_url);
sqlite> .tables
data
sqlite> select * from data;
686799531875405824|491074580|@_tessr @ProductHunt No one has stolen me yet. Security through obscurity.|NULL|NULL|NULL|NULL
686661056115175425|491074580|Predictions of peach's demise already starting. Nice.|NULL|NULL|NULL|NULL
686956278099349506|491074580|When was the state of the union first started? Ok wow since the office has existed. https://t.co/Cqgjkhr3Aa|https://en.wikipedia.org/wiki/State_of_the_Union#History|NULL|NULL|NULL
687115788487122944|491074580|RT @lessig: Looks like the @citizenequality act got a supporter tonight. Thank you @POTUS|NULL|NULL|NULL|NULL
686661056115175425|491074580|Predictions of peach's demise already starting. Nice.|NULL|NULL|NULL|NULL
687008713039835136|491074580|#GOPDebate approaching. Can't wait to observer a trump in its natural habitat!|NULL|NULL|NULL|NULL
687208777561448448|18673945|@yvanscher hey! saw u upvoted Cubeit on ProductHunt. Any feedback on how we can make Cubeit better for you? :) Thanks!|NULL|NULL|NULL|NULL
686662539913084928|491074580|RT @PopSci: iOS 9.3 update will tint your screen at night, for your health https://t.co/zrDt4TsoXB https://t.co/yXCEGQPHWp|http://pops.ci/cJWqhM|NULL|http://twitter.com/PopSci/status/686661925267206144/photo/1|NULL
```

`parallel` - with the 'parallel' option set to true the dump method works a little differently for SmappDataset objects, it does not dump to one file but rather a file for each subsection in the dataset, so each SmappCollection, input, or SmappDataset inside the SmappDataset get its own file.

# get_top_entities

returns the top twitter entites from a tweet object, you can [read about twitter entities here](https://dev.twitter.com/overview/api/entities-in-twitter-objects)

abstract:
```python
collection.top_entities({'ENTITY_FIELD':NUMBER_OF_TOP_TERMS, 'ENTITY_FIELD':NUMBER_OF_TOP_TERMS, 'ENTITY_FIELD':NUMBER_OF_TOP_TERMS})
```

practical:
```python
collection.top_entities({'user_mentions':5, 'media':3, 'hashtags':5, 'urls':0, 'user_mentions':2, 'symbols':2})
# or
collection.top_entities({'hashtags':5})
```

*returns* a dictionary containing tho requested entities and the counts for each entity

input:
```python
print collection.top_entities({'user_mentions':5, 'media':3, 'hashtags':5})
```

output:
```
{
        "hashtags": {
                "JadeHelm": 118, 
                "pjnet": 26, 
                "jadehelm": 111, 
                "falseflag": 32, 
                "2a": 26
        },
        "user_mentions": {
                "1619936671": 41, 
                "27234909": 56, 
                "733417892": 121, 
                "10228272": 75, 
                "233498836": 58
        }, 
        "media": {
                "https://t.co/ORaTXOM2oX": 55, 
                "https://t.co/pAfigDPcNc": 27, 
                "https://t.co/TH8TmGuYww": 24
        }
}
```

*returns* a dictionary filled with the top terms you requested

note: passing 0 to a field like `'hashtags':0` returns all the hashtags

note: no support for extended entities, retweet entities, user entites, or direct message entities.

note: if not enough entity objects are returned they get filled into the dictionary with null like so:

```
{
    "symbols": {
            "0": null, 
            "1": null, 
            "hould": 1
    }
}
```

# get_top_hashtags

get the top hashtags from a collection

abstract:
```python
collection.get_top_hashtags(NUMBER_TOP)
```

practical:
```python
hashtags = collection.get_top_hashtags(5)
print(hashtags)
```

*returns* the top hashtags as a dictionary

# get_top_urls

get the top urls from a collection

abstract:
```python
collection.get_top_urls(NUMBER_TOP)
```

practical:
```python
urls = collection.get_top_urls(6)
print(urls)
```

*returns* the top urls from a collection

# get_top_mentions

get the top mentions from a collection (these are @ mentions)

abstract:
```python
collection.get_top_mentions(NUMBER_TOP)
```

practical:
```python
mentions = collection.get_top_mentions(40)
```

*returns* the top @ mentions from a collection

# get_top_media

get the top media url references

abstract:
```python
collection.get_top_media(NUMBER_TOP)
```

practical:
```python
media = collection.get_top_media(3)
print(media)
```

*returns* the top media urls from a collection

# get_top_symbols

get the top symbols in a collection

abstract:
```python
collection.get_top_symbols(NUMBER_TOP)
```

practical:
```python
symbols = collection.get_top_symbols(10)
print(symbols)
```

*returns* the top symbols from a collection the number of top symbols depends on how man yspecified for input

# contributors

you might ask the difference between, pysmap and smappdragon. pysmap is easier to use but less flexible/more rigid in its implementation. smappdragon is a flexible tool fro programmers to use, you can build arbitray filters for data, pysmap is just a set of filters.

methods on smappdragon are lower level and more general. whereas methods on pysmap would be specific and rigid. so for example on smappdragon, you could [get all the entities](https://github.com/SMAPPNYU/smappdragon#top_entities), on pysmap you would have to ask for hashtags, mentions, etc. (which are all entities).

another example, something like [apply_labels](https://github.com/SMAPPNYU/smapp-toolkit#apply_labels) would go on smappdragon, not pysmap.

# viz 

a set of visualization tools, basically ways to graph and visualize a [SmappCollection](#smapp_collection)

# plots

a set of graph tools

# bar_graph_tweet_field_grouped_by_period

a tool that can be used to create generalized bar graphs from a smapp collection an various tweet data.

abstract:
```python
bar_graph_tweet_field_grouped_by_period(SMAPP_COLLECTION, TWEET_FIELD, TWEET_FIELD_VALUES_TO_MATCH, CUSTOM_FILTER_FUNCTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

def custom_filter(tweet):
    return True

plots.bar_graph_tweet_field_grouped_by_period(collection, 'user.lang', ['en', 'fr', 'es'], custom_filter, 'weeks', datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_languages

make a bar graph of the number of tweets containing the specified languages

abstract:
```python
bar_graph_languages(SMAPP_COLLECTION, LANGUAGES_TO_MATCH, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_languages(collection, ['en', 'fr', 'es'], 'days', datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_user_languages

graph all the tweets where the users who made the tweets have one of the specified languages

abstract:
```python
bar_graph_user_languages(SMAPP_COLLECTION, LANGUAGES_TO_MATCH, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_user_languages(collection, ['en', 'fr', 'es'], 'days', datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets

graph all tweets per time period

abstract:
```python
bar_graph_tweets(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

bar_graph_tweets(collection, period_type, start, end, output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets_with_urls

graph all tweets that contain urls by time period

abstract:
```python
bar_graph_tweets_with_urls(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_tweets_with_urls(collection, 'hours',  datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets_with_media

graph all tweets that contain media (like images) by time period

abstract:
```python
bar_graph_tweets_with_media(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_tweets_with_media(collection, 'hours',  datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets_with_mentions

graph all tweets that contain user mentions by time period

abstract:
```python
bar_graph_tweets_with_mentions(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_tweets_with_mentions(collection, 'hours',  datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets_with_hashtags

graph all tweets that contain hashtags by time period

abstract:
```python
bar_graph_tweets_with_hashtags(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_tweets_with_hashtags(collection, 'hours',  datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets_with_symbols

graph all tweets that contain symbols (like stock tickers, $AAPL, $GOOG, $TWTR) by time period

abstract:
```python
bar_graph_tweets_with_symbols(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_tweets_with_symbols(collection, 'hours',  datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets_with_retweets

graph all tweets that are retweets by time period

abstract:
```python
bar_graph_tweets_with_retweets(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_tweets_with_retweets(collection, 'hours',  datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# bar_graph_tweets_with_location

graph all tweets that have a location field attached to them

abstract:
```python
bar_graph_tweets_with_location(SMAPP_COLLECTION, SLICE_PERIOD, START_DATE, END_DATE, OUTPUT_FILE_PATH, X_LABEL, Y_LABEL, GRAPH_TITLE)
```

practical:
```python
from pysmap import SmappCollection, plots

collection = SmappCollection('json', 'docs/tweet_collection.json')
output_path = 'doc/output_graph.html'

plots.bar_graph_tweets_with_location(collection, 'hours',  datetime(2015,9,1), datetime(2015,11,30), output_path, 'time', 'tweet count', 'tweet count v time')
```

*returns* an html graph file and opens the graph in the default browser of the user

# networks

code for making network graphs of twitter data

# retweet_network

export a retweet graph using the `networkx` library where users are nodes, retweets are directed edges.

abstract:
```python
import networkx as nx
from pysmap import networks

digraph = networks.retweet_network(COLLECTION_OBJECT, TWEET_METADATA, USER_METADATA)
nx.write_graphml(digraph, '/path/where/you/want/your.graphml')
```

practical:
```python
import networkx as nx
from pysmap import networks

tweet_fields = ['id_str', 'retweeted_status.id_str', 'timestamp', 'text', 'lang']
user_fields = ['id_str', 'screen_name', 'location', 'description']

digraph = networks.retweet_network(collection, tweet_fields, user_fields)
nx.write_graphml(digraph, '~/smappdata/collection_retweets.graphml')

# or omitting metadata (which saves space)
col = collection.get_tweets_containing('cats').get_retweets()
digraph = networks.retweet_network(col, [], [])
nx.write_graphml(digraph, '~/smappdata/collection_sparse_retweets.graphml')
```

*input*

`collection` - [smapp_dataset](#smapp_dataset) or [smapp_collection](#smapp_collection)

`user_fields` - is a list of fields from the User object that will be included as attributes of the nodes.

`tweet_fields` - is a list of the fields from the Tweet object that will be included as attributes of the edges.

*output*

a `.graphml` file may then be opened in graph analysis/visualization programs such as [Gephi](http://gephi.github.io/) or [Pajek](http://vlado.fmf.uni-lj.si/pub/networks/pajek/).

note: if the collection result includes non-retweets as well, users with no retweets
will also appear in the graph as isolated nodes. only retweets are edges in the resulting graph.

note: nodes and edges have attributes attached to them, which are customizable using the `user_fields` and `tweet_fields` arguments.

note: for large graphs where the structure is interesting but the tweet text itself is not, it is advisable to ommit most of the metadata.

note: the `networkx` library also provides algorithms for [vizualization](http://networkx.github.io/documentation/networkx-1.9.1/reference/drawing.html) and [analysis](http://networkx.github.io/documentation/networkx-1.9.1/reference/algorithms.html).

note: there are no defaults, you have to specify the fields you want.

# developer note '.' field splitting:

there was a habit at the lab of creating one helper function that would take a tweet and a '.' delimited list of fields, split on this character to traverse into a json and save lots of coding time and lines of code. i wanted to leave a few lines here to explain why this is a bad idea in the context of the smapp lab:

1 - it makes code difficult to understand for grad students, we want them to be able to see exactly what a function does without needing to be a python expert.

2 - it casuse problems if you want to traverse into a json object but one of the fields you want 3 levels in has a '.' as part of its name. now twitter doesnt do this but sometimse people cahnge their data to csv, data gets messed up, or people want to use slightly different data. the tools should work for whatever people throw at them, not exclusively for twitter data.

3 - the obvious solution is to offer a function where the user can define a splitting character, the thing is this will be confusing to read. So in the end i conclude to go another route. In the end this would save a few lines of code and reduce readability drastically.

if you want a way to declare nested traversals see: [https://github.com/SMAPPNYU/smappdragon#set_filter](https://github.com/SMAPPNYU/smappdragon#set_filter)

#developer note publishing:

1 - make a ~/.pypirc file with:

[distutils]
index-servers = pypi

[pypi]
repository: https://pypi.python.org/pypi
username: YOUR_PYPI_USERNAME
password: YOUR_PASSWORD

2 - pip install twine

3 - python setup.py sdist

4 - twine upload sdist/*

# author

[yvan](https://github.com/yvan)