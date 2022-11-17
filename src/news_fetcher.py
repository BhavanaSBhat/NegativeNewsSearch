from newscatcherapi import NewsCatcherApiClient
import time
import os
import tweepy

NEWS_CATCHER_API_KEY = os.environ.get('NEWS_API_KEY','LF1AsvzlwVI8s2O5K-l4Y-AzEpIliTvY2YXhrJVuQD0')
# TWITTER_CONSUMER_KEY = os.environ.get('CONSUMER_KEY', 'UYiB42Nj9L8JfN9Fx3uOLcFL8')
# TWITTER_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', 'ONacdBNXDM8GeGnAdeOdoHYqe9UgCxOlEA5RNorPIbi4UTzTHk')
# TWITTER_ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', '1580401806437675008-p4LaOLuU6HRBdhJkTvGwYK45w8oFnI')
# TWITTER_TOKEN_SECRET = os.environ.get('ACCESS_SECRET', '0MafTcZULXzMgIm7RFozRZ5cOPTB3gBM3agWFZmcbOdxD')

TWITTER_CONSUMER_KEY = os.environ.get('CONSUMER_KEY', 'UYiB42Nj9L8JfN9Fx3uOLcFL8')
TWITTER_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', 'ONacdBNXDM8GeGnAdeOdoHYqe9UgCxOlEA5RNorPIbi4UTzTHk')
TWITTER_ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', '1580401806437675008-p4LaOLuU6HRBdhJkTvGwYK45w8oFnI')
TWITTER_TOKEN_SECRET = os.environ.get('ACCESS_SECRET', '0MafTcZULXzMgIm7RFozRZ5cOPTB3gBM3agWFZmcbOdxD')


def fetch_news_newscatcher_api(query_string : str, from_date : str, to_date : str, language : str):
    total_fetached_articles = []
    articles_page_size = 100 # page size defaulted to 10
    try:
        news_catcher_obj = NewsCatcherApiClient(x_api_key=NEWS_CATCHER_API_KEY)
        page_no = 1
        while len(total_fetached_articles) < 2:
            fetched_articles = news_catcher_obj.get_search(q=query_string,lang=language,from_=from_date,
                                to_=to_date,page_size=articles_page_size,page=page_no)['articles']
            total_fetached_articles.extend([{"full_text" : article['summary'], "source":"NewsCatcher"} for article in fetched_articles])
            page_no = page_no + 1
            time.sleep(1)
        return total_fetached_articles
    except Exception as e:
        return total_fetached_articles

def fetch_news_twitter_api(query_string:str, language:str, no_of_articles:int, tweet_mode='extended'):
    auth_obj = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth_obj.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_TOKEN_SECRET)
    tweety_api = tweepy.API(auth_obj)
    list_tweets = tweepy.Cursor(tweety_api.search_tweets, q=query_string, lang=language, tweet_mode=tweet_mode).items(no_of_articles)
    fields_to_fetch = ['full_text', 'entities']
    total_tweets = []
    for tweet in list_tweets:
        sub_tweet_dict = {}
        for field_name in fields_to_fetch:
            sub_tweet_dict[field_name] = tweet._json[field_name]
            sub_tweet_dict['source'] = "twitter"
        total_tweets.append(sub_tweet_dict)
    return total_tweets

#testing parameters
# query_string = '(Apple AND company) OR "Apple Inc"'
# data = fetch_news_twitter_api(query_string, 'en',10)
# print(data)