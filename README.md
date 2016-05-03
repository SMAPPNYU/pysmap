```
 ___ _ __ ___   __ _ _ __  _ __  _   _ 
/ __| '_ ` _ \ / _` | '_ \| '_ \| | | |
\__ \ | | | | | (_| | |_) | |_) | |_| |
|___/_| |_| |_|\__,_| .__/| .__/ \__, |
                    |_|   |_|    |___/ 
```
:snake: smappy is a high level toolkit for dealing with twitter data it also has a higher level interface for [smappdragon](https://github.com/SMAPPNYU/smappdragon). it aggregates functionality from the ld toolkit and functionality from our old util library smappPy.

you might ask the difference between, smappy and smappdragon. smappy is easier to use but less flexible/more rigid in its implementation. smappdragon is a flexible tool fro programmers to use, you can build arbitray filters for data, smappy is just a set of filters.

methods on smappdragon are lower level and more general. whereas methods on smappy would be specific and rigid. so for example on smappdragon, you could [get all the entities](https://github.com/SMAPPNYU/smappdragon#top_entities), on smappy you would have to ask for hashtags, mentions, etc. (which are all entities).

another example, something like [apply_labels](https://github.com/SMAPPNYU/smapp-toolkit#apply_labels) would go on smappdragon, not smappy.

- [twitterutil](#twitterutil)
    - [smapp_collection](#smapp_collection)
        - [get_tweets_containing](#get_tweets_containing)
        - [count_tweet_terms](#count_tweet_terms)
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



abstract:
```python
```

practical:
```python
```

*returns*

#smapp_collection



abstract:
```python
```

practical:
```python
```

*returns*

#get_tweets_containing



abstract:
```python
```

practical:
```python
```

*returns*

#count_tweet_terms



abstract:
```python
```

practical:
```python
```

*returns*

#get_tweet_texts



abstract:
```python
```

practical:
```python
```

*returns*

#get_date_range



abstract:
```python
```

practical:
```python
```

*returns*

#tweet_language_is



abstract:
```python
```

practical:
```python
```

*returns*

#user_language_is



abstract:
```python
```

practical:
```python
```

*returns*

#exclude_retweets



abstract:
```python
```

practical:
```python
```

*returns*

#tweets_with_user_location



abstract:
```python
```

practical:
```python
```

*returns*

#get_geo_enabled



abstract:
```python
```

practical:
```python
```

*returns*

#get_non_geo_enabled



abstract:
```python
```

practical:
```python
```

*returns*

#limit_number_of_tweets



abstract:
```python
```

practical:
```python
```

*returns*

#get_top_hashtags



abstract:
```python
```

practical:
```python
```

*returns*

#get_top_urls



abstract:
```python
```

practical:
```python
```

*returns*

#get_top_mentions



abstract:
```python
```

practical:
```python
```

*returns*

#get_top_media



abstract:
```python
```

practical:
```python
```

*returns*

#get_top_symbols



abstract:
```python
```

practical:
```python
```

*returns*



#author

[yvan](https://github.com/yvan)