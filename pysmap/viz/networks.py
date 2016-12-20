import networkx as nx
from smappdragon import TweetParser

'''
generate a retweet graph from the selection of tweets.
'''
def retweet_network(collection, tweet_fields, user_fields):
    def replace_none(s):
        if s is None:
            return 'NULL'
        return s

    tp = TweetParser()
    dg = nx.DiGraph(name="retweet graph")

    for tweet in collection:

        um_dict = {field:replace_none(value) for field,value in tp.parse_columns_from_tweet(tweet['user'], user_fields)}
        t_dict = {field:replace_none(value) for field,value in tp.parse_columns_from_tweet(tweet, tweet_fields)}

        if tweet['user']['id_str'] not in dg:
            dg.add_node(tweet['user']['id_str'], attr_dict=um_dict)
        if 'retweeted_status' in tweet:
            rtu_dict = {field:replace_none(value) for field,value in tp.parse_columns_from_tweet(tweet['retweeted_status']['user'], user_fields)}
            dg.add_node(tweet['retweeted_status']['user']['id_str'], attr_dict=rtu_dict)
            dg.add_edge(tweet['user']['id_str'], tweet['retweeted_status']['user']['id_str'], attr_dict=rtu_dict)
    return dg