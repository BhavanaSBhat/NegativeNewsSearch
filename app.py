from flask import Flask, render_template, request
import os
from src.data_cleaning_transform import clean_text
from src.news_fetcher import fetch_news_newscatcher_api, fetch_news_twitter_api
from src.sentimental_model import sentimental_model_pipeline, get_sentiments
import pandas as pd
import os
app = Flask(__name__)


template_dir = os.path.abspath('templates/')
app = Flask(__name__, template_folder=template_dir)
@app.route('/')
def home_page():
	return render_template('/index.html')

@app.route('/negativeNewsSearch', methods=['GET'])
def get_twitter_data():
	# Step1 : Fetch news from newscatcher and twitter api
	query_string = request.args.get('query_string')
	language = "en"
	from_date = request.args.get('fromDate')
	to_date = request.args.get('endDate')
	no_of_articles = 10
	news_catcher_news = fetch_news_newscatcher_api(query_string, from_date, to_date, language, no_of_articles)
	twitter_news = fetch_news_twitter_api(query_string, language, "05-11-2022", no_of_articles)

	if news_catcher_news and twitter_news:
		combined_news_reaults = news_catcher_news + twitter_news
	elif news_catcher_news:
		combined_news_reaults = news_catcher_news
	else:
		combined_news_result = twitter_news

	# Step2: clean the news text
	entity_parameter = []
	for news in combined_news_reaults:
		if 'entities' in news.keys():
			entity_parameter = [j['screen_name'] for j in news['entities']['user_mentions']]
		news['clean_text'], news['all_link'] = clean_text(news['full_text'], entity_parameter)

	# Step3: extract sentimentals from the news
	model_pipeline = sentimental_model_pipeline()
	sentiment_news_results = get_sentiments(combined_news_reaults, 'clean_text', model_pipeline)

	# Step4: load sentiment news into a dataframe
	news_data = pd.DataFrame(sentiment_news_results)
	sorted_news_df = news_data.sort_values(by='negative', ascending=False).reset_index(drop=True)
	# TODO: NAGTIVE NEWS SCORE TO BE MORE THAN .90 HAS TO BE SELECTED
	top_5_news = sorted_news_df[sorted_news_df.negative != 0].head(5)
	top_5_news_str = ",".join(list(top_5_news['full_text']))
	return render_template('/index.html', results=top_5_news_str)


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)