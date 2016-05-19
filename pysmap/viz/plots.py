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
  
# '''
#   If `names` is set, use those. Otherwise, use top `n_names` names.
# '''
# def geolocation_names_per_day(collection, start, step_size=timedelta(days=1), num_steps=31,
#   names=None, name_colors=None, n_names=10,
#   x_label_step = 2, alpha=.65, bar_width=.8, xtick_format='%Y-%m-%d', print_progress_every=100000, show=True):

#     global_name_counts = Counter()
#     # Set up count dict
#     name_counts = OrderedDict()
#     for p in range(num_steps):
#         name_counts[p] = OrderedDict()
#         # for l in names:
#             # name_counts[p][l] = 0

#     # Iterate over time period, querying for tweets and storing counts
#     # NOTE: Could do this with a few mapreduce queries
#     for step in range(num_steps):
#         query_start = start + (step * step_size)
#         print "{0}: {1} - {2}".format(step, query_start, query_start + step_size)

#         # tweets = collection.find({"timestamp": {"$gte": query_start, "$lt": query_start + step_size}})
#         tweets = collection.since(query_start).until(query_start+step_size)
#         total = tweets.count()

#         counter = 0
#         for tweet in tweets:
#             if counter % print_progress_every == 0:
#                 print "\t{0} of {1}".format(counter, total)
#             counter += 1

#             if not tweet.get('place', None):
#                 place_name = "unk"
#             else:
#                 place_name = tweet['place']['full_name']
#                 global_name_counts[place_name] += 1
#             if place_name not in name_counts[step]:
#                 name_counts[step][place_name] = 0
#             name_counts[step][place_name] += 1

#         count_total = 0
#         for n in name_counts[step].keys():
#             count_total += name_counts[step][n]
#         # assert count_total == total, "Error: Tweet by-name count does not match query total"
#         print "\tQuery total: {0}, Count total: {1}".format(total, count_total)

#     # Pick top N places
#     if names is None:
#         names = [e[0] for e in global_name_counts.most_common(n_names)]
#     # Pick colors
#     if name_colors is None:
#         name_colors = sns.color_palette("hls", n_names)
#     elif len(name_colors) != len(names):
#         warnings.warn("name_colors length doesn't match names length. Picking new colors.")
#         name_colors = sns.color_palette("hls", n_names)
#     name_colors.append((.65,.65,.65))

#     for step in range(num_steps):
#         other = sum(name_counts[step][name] for name in name_counts[step] if name not in names)
#         new_name_counts = OrderedDict()
#         for name in names:
#             new_name_counts[name] = name_counts[step].get(name, 0)
#         new_name_counts['other'] = other
#         name_counts[step] = new_name_counts

#     names.append('other')

#     # Plot tweets in bars by name (in order of names list)
#     bars = OrderedDict()
#     bars[names[0]] = plt.bar(range(num_steps),
#                                  [name_counts[i][names[0]] for i in range(num_steps)],
#                                  width=bar_width,
#                                  linewidth=0.0,
#                                  color=name_colors[0],
#                                  alpha=alpha,
#                                  label=names[0])

#     for l in names[1:]:
#         bars[l] = plt.bar(range(num_steps),
#                           [name_counts[i][l] for i in range(num_steps)],
#                           width=bar_width,
#                           linewidth=0.0,
#                           color=name_colors[names.index(l)],
#                           alpha=alpha,
#                           bottom=[c.get_y() + c.get_height() for c in bars[names[names.index(l)-1]].get_children()],
#                           label=l)
#     plt.xlim(0, num_steps)
#     plt.tick_params(axis="x", which="both", bottom="on", top="off", length=8, width=1, color="#999999")
#     plt.ylabel("# Tweets (by geolocation place name)")
#     plt.legend(fontsize=14, loc=1)
#     plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=14)
#     plt.xticks(range(num_steps)[::x_label_step],
#                [d.strftime(xtick_format) for d in [start + (i * step_size) for i in range(num_steps)][::x_label_step]],
#                rotation=55)
#     plt.subplots_adjust(right=.6)
#     if show:
#         plt.show()
# '''
#   If `names` is set, use those. Otherwise, use top `n_names` names.
# '''
# def user_locations_per_day(collection, start, step_size=timedelta(days=1), num_steps=31,
#   names=None, name_colors=None, n_names=10,
#   x_label_step = 2, alpha=.65, bar_width=.8, xtick_format='%Y-%m-%d', print_progress_every=100000, show=True):

#     global_name_counts = Counter()
#     # Set up count dict
#     name_counts = OrderedDict()
#     for p in range(num_steps):
#         name_counts[p] = OrderedDict()
#         # for l in names:
#             # name_counts[p][l] = 0

#     # Iterate over time period, querying for tweets and storing counts
#     # NOTE: Could do this with a few mapreduce queries
#     for step in range(num_steps):
#         query_start = start + (step * step_size)
#         print "{0}: {1} - {2}".format(step, query_start, query_start + step_size)

#         # tweets = collection.find({"timestamp": {"$gte": query_start, "$lt": query_start + step_size}})
#         tweets = collection.since(query_start).until(query_start+step_size)
#         total = tweets.count()

#         counter = 0
#         for tweet in tweets:
#             if counter % print_progress_every == 0:
#                 print "\t{0} of {1}".format(counter, total)
#             counter += 1

#             if not tweet['user'].get('location', None):
#                 place_name = "unk"
#             else:
#                 place_name = tweet['user']['location']
#                 global_name_counts[place_name] += 1
#             if place_name not in name_counts[step]:
#                 name_counts[step][place_name] = 0
#             name_counts[step][place_name] += 1

#         count_total = 0
#         for n in name_counts[step].keys():
#             count_total += name_counts[step][n]
#         # assert count_total == total, "Error: Tweet by-name count does not match query total"
#         print "\tQuery total: {0}, Count total: {1}".format(total, count_total)

#     # Pick top N places
#     if names is None:
#         names = [e[0] for e in global_name_counts.most_common(n_names)]
#     # Pick colors
#     if name_colors is None:
#         name_colors = sns.color_palette("hls", n_names)
#     elif len(name_colors) != len(names):
#         warnings.warn("name_colors length doesn't match names length. Picking new colors.")
#         name_colors = sns.color_palette("hls", n_names)
#     name_colors.append((.65,.65,.65))

#     for step in range(num_steps):
#         other = sum(name_counts[step][name] for name in name_counts[step] if name not in names)
#         new_name_counts = OrderedDict()
#         for name in names:
#             new_name_counts[name] = name_counts[step].get(name, 0)
#         new_name_counts['other'] = other
#         name_counts[step] = new_name_counts

#     names.append('other')

#     # Plot tweets in bars by name (in order of names list)
#     bars = OrderedDict()
#     bars[names[0]] = plt.bar(range(num_steps),
#                                  [name_counts[i][names[0]] for i in range(num_steps)],
#                                  width=bar_width,
#                                  linewidth=0.0,
#                                  color=name_colors[0],
#                                  alpha=alpha,
#                                  label=names[0])

#     for l in names[1:]:
#         bars[l] = plt.bar(range(num_steps),
#                           [name_counts[i][l] for i in range(num_steps)],
#                           width=bar_width,
#                           linewidth=0.0,
#                           color=name_colors[names.index(l)],
#                           alpha=alpha,
#                           bottom=[c.get_y() + c.get_height() for c in bars[names[names.index(l)-1]].get_children()],
#                           label=l)
#     plt.xlim(0, num_steps)
#     plt.tick_params(axis="x", which="both", bottom="on", top="off", length=8, width=1, color="#999999")
#     plt.ylabel("# Tweets (by user location)")
#     plt.legend(fontsize=14, loc=1)
#     plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=14)
#     plt.xticks(range(num_steps)[::x_label_step],
#                [d.strftime(xtick_format) for d in [start + (i * step_size) for i in range(num_steps)][::x_label_step]],
#                rotation=55)
#     plt.subplots_adjust(right=.6)
#     if show:
#         plt.show()

# def _entity_stacked_bar_plot(collection, column, labels, group_by='days', xtick_format='%Y-%m-%d', alpha=.65, bar_width=.8, show=True):
#     data = collection.group_by(group_by).entities_counts()

#     urlbars = plt.bar(np.arange(len(data)),
#                       data[column],
#                       width=bar_width,
#                       linewidth=0.0,
#                       color='b',
#                       alpha=alpha,
#                       label=labels[0])
#     plt.bar(np.arange(len(data)),
#                       data['_total'] - data[column],
#                       width=bar_width,
#                       linewidth=0.0,
#                       color='grey',
#                       alpha=alpha,
#                       bottom=[c.get_y() + c.get_height() for c in urlbars.get_children()],
#                       label=labels[1])
#     plt.xticks(np.arange(len(data))+.3, [ts.strftime(xtick_format) for ts in data.index], rotation=45)
#     plt.legend()

#     if show:
#         plt.show()

# '''
#   Makes a stacked bars plot from data in a pandas.DataFrame.
#   columns are the columns to be stacked.
#   Example: Plot language proportions
#   ##################################
#       data = collection.group_by('days').language_counts(langs=['en','es','other'])
#       plt.figure(figsize=(10,10))
#       stacked_bar_plot(data, ['en','es','other'], colors=['royalblue', 'yellow', 'grey'])
#       plt.title('Tweet proportions in English and Spanish', fontsize=24)
#       plt.tight_layout()
#   -----------------------------------------------------------------
#   Example: Plot retweet proportion
#   ################################
#       data = col.since(datetime(2015,6,18,12)).until(datetime(2015,6,18,12,10)).group_by('minutes').entities_counts()
#       data['original tweet'] = data['_total'] - data['retweet']
#       plt.figure(figsize=(10,10))
#       stacked_bar_plot(data, ['retweet', 'original tweet'], colors=['salmon', 'lightgrey'])
#       plt.title('Retweet proportion', fontsize=24)
#       plt.tight_layout()
# '''

# def stacked_bar_plot(data, columns, x_tick_date_format='%Y-%m-%d', x_tick_step=2, bar_width=.8, alpha=.6, colors=sns.color_palette()):
#     bars = OrderedDict()
#     bars[columns[0]] = plt.bar(range(len(data)),
#                                data[columns[0]],
#                                width=bar_width,
#                                linewidth=0.0,
#                                color=colors[0],
#                                alpha=alpha,
#                                label=columns[0])

#     for l in columns[1:]:
#         bars[l] = plt.bar(range(len(data)),
#                           data[l],
#                           width=bar_width,
#                           linewidth=0.0,
#                           color=colors[columns.index(l)],
#                           alpha=alpha,
#                           bottom=[c.get_y() + c.get_height() for c in bars[columns[columns.index(l)-1]].get_children()],
#                           label=l)
#     plt.xlim(0, len(data))
#     plt.tick_params(axis="x", which="both", bottom="on", top="off", length=8, width=1, color="#999999")
#     plt.legend(fontsize=14, loc=0)
#     plt.xticks(np.arange(len(data))[::x_tick_step]+.4,
#                [x.strftime(x_tick_date_format) for x in data.index[::x_tick_step]],
#                rotation=45,
#                fontsize=18)
#     plt.yticks(fontsize=18)
#     plt.tight_layout()

