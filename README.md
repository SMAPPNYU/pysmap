```
 _ __  _   _ ___ _ __ ___   __ _ _ __
| '_ \| | | / __| '_ ` _ \ / _` | '_ \
| |_) | |_| \__ \ | | | | | (_| | |_) |
| .__/ \__, |___/_| |_| |_|\__,_| .__/
|_|    |___/                    |_|
```

[![PyPI](https://img.shields.io/pypi/v/pysmap.svg)](https://pypi.python.org/pypi/pysmap) [![PyPI](https://img.shields.io/pypi/dm/pysmap.svg)](https://pypi.python.org/pypi/pysmap) [![PyPI](https://img.shields.io/pypi/l/pysmap.svg)](https://github.com/SMAPPNYU/pysmap/blob/master/LICENSE)

:snake: pysmap is a high level toolkit for dealing with twitter data it also has a higher level interface for [smappdragon](https://github.com/SMAPPNYU/smappdragon). it has functionality from the old toolkit and functionality from our old util library smappPy.
- [twitterutil](#twitterutil)
    - [smapp_collection](#smapp_collection)
        - [get_tweets_containing](#get_tweets_containing)
        - [count_tweet_terms](#count_tweet_terms)
        - [count_top_terms](#count_top_terms)
        - [get_tweet_texts](#get_tweet_texts)
        - [get_date_range](#get_date_range)
        - [tweet_language_is](#tweet_language_is)
        - [user_language_is](#user_language_is)
        - [exclude_retweets](#exclude_retweets)
        - [tweets_with_user_location](#tweets_with_user_location)
        - [get_geo_enabled](#get_geo_enabled)
        - [get_non_geo_enabled](#get_non_geo_enabled)
        - [limit_number_of_tweets](#limit_number_of_tweets)
        - [get_top_hashtags](#get_top_hashtags)
        - [get_top_urls](#get_top_urls)
        - [get_top_mentions](#get_top_mentions)
        - [get_top_media](#get_top_media)
        - [get_top_symbols](#get_top_symbols)

#twitterutil

the package with an array of twitter tools.

#smapp_collection

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

#get_tweets_containing

gets tweets containing the specified term.

abstract:
```python
collection.get_tweets_containing(TERM)
```

practical:
```python
collection.get_tweets_containing('cats')
```

*returns* a collections which will filter out any tweets that do no have the specified term

#count_tweet_terms


abstract:
```python
collection.count_tweet_terms(TERM)
```

practical:
```python
count = collection.count_tweet_terms('cats')
print(count)
```

*returns* a count of all the terms that match the specified term

#get_tweet_texts

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

*returns*

#get_date_range

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

#tweet_language_is

only returns tweets where the language is the specified one

abstract:
```python
collection.tweet_language_is(LANGUAGE_CODE)
```

practical:
```python
#get tweets in english
collection.tweet_language_is('en')
```

*returns* a collection where all the tweets have their text language as the specified language

#user_language_is

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

#exclude_retweets

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

#tweets_with_user_location

returns tweets that have a user location

abstract:
```python
collection.tweets_with_user_location(PLACE_TERM)
```

practical:
```python
collection.tweets_with_user_location('CA')
```

*returns* a collection where the places field of that tweet has the specified place

#get_geo_enabled

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

#get_non_geo_enabled

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

#limit_number_of_tweets

limits the # of tweets a collection can output

abstract:
```python
collection.limit_number_of_tweets(LIMIT_NUMEBER)
```

practical:
```python
collection.limit_number_of_tweets(145)
```

*returns* a collection that is limited on terms of the number of tweets it can output

#get_top_hashtags

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

#get_top_urls

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

#get_top_mentions

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

#get_top_media

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

#get_top_symbols

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

#contributors

you might ask the difference between, pysmap and smappdragon. pysmap is easier to use but less flexible/more rigid in its implementation. smappdragon is a flexible tool fro programmers to use, you can build arbitray filters for data, pysmap is just a set of filters.

methods on smappdragon are lower level and more general. whereas methods on pysmap would be specific and rigid. so for example on smappdragon, you could [get all the entities](https://github.com/SMAPPNYU/smappdragon#top_entities), on pysmap you would have to ask for hashtags, mentions, etc. (which are all entities).

another example, something like [apply_labels](https://github.com/SMAPPNYU/smapp-toolkit#apply_labels) would go on smappdragon, not pysmap.

#author

[yvan](https://github.com/yvan)