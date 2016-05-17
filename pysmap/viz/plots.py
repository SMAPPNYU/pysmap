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
  timeslice is the grouping you want, by day, by week, by month, etc
  start and end is the total date range you want to be queried,
  later ell do multipe fields
'''
def tweet_field_grouped_by_timeslice(collection, field, values_to_match, custom_filter, timeslice, start, end, output_path):
  split_field = field.split('.')

  if timeslice == 'hours':
    time_delta = timedelta(hours=1)
  elif timeslice == 'days':
    time_delta = timedelta(days=1)
  elif timeslice == 'weeks':
    time_delta = timedelta(weeks=1)
  elif timeslice == 'months':
    time_delta = timedelta(weeks=4)
  elif timeslice == 'years':
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

  for tweet in collection.get_date_range(start, end):
    # flattened_tweet = tweet_parser.flatten_dict(tweet)
    if ((field == '') or (tweet[field] in values_to_match)) and custom_filter(tweet):
      tweet_time = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
      period = round((tweet_time - start) // time_delta)
      field_counts[period if period > 0 else 0] += 1

  data = {
    'period':[key for key in field_counts.keys()],
    'instances':[val for val in field_counts.values()]
  }

  output_file(output_path)
  show(Bar(data, 'period', values='instances'))

# import pytz
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# from collections import OrderedDict

# def languages_per_day(collection, start, step_size=timedelta(days=1), num_steps=31,
#   languages=['en', 'es', 'other'], language_colors=['red', 'royalblue', 'grey'],
#   x_label_step = 2, alpha=.65, bar_width=.8, print_progress_every=100000, show=True):
#     # create an ordered dict
#     # where each key is 1-31 (num_steps)
#     # and the value of 1-31 are dicts
#     # each of those dicts 1-31
#     # has keys for each language, and counts.
#     language_counts = OrderedDict()
#     for p in range(num_steps):
#         language_counts[p] = OrderedDict()
#         for l in languages:
#             language_counts[p][l] = 0

#     # Iterate over time period, querying for tweets and storing counts
#     # for each step
#     for step in range(num_steps):
#         # start our query 
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

#             if "lang" not in tweet:
#                 tweet["lang"] = "unk"
#             if tweet["lang"] in languages:
#                 language_counts[step][tweet["lang"]] += 1
#             else:
#                 language_counts[step]["other"] += 1

#         count_total = 0
#         for l in languages:
#             count_total += language_counts[step][l]
#         assert count_total == total, "Error: Tweet by-language count does not match query total"
#         print "\tQuery total: {0}, Count total: {1}".format(total, count_total)
#         print "\t{0}".format(language_counts[step])

#     # Plot tweets in bars by language (in order of languages list)
#     bars = OrderedDict()
#     bars[languages[0]] = plt.bar(range(num_steps),
#                                  [language_counts[i][languages[0]] for i in range(num_steps)],
#                                  width=bar_width,
#                                  linewidth=0.0,
#                                  color=language_colors[0],
#                                  alpha=alpha,
#                                  label=languages[0])

#     for l in languages[1:]:
#         bars[l] = plt.bar(range(num_steps),
#                           [language_counts[i][l] for i in range(num_steps)],
#                           width=bar_width,
#                           linewidth=0.0,
#                           color=language_colors[languages.index(l)],
#                           alpha=alpha,
#                           bottom=[c.get_y() + c.get_height() for c in bars[languages[languages.index(l)-1]].get_children()],
#                           label=l)
#     plt.xlim(0, num_steps)
#     plt.tick_params(axis="x", which="both", bottom="on", top="off", length=8, width=1, color="#999999")
#     # plt.xlabel(x_label)
#     plt.ylabel("# Tweets (by language)")
#     # plt.title(plot_title)
#     plt.legend(fontsize=14, loc=0)
#     plt.xticks(range(num_steps)[::x_label_step],
#                ["{0}-{1}-{2}".format(d.year, d.month, d.day) for d in [start + (i * step_size) for i in range(num_steps)][::x_label_step]],
#                rotation=55)
#     if show:
#         plt.show()

# def tweets_per_day_with_annotations(collection, start, num_steps, step_size=timedelta(days=1),
#     alpha=.4, line_width=2.0, line_color="red", x_label_step=10, events=[], show=True):
#     """
#     Script to plot tweets per day with vertical annotation lines
#     """
#     # Get tweets per day
#     tweets_per_day = []
#     for step in range(num_steps):
#         query_start = start + (step * step_size)
#         tweets = collection.since(query_start).until(query_start+step_size)
#         total = tweets.count()
#         tweets_per_day.append(total)
#         print "{0}: {1} - {2}: {3}".format(step, query_start, query_start + step_size, total)

#     # Plot
#     plt.plot(range(num_steps), tweets_per_day, alpha=alpha, linewidth=line_width, color=line_color)

#     ymin, ymax = plt.ylim()
#     for e in events:
#         plt.axvline(e[0], linestyle="--", color="#999999")
#         if e[2] == "bottom":
#             plt.text(e[0] + 0.2, ymin + (0.05 * ymax), e[1], rotation=-90, verticalalignment="bottom")
#         else:
#             plt.text(e[0] + 0.2, ymax - (0.05 * ymax), e[1], rotation=-90, verticalalignment="top")

#     plt.xlim(0, num_steps-1)
#     plt.ylabel("# Tweets")
#     plt.tick_params(axis="x", which="both", bottom="on", top="off", length=8, width=1, color="#999999")
#     plt.xticks(range(num_steps)[::x_label_step],
#                ["{0}-{1}-{2}".format(d.year, d.month, d.day) for d in [start + (i * step_size) for i in range(num_steps)[::x_label_step]]],
#                rotation=55)
#     if show:
#         plt.show()
# '''
#   Plot a barchart (tweets per timeunit)
# '''
# def tweets_over_time(collection, start, step_size=timedelta(days=1), num_steps=31, alpha=.7, bar_width=.8, x_label_step=7,
#     xtick_format=None, show=True):

#     x_label = "Time"
#     y_label = "Tweets"

#     times = [start + (i * step_size) for i in range(num_steps)]
#     counts = []
#     for step in times:
#         tweets = collection.since(step).until(step + step_size)
#         counts.append(tweets.count())

#     sns.set_style("darkgrid")
#     sns.set_palette("husl")

#     bars = plt.bar(range(num_steps),
#                    counts,
#                    width=bar_width,
#                    linewidth=0.0,
#                    alpha=alpha,
#                    align="edge")

#     plt.xlim(0, num_steps)
#     plt.tick_params(axis="x", which="both", bottom="on", top="off", length=8, width=1, color="#999999")
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)

#     if not xtick_format:
#         if step_size.total_seconds() < 60*60:
#             xtick_format = '%H:%M'
#         elif step_size.total_seconds() < 60*60*24:
#             xtick_format = '%m-%d %H:%M'
#         else:
#             xtick_format = '%Y-%m-%d'

#     plt.xticks(range(num_steps)[::x_label_step],
#                [t.strftime(xtick_format) for t in times[::x_label_step]],
#                rotation=90)

#     plt.tight_layout()
#     if show:
#         plt.show()
#     return times,counts

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

# def tweets_with_urls(collection, group_by='days', xtick_format='%Y-%m-%d', alpha=.65, bar_width=.8, show=True):
#     _entity_stacked_bar_plot(collection, group_by=group_by, column='url', labels=['Tweets with URLs', 'Tweets without URLs'],
#         xtick_format=xtick_format, alpha=alpha, bar_width=bar_width, show=show)

# def tweets_with_images(collection, group_by='days', xtick_format='%Y-%m-%d', alpha=.65, bar_width=.8, show=True):
#     _entity_stacked_bar_plot(collection, group_by=group_by, column='image', labels=['Tweets with images', 'Tweets without images'],
#         xtick_format=xtick_format, alpha=alpha, bar_width=bar_width, show=show)

# def tweets_with_mentions(collection, group_by='days', xtick_format='%Y-%m-%d', alpha=.65, bar_width=.8, show=True):
#     _entity_stacked_bar_plot(collection, group_by=group_by, column='mention', labels=['Tweets with mentions', 'Tweets without mentions'],
#         xtick_format=xtick_format, alpha=alpha, bar_width=bar_width, show=show)

# def tweets_with_hashtags(collection, group_by='days', xtick_format='%Y-%m-%d', alpha=.65, bar_width=.8, show=True):
#     _entity_stacked_bar_plot(collection, group_by=group_by, column='hashtag', labels=['Tweets with hashtags', 'Tweets without hashtags'],
#         xtick_format=xtick_format, alpha=alpha, bar_width=bar_width, show=show)

# def tweets_retweets(collection, group_by='days', xtick_format='%Y-%m-%d', alpha=.65, bar_width=.8, show=True):
#     _entity_stacked_bar_plot(collection, group_by=group_by, column='retweet', labels=['RTs', 'Non-RTs'],
#         xtick_format=xtick_format, alpha=alpha, bar_width=bar_width, show=show)

# def geocoded_tweets(collection, group_by='days', xtick_format='%Y-%m-%d', alpha=.65, bar_width=.8, show=True):
#     _entity_stacked_bar_plot(collection, group_by=group_by, column='geo_enabled', labels=['Geocoded tweets', 'Non-geocoded tweets'],
#         xtick_format=xtick_format, alpha=alpha, bar_width=bar_width, show=show)

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


# '''
#   Used to plot, for instance, tweets per day, with vertical lines to annotate events.
#     `data` is a pandas.DataFrame object holding the line to be plotted
#     `events` is a list of tuples with times, texts and alignments for events to be annotated onto figure
#     `x` is the name of the column in the dataframe to use as the x-axis (defaults to the index)
#     `y` is the column to plot on the y-axis
#   Example (tweets per hour with annotations)
#   #########################################
#   data = collection.group_by('hours')
#   events = [
#     (datetime(2015,6,21,10), 'Sunrise', 'top'),
#     (datetime(2015,6,21,22), 'Sunset', 'bottom')
#   ]
#   plt.figure(10,6)
#   line_with_annotations(data, events, x_tick_timezone='America/New_York')
#   plt.title('Tweets mentioning Donald Trump\non 2015-6-21', fontsize=24)
# '''
# def line_with_annotations(data, events=[], x=None, y='count', x_tick_date_format='%Y-%m-%d', x_tick_timezone='UTC', x_tick_step=2, linewidth=2.0, alpha=.3, line_color='red', x_label_step=2):
#     x = data[x] if x else data.index
#     y = data[y]

#     plt.plot(x, y, alpha=alpha, linewidth=linewidth, color=line_color)

#     ymin, ymax = plt.ylim()
#     for e in events:
#         plt.axvline(e[0], linestyle="--", color="#999999")
#         if e[2] == "bottom":
#             plt.text(e[0], ymin + (0.05 * ymax), e[1], rotation=-90, verticalalignment="bottom")
#         else:
#             plt.text(e[0], ymax - (0.05 * ymax), e[1], rotation=-90, verticalalignment="top")

#     plt.ylabel("# Tweets", fontsize=22)
#     plt.tick_params(axis="x", which="both", bottom="on", top="off", length=8, width=1, color="#999999")
#     plt.xticks(x[::x_label_step], [e.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(x_tick_timezone)).strftime(x_tick_date_format) for e in x[::x_label_step]], fontsize=16, rotation=90)
#     plt.yticks(fontsize=16)
#     plt.xlabel('Time\nin {}'.format(x_tick_timezone), fontsize=22)
