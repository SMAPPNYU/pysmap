from bokeh.charts import Bar, show, output_file

from datetime import datetime, timedelta
from collections import OrderedDict
from smappdragon import TweetParser

'''
  this gets tweets by timeslice
  collection is a SmappCollection
  field is the field in a tweet on which you want to compare
  values_to_match are the values you want that field to match
  filter can be any extra filter like a custom smappdragon filter
  that can be applied to a tweet to make your graph
  period_type is the grouping you want, by day, by week, by month, etc
  start and end is the total date range you want to be queried,
  later ell do multipe fields
  output_path 
'''
def bar_graph_tweet_field_grouped_by_period(collection, field, values_to_match, custom_filter, period_type, start, end, output_path):
  if period_type == 'hours':
    time_delta = timedelta(hours=1)
  elif period_type == 'days':
    time_delta = timedelta(days=1)
  elif period_type == 'weeks':
    time_delta = timedelta(weeks=1)
  elif period_type == 'months':
    time_delta = timedelta(weeks=4)
  elif period_type == 'years':
    time_delta = timedelta(weeks=52)

  # calculate how many periods we need
  duration = end - start
  periods = round(duration // time_delta)

  # setup a dictionary
  # avoid having an empty dict
  field_counts = {}
  if periods <= 0:
    field_counts[0] = 0
  else:
    for period in range(periods):
      field_counts[period] = 0

  # split the input field for compound fields
  split_field = field.split('.')
  tweet_parser = TweetParser()

  for tweet in collection.get_date_range(start, end):
    flattened_tweet = tweet_parser.flatten_dict(tweet)
    
    for tweet_tuple in flattened_tweet:
      if tweet_tuple[0] == split_field:
        value = tweet_tuple[1] 
        break

    # empty fild value matches all tweets, then only custom filter can be used to count
    if ((field == '') or (value in values_to_match)) and custom_filter(tweet):
      tweet_time = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
      period = round((tweet_time - start) // time_delta)
      field_counts[period if period > 0 else 0] += 1

  data = {
    'period':[key for key in field_counts.keys()],
    'tweets':[val for val in field_counts.values()]
  }

  output_file(output_path)
  show(Bar(data, 'period', values='tweets', title='tweets per period'))

def bar_graph_languages(collection, langs_to_match, period_type, start, end, output_path):
  bar_graph_tweet_field_grouped_by_period(collection, 'lang', langs_to_match, lambda tweet:True, period_type, start, end, output_path)

def bar_graph_user_languages(collection, langs_to_match, period_type, start, end, output_path):
  bar_graph_tweet_field_grouped_by_period(collection, 'user.lang', langs_to_match, lambda tweet:True, period_type, start, end, output_path)

def bar_graph_tweets(collection, period_type, start, end, output_path):
  bar_graph_tweet_field_grouped_by_period(collection, '', [], lambda tweet:True, period_type, start, end, output_path)

def bar_graph_tweets_with_urls(collection, period_type, start, end, output_path):
  def custom_filter(tweet):
    if len(tweet['entities']['urls']) > 0:
      return True
    return False
  bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, period_type, start, end, output_path)

def bar_graph_tweets_with_media(collection, period_type, start, end, output_path):
  def custom_filter(tweet):
    if len(tweet['entities']['media']) > 0:
      return True
    return False
  bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, period_type, start, end, output_path)

def bar_graph_tweets_with_mentions(collection, period_type, start, end, output_path):
  def custom_filter(tweet):
    if len(tweet['entities']['user_mentions']) > 0:
      return True
    return False
  bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, period_type, start, end, output_path)

def bar_graph_tweets_with_hashtags(collection, period_type, start, end, output_path):
  def custom_filter(tweet):
    if len(tweet['entities']['hashtags']) > 0:
      return True
    return False
  bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, period_type, start, end, output_path)

def bar_graph_tweets_with_symbols(collection, period_type, start, end, output_path):
  def custom_filter(tweet):
    if len(tweet['entities']['symbols']) > 0:
      return True
    return False
  bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, period_type, start, end, output_path)

def bar_graph_tweets_with_retweets(collection, period_type, start, end, output_path):
  def custom_filter(tweet):
    if 'retweeted_status' in tweet:
      return True
    return False
  bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, period_type, start, end, output_path)

def bar_graph_tweets_with_locations(collection, period_type, start, end, output_path):
  def custom_filter(tweet):
    if 'retweeted_status' in tweet:
      return True
    return False
  bar_graph_tweet_field_grouped_by_period(collection, '', [], custom_filter, period_type, start, end, output_path)
  